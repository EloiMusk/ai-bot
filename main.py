import io
import os
import discord
from dotenv import load_dotenv

from stableDiffusion import query

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

user_token_dict = {}


def set_huggingface_token(token, user_id=None):
    if user_id is None:
        return False
    user_token_dict[user_id] = token


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$'):
        if message.content.startswith('$help'):
            with open('help.md', 'r') as f:
                help_text = f.read()
            await message.channel.send(help_text)
            return

        if message.content.startswith('$set_token'):
            message.content = message.content.replace('$set_token', '')
            message.content = message.content.replace(' ', '')
            if not message.content:
                await message.channel.send('Please provide a token! You can get one at'
                                           ' https://huggingface.co/settings/token')
                return
            set_huggingface_token(message.content, message.author.id)
            await message.channel.send('HuggingFace token set!')
            return

        if message.content.startswith('$generate'):
            if not user_token_dict.get(message.author.id):
                await message.channel.send(
                    'Please set your HuggingFace token first with $set_token. You can get one at '
                    'https://huggingface.co/settings/token')
                return
            message.content = message.content.replace('$generate', '')
            await message.channel.send('Sure thing! gimme a sec...')
            image_bytes = query({"inputs": message.content}, user_token_dict[message.author.id])
            await message.channel.send(file=discord.File(io.BytesIO(image_bytes), 'image.png'))

        if message.content.startswith('hello'):
            await message.channel.send('Hello! I am a bot that generates images from text. '
                                       'You can use me by typing $help')
    else:
        await message.channel.send('Hello! I am a bot that generates images from text. '
                                   'You can use me by typing $help')

client.run(TOKEN)
