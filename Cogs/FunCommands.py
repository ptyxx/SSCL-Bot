from discord.ext import commands
from discord.ext.commands import CommandNotFound
from main import prefix

class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='gives you free points')
    async def freepoints(self, ctx):
        await ctx.send('https://tenor.com/view/dance-moves-dancing-singer-groovy-gif-17029825')
        await ctx.send('you wish lol')

    @commands.command(brief='typescript lel')
    async def ts(self, ctx):
      await ctx.send('https://media.discordapp.net/attachments/651480116395900958/820248041713696788/ts.gif')

    @commands.command(brief='when the imposter is delicious')
    async def sus(self, ctx):
        await ctx.send('https://tenor.com/view/imposter-sus-jerma-among-us-when-the-imposter-is-delicious-gif-19672653')





def setup(client):
    client.add_cog(FunCommands(client))