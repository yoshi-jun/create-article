from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from langchain.document_loaders import TextLoader
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate

#==========================================================================================================
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

#----------------------------------------------------------------------------------------------------------
def MakeWrighterPrompt(title, fname=None)
    
    if fname is None:
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
    if fname is not None:
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
     
        # 記事作成の材料の読み込み    
        loader = TextLoader(fname)
        data   = loader.load()

        # 入力メッセージの作成
        prompt = temp.invoke({"title": title, "data": data[0].page_content})

    # ヒューマンメッセージの作成
    human_message = HumanMessage(content=prompt.to_string())
    
    return (system_message, human_message)

#----------------------------------------------------------------------------------------------------------
def MakeEditorPrompt(article, fname=None):

    if fname is None:
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

    if fname is not None:
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
        # 記事作成の材料の読み込み
        loader = TextLoader(fname)
        data = loader.load()

        
        # プロンプトの作成
        temp = PromptTemplate.from_template(
            "記事の材料:{materi}"
            "記事本文:{article}"
            )
    
        prompt = temp.format(materi=data, article=article)
    # ヒューマンメッセージの作成
    human_message = HumanMessage(content=prompt)
    
    return (system_message, human_message)

#----------------------------------------------------------------------------------------------------------
# def main():    
#     while True:
#         # wrighterの作成
#         while True:
#             mode = input("記事生成に使用するモデルを選択してください (openai, google または ollama) \n")
#             wrighter = GetLlm(mode)
#             if wrighter is not None:
#                 break
            
#             print("対応しているモデル名を入力してください")
    
#         print("記事作成に使用するモデル:" , mode)

#         # 入力テキストの作成と記事生成
#         # ユーザーから記事タイトルの入力
#         title = input(
#             "============================================\n"
#             "記事のタイトルを入力してください\n[\"esc\"を入力して終了]\n"
#             "============================================\n"
#             "タイトル    　　 　: "
#              )
        
#         if title.lower() == "esc":
#             print("終了します。")
#             break
        
#         # 情報の追加
#         while True:
#             materi = input(
#                 "記事作成に使用するファイルを入力してください。使用しない場合はNoneを入力してください\n"
#                 "ファイル名         :"
#               )
            
#             if materi == "None":
#                 materi = None
#                 break
#             if os.path.isfile(materi):
#                 break

#             print("[Error]ファイル"+materi+"が見つかりません。")

#         # wrighterに入力するテキストを作成
#         system_message, human_message = MakeWrighterPrompt(title, fname=materi)
        
#         # raw_articleを作成
#         article = []
#         for chunk in wrighter.stream([system_message, human_message]):
#             if chunk.content:
#                 print(chunk.content, end="", flush=True)
#                 article.append(chunk) # wrighterの出力結果をeditorに渡す
#         editor = wrighter
        
#         print("\n=================================================================================\n")
#         # 編集者によって記事がプロンプトを守っているか確認
#         # editorに入力するテキストを作成
#         system_message, human_message = MakeEditorPrompt(article, fname=materi)
#         # editorによる修正記事の出力
#         for chunk in editor.stream([system_message, human_message]):
#             if chunk.content:
#                 print(chunk.content, end="", flush=True)
#         print("\n")

#----------------------------------------------------------------------------------------------------------
# if __name__ == "__main__":
#    main()
