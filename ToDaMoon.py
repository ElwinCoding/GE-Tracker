import discord
from discord.ext import commands
import ItemID
import tabulate

"""
this is a discord bot

bot-test channel ID: 1064029569801265162
"""

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is online")
    channel = bot.get_channel(1064029569801265162)
    await channel.send(f'{bot.user.name} has connected to Discord!')
    collections = ItemID.ItemCollection()
    queues = ItemID.ItemQueues(collections)
    lists = queues.dumpChecker()
    await channel.send((lists[0]))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!hi"):
        await message.channel.send("Hello!")

bot.run("MTA2NDAyNTA0MDY3MDE2NzE0MA.G26nZj.2-qDpC-1UvgdiahI3TJq3XFSBJANUqS0P_YWok")