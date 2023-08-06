# bot.py
import os
import roll
import crit
import destiny

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Necessary to get the list of emojis
SW = int(os.getenv('SW_SERVER'))
RD = int(os.getenv('RD_SERVER'))

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    roll.initializeEmojiMap(next((x for x in client.guilds if x.id == SW), None).emojis, next((x for x in client.guilds if x.id == RD), None).emojis)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.lower().startswith('$roll'):
        if "d" in message.content.split(' ')[1]:
            await roll.poly(message)
        else:
            await roll.roll(message, 'N')
    elif message.content.lower().startswith('$poly'):
        await roll.poly(message)
    elif message.content.lower().startswith('$crit'):
        await crit.rollCrit(message)
    elif message.content.lower().startswith('$shipcrit'):
        await crit.rollShipCrit(message)
    elif message.content.lower().startswith('$destiny'):
        await destiny.parseDestiny(message)

client.run(TOKEN)