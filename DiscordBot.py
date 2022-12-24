import discord
import re
import time
import threading
import logging


class DiscordEnvironmentVariables:
    def __init__(self, token=None):
        self.token = token


class DiscordEnvironmentParser:
    """
    Obtains information from discord_token.env and returns a DiscordEnvironmentVariables object.
    """
    @classmethod
    def getEnvironmentVariables(cls) -> DiscordEnvironmentVariables:
        environ_variables = DiscordEnvironmentVariables()
        regex = re.compile("TOKEN=(.*)$")
        with open("discord_token.env") as f:
            for line in f:
                environ_variables.token = regex.search(line).group(1)
        return environ_variables


environment_variables = DiscordEnvironmentParser.getEnvironmentVariables()

intents = discord.Intents().all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    if message.content.startswith('!hello'):
        reply = f"Hi, {username} you nincompoop"
        await message.channel.send(reply)


def doSomeProcessing():
    threading.Timer(interval=60, function=doSomeProcessing).start()
    logging.info("Doing something")
    time.sleep(2)
    logging.info("Finished doing something")


logging.basicConfig(level=logging.INFO)
doSomeProcessing()
client.run(token=environment_variables.token)
