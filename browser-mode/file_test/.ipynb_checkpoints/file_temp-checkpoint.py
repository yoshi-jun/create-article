import chainlit as cl


@cl.on_chat_start
async def start():
    files = None
    
    await cl.Message(content="指定されたLLMのモデルの中から選んでください").send()
    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text file to begin!", accept=["text/plain"]
        ).send()

    text_file = files[0]

    with open(text_file.path, "r", encoding="utf-8") as f:
        text = f.read()

    # Let the user know that the system is ready
    await cl.Message(
        content=text
    ).send()