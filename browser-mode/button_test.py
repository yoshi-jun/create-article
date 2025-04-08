import chainlit as cl


@cl.on_chat_start
def start():
    print("hello", cl.user_session.get("id"))


@cl.on_chat_end
def end():
    print("goodbye", cl.user_session.get("id"))