# インストールした discord.py を読み込む
import discord
import os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# intentsを設定する必要がある
intents = discord.Intents.none()
intents.reactions = True
intents.guilds = True
intents.messages = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

# test channel id
CHANNEL_ID = 1234306482799902801

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

# メッセージ受信時に動作する処理


@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
