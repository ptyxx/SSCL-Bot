from discord.ext import commands
import discord
from main import *

class AdministratorCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='change bot status, Admin only', hidden=True)
    @commands.has_permissions(ban_members=True)
    async def newstat(self, ctx, status):
        await client.change_presence(status=discord.Status.online, activity=discord.Game(status))
        await ctx.send(f'new status: {status}')


  


def setup(client):
    client.add_cog(AdministratorCommands(client))
