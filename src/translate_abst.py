import anthropic
import codecs
import json
import os
import time


def main():
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    model = "claude-3-haiku-20240307"

    with open("../data/title_abst_RAG AND prompt.json", "r") as f:
        dic = json.load(f)

    output = {}
    for title, abst in dic.items():
        prompt = f"""
        あなたは優秀な研究者です。英語で書かれた論文のアブストラクトを読んで日本語に翻訳してください。専門用語については無理に日本語に訳そうとしないでください。翻訳の際は、翻訳した文章のみを表示してください。
        # アブストラクト
        {abst}
        """
        message = client.messages.create(
            model=model,
            max_tokens=1000,  # 出力上限（4096まで）
            temperature=0.0,  # 0.0-1.0
            system="",  # 必要ならシステムプロンプトを設定
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        output[title] = message.content[0].text
        # フリープランのRPMのため
        time.sleep(13)

    with codecs.open("../data/title_abst_RAG AND prompt_ja.json", "w", "utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
