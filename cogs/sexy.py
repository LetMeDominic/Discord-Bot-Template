import discord
from discord.ext import commands

class Sexy(commands.Cog):

    def __init__(self, client) -> None:
        self.client = client




        @commands.Cog.listener()
        async def on_ready(self):
            print('Python Bot is now online')



        @commands.command()
        async def ping(self, ctx):
            await ctx.send("Pong")


def setup(client):
    client.add_cog(Sexy(client))