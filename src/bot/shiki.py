# インストールした discord.py を読み込む
import discord
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers.string import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_voyageai import VoyageAIEmbeddings

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# intentsを設定する必要がある
intents = discord.Intents.all()

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# test channel id
CHANNEL_ID = 1234306482799902801

# RAG関係
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")
# llm_model = "claude-3-haiku-20240307"
llm_model = "claude-3-opus-20240229"
embed_model = "voyage-law-2"
embeddigns = VoyageAIEmbeddings(
    voyage_api_key=VOYAGE_API_KEY, model=embed_model)
storage_path = "../../storage"
# file = "title_abst_RAG AND prompt_ja.json"
file = "title_abst_RAG AND prompt.json"
llm = ChatAnthropic(api_key=ANTHROPIC_API_KEY,
                    model_name=llm_model)
vectorstore = FAISS.load_local(
    folder_path=os.path.join(storage_path, file.replace(".json", "")),
    embeddings=embeddigns,
    allow_dangerous_deserialization=True
)
retriver = vectorstore.as_retriever()

template = """
あなたは優秀な研究者です。学生からの研究の質問に対して、最新の研究を参考にしつつ、適切なアプローチを回答してください。
最新の研究動向についてはcontextを参考にしてください:{context}
質問:{question}
"""
prompt = ChatPromptTemplate.from_template(template=template)

# chainを作成
chain = (
    {"context": retriver, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 起動時に動作する処理


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await greet()

# 起動時にメッセージを送る


async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('hello')


# mention+"/rag"があれば、RAGが回答
async def rag(message):
    query = message.content.replace("/rag", "")
    await message.channel.send(chain.invoke(query))

# メッセージ受信時に動作する処理


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    # botがメンションされた時の動作
    if client.user in message.mentions:
        if '/rag' in message.content:
            await rag(message)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
