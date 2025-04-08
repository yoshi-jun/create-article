from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_ollama import ChatOllama   #conda に対応していないため見送り
from langchain_community.chat_models import ChatOllama #上記の代わり

from langchain.document_loaders import TextLoader
from langchain.schema import SystemMessage, HumanMessage


def GetEditor(mode):
    # Chatモデルのインスタンスをストリーミングモードで初期化
    if mode.lower() == "openai":
        editor = ChatOpenAI(model="gpt-4o-mini", streaming=True)
    elif mode.lower() == "google" or mode is None:
        editor = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7)
    elif mode.lower() == "ollama":
        editor = ChatOllama(model = "llama3")
    else:
        editor = None
    return editor

def MakeMessage(title, fname=None):
    # システムメッセージ
    if fname is None:
        system_message = SystemMessage(
            content=(
                "あなたはウェブエディターです。1500文字程度で次のタイトルに沿った記事を作成してください。"
                "記事は適度にフランクな口調で作成してください。記事中に読者への問いかけを一つだけ入れてください。"
                "記事中に身近な話題の場合は体験談も入れてください。Markdownの形式で記述しないでください。"
                "記事は必ず日本語で作成してください。"
            )
        )
    if fname is not None:
        system_message = SystemMessage(
            content=(
                "あなたはウェブエディターです。1500文字程度で次のタイトルと取材内容に沿った記事を作成してください。"
                "記事は適度にフランクな口調で作成してください。記事中に読者への問いかけを一つだけ入れてください。"
                "記事中に身近な話題の場合は体験談も入れてください。Markdownの形式で記述しないでください。"
                "記事は必ず日本語で作成してください。"
            )
        )
    
    # ユーザーからの入力メッセージ
    if fname is None:
        human_message = HumanMessage(content=title)
    
    if fname is not None:
        # 記事作成の材料の読み込み
        loader = TextLoader(fname)
        data = loader.load()

        human_message = HumanMessage(
            content=(
                "記事のタイトルは"+title+"です。取材内容は次のとおりです。"+data[0].page_content
            )
        )
    print("プロンプト作成完了")     
    return (system_message, human_message)

def main():
    # editorの作成
    while True:
        mode = input("記事生成に使用するモデルを選択してください (openai, google または ollama) \n")
        editor = GetEditor(mode)
        if editor is not None:
            break
        
        print("対応しているモデル名を入力してください")
    print("mode :",mode)
    # 入力テキストの作成と記事生成
    while True:
        # ユーザーから記事タイトルの入力
        
        title = input("============================================\n記事のタイトルを入力してください\n[\"esc\"を入力して終了]\n============================================\n")
        
        if title.lower() == "esc":
            print("終了します。")
            break

        while True:
            # 記事作成に使用する情報
            materi = input("記事作成に使用するファイルを入力してください。使用しない場合は入力せずにエンターを入力してください\n")

            if os.path.isfile(materi):
                break

            print("ファイル"+materi+"が見つかりません。")
            
        # editorに入力するテキストを作成
        system_message, human_message = MakeMessage(title,fname = materi)
        
        # ストリーミングのレスポンスを生成        
        for chunk in editor.stream([system_message, human_message]):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    main()