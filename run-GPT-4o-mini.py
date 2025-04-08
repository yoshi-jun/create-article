
# Define OpenAI instance
from openai import OpenAI

def create_responce(title):
    client = OpenAI()

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "あなたはウェブエディターです。1500文字程度で次のタイトルに沿った記事を作成してください。適度にフランクな口調をで記事を作成してください。読者への問いかけを一つだけ入れてください。markdownの形式で記述しないでください。身近な話題の場合は体験談も入れてください。"},
            {"role": "user"  , "content": title},
        ],
        stream=True,
    )
    
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
    print("\n")

def main():
    while(1):
        title = input("============================================\n記事のタイトルを入力してください\n[\"esc\"を入力して終了]\n============================================\n")
        if (title == "esc"):
            break
        create_responce(title)

if __name__ == "__main__" :         
    main()
