import discord
import re


class DiscordEnvironmentParser:
    """
    Obtains information from discord_token.env and stores it in this class.
    """

    def __init__(self):
        self.TOKEN = None

    def getEnvironmentVariables(self):
        regex = re.compile("TOKEN=(.*)$")
        with open("discord_token.env") as f:
            for line in f:
                self.TOKEN = regex.search(line).group(1)


environment_variables = DiscordEnvironmentParser()
environment_variables.getEnvironmentVariables()

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client}')

client.run(environment_variables.TOKEN)


