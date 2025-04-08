import sys
import webbrowser
import chainlit as cl
from List2Tex import GetLlm, MakeWrighterPrompt

@cl.on_chat_start
async def start():

    await cl.Message(content="# List2Tex").send()
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
                content=f"{wrighter_name}のコンテキストに沿って文章を生成します。\n"
                +"箇条書きの内容を入力してください"
            ).send()
            
            if res:
                title = res["output"]
                break
        # Make Prompt
        sys_msg, hum_msg = MakeWrighterPrompt(title)

        # Print Article
        mes = cl.Message(content="")
        article=[]
        for chunk in wrighter.stream([sys_msg, hum_msg]):
            if token := chunk.content or "":
                await mes.stream_token(token)