import sys
import webbrowser
import chainlit as cl
from article_wrighter import GetLlm, MakeWrighterPrompt, MakeEditorPrompt

@cl.on_chat_start
async def start():

    await cl.Message(content="# 記事生成アプリ試作君v2").send()
    while(1):
        #LLM setup
        llms = ["openai", "google", "ollama"]
        wrighter_name = ""
        
        while(1):
            res = await cl.AskUserMessage(
                content = "使用するLLMを"+",".join(llms)+"から選んでください。\n"
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
        
        # Get Title of Article
        while(True):
            res = await cl.AskUserMessage(
                content=f"{wrighter_name}を使用して記事を作成します。\n"
                +"作成する記事のタイトルを入力してください"
            ).send()
            
            if res:
                title = res["output"]
                break
        # Make Prompt
        sys_msg, hum_msg = MakeWrighterPrompt(title)

        # Print Article
        log = cl.Message(content="")
        await log.stream_token("記事作成中\n")
        article=[]
        for chunk in wrighter.stream([sys_msg, hum_msg]):
            if token := chunk.content or "":
                article.append(token)
        
        await log.stream_token("記事作成完了。プロット開始\n")
        mes = cl.Message(content="")
        sys_msg, hum_msg = MakeEditorPrompt(article)
        for chunk in wrighter.stream([sys_msg, hum_msg]):
            if token := chunk.content or "":
                await mes.stream_token(token)
        
        