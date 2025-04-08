import sys
import webbrowser
import chainlit as cl

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from langchain.document_loaders import TextLoader
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate

# ==========================================================================================
def GetLlm(mode):
    # Chatモデルのインスタンスをストリーミングモードで初期化
    if mode.lower() == "openai":
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    elif mode.lower() == "google" or mode is None:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, streaming=True)
    elif mode.lower() == "ollama":
        llm = ChatOllama(model = "llama3",streaming=True)
    else:
        llm = None
    return llm

#-------------------------------------------------------------------------------------------
def MakeWrighterPrompt(title, materi=None):
    
    if materi is None:
        # システムメッセージの作成
        system_message = SystemMessage(content=
            "あなたはウェブライターです。1500文字程度で次のタイトルに沿った記事を作成してください。"
            "1. 記事が適度にフランクな文体で作成されていること"
            "2. 記事中に読者への問いかけが含まれていること"
            "3. 記事が身近な話題の場合、体験談が含まれていること"
            "4. Markdownの形式で記述されていないこと"
            "5. 記事が日本語で記述されていること"
            "6. タイトル名はタイトル: タイトル名の形式で出力すること"
            )
        # プロンプトテンプレートの作成
        temp = PromptTemplate.from_template(
            "記事のタイトルは{title}です。"
            )

        # 入力メッセージの作成
        prompt = temp.invoke({"title": title})

    # 参考記事なしの場合
    if materi is not None:
        # システムメッセージの作成
        system_message = SystemMessage(content=
            "あなたはウェブライターです。1500文字程度で次のタイトルに沿った記事を作成してください。"
            "1. 記事が適度にフランクな文体で作成されていること"
            "2. 記事中に読者への問いかけが含まれていること"
            "3. 記事が身近な話題の場合、体験談が含まれていること"
            "4. Markdownの形式で記述されていないこと"
            "5. 記事が日本語で記述されていること"
            "6. タイトル名はタイトル: タイトル名の形式で出力すること"
            )
        # プロンプトテンプレートの作成
        temp = PromptTemplate.from_template(
            "記事のタイトルは{title}です。"
            "取材内容は次のとおりです{data}"
            )

        # 入力メッセージの作成
        prompt = temp.invoke({"title": title, "data": materi})

    # ヒューマンメッセージの作成
    human_message = HumanMessage(content=prompt.to_string())
    
    return (system_message, human_message)

#-------------------------------------------------------------------------------------------
def MakeEditorPrompt(article, materi=None):

    if materi is None:
        # システムメッセージの作成
        system_message = SystemMessage(content=
            "あなたはウェブメディアの編集者です。次の条件が正しく守られているかを判断してください。"
            "1. 記事の文体がフランクすぎないこと"
            "2. 記事中に読者への問いかけが含まれていること"
            "3. 記事が身近な話題の場合、体験談が含まれていること"
            "4. 記事がMarkdownの形式で記述しないこと"
            "5. 記事が正確な日本語で記述されていること"
            "6. 記事の文字数が1500文字程度であること"
            "7. タイトルを変更しないこと"
            "8. タイトル名はタイトル: タイトル名の形式で出力すること"
            "上記の全条件が守られている文章に修正し、記事のみを出力してください。"
            )
        # プロンプトの作成
        temp = PromptTemplate.from_template(
            "記事本文:{article}"
        )
        
        prompt = temp.format(article=article)

    if materi is not None:
        # システムメッセージの作成
        system_message = SystemMessage(content=
            "あなたはウェブメディアの編集者です。次の条件が正しく守られているかを判断してください。"
            "1. 記事の文体がフランクすぎないこと"
            "2. 記事中に読者への問いかけが含まれていること"
            "3. 記事が身近な話題の場合、体験談が含まれていること"
            "4. 記事がMarkdown形式で記述しないこと"
            "5. 記事が正確な日本語で記述されていること"
            "6. 記事の文字数が1500文字程度であること"
            "7. タイトルを変更しないこと"
            "9. タイトル名はタイトル: タイトル名の形式で出力すること"
            "8. 記事が材料に沿って作られていること"
            "上記の全条件が守られている記事に修正し、記事のみを出力してください。"
            )
        
        # プロンプトの作成
        temp = PromptTemplate.from_template(
            "記事の材料:{materi}"
            "記事本文:{article}"
            )
    
        prompt = temp.format(materi=materi, article=article)
    # ヒューマンメッセージの作成
    human_message = HumanMessage(content=prompt)
    
    return (system_message, human_message)

#============================================================================================
@cl.on_chat_start
async def start():

    await cl.Message(content="# 記事生成アプリ君v3").send()
    
    while(1):
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # LLM setup
        llms = ["openai", "google", "ollama"]
        wrighter_name = ""
        
        while(1):
            res = await cl.AskUserMessage(
                content="使用するLLMを"+",".join(llms)+"から選んでください。openaiを使用する場合\n"
                # +"終了する場合はescを入力してください"
                ).send()
            
            if res:
                wrighter_name = res["output"]
                
                if wrighter_name == "esc":
                    webbrowser.open("about:blank")
                    sys.exit()
                
                wrighter = GetLlm(wrighter_name)
            
                if wrighter:
                    break
            
            await cl.Message(content="指定されたLLMのモデルの中から選んでください").send()
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Get Title of Article
        while(True):
            res = await cl.AskUserMessage(
                content=f"{wrighter_name}を使用して記事を作成します。\n"
                +"作成する記事のタイトルを入力してください"
                ).send()
            
            if res:
                title = res["output"]
                break
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Get File of Article material 
        res = await cl.AskUserMessage(
            content = "記事作成に取材情報を使用しますか(y or n)"
            ).send()
        
        files = None
        text  = None
        
        if res["output"] == "y" or res["output"] == "Y":
            while(files == None):
                files = await cl.AskFileMessage(
                    content="テキストファイルを添付してください。", accept=["text/plain"]
                    ).send()
            
            text_file = files[0]
            
            with open(text_file.path, "r", encoding="utf-8") as f:
                text = f.read()
            
            # Print text written in file
            await cl.Message(
                content=text
            ).send()
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Make Prompt
        sys_msg, hum_msg = MakeWrighterPrompt(title, text)
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Print Article
        log = cl.Message(content="")
        mes = cl.Message(content="")
        
        await log.stream_token("記事作成中\n")
        article = []
        
        for chunk in wrighter.stream([sys_msg, hum_msg]):
            if token := chunk.content or "":
                article.append(token)
                await mes.stream_token(token)
        
        # await log.stream_token("記事作成完了。プロット開始\n")
        # sys_msg, hum_msg = MakeEditorPrompt(article, text)
        # for chunk in wrighter.stream([sys_msg, hum_msg]):
        #     if token := chunk.content or "":
        #         await mes.stream_token(token)
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~