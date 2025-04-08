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
def MakeWrighterPrompt(bullet, fname=None):
    if fname is None:
        # システムメッセージの作成
        system_message = SystemMessage(content=
            "入力される箇条書きを文章に構成してください。"
            "1. 正しい日本語で記述されていること"
            "2. 箇条書きのコンテキストに沿っていること"
            )
        # プロンプトテンプレートの作成
        temp = PromptTemplate.from_template(
            "箇条書きの内容は{bullet}です。"
            )

        # 入力メッセージの作成
        prompt = temp.invoke({"bullet": bullet})

    # ヒューマンメッセージの作成
    human_message = HumanMessage(content=prompt.to_string())
    
    return (system_message, human_message)

