from discord.ext import commands
from discord.ext.commands import CommandNotFound
from main import prefix
import json
from main import *

with open("pack_points.json") as fp:
    users = json.load(fp)


def save_users():
    with open("pack_points.json", "w+") as fp:
        json.dump(users, fp, sort_keys=False, indent=4)

def add_points(user: discord.User, points: int):
    id = str(user.id)
    if id not in users:
        users[id] = {}
    users[id]["points"] = users[id].get("points", 0) + points
    save_users()

def remove_points(user: discord.User, points: int):
    id = str(user.id)
    if id not in users:
        users[id] = {}
    users[id]["points"] = users[id].get("points", 0) - points
    save_users()

def get_points(user: discord.User):
    id = user.id
    if id in users:
        return users[id].get("points", 0)
    return 0



def get_points_by_id(id):
    if str(id) in users:
        return users[id].get("points", 0)
    return 0



class ListPoints(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command(brief='lol')
    @commands.has_permissions(ban_members=True)
    async def premove(self, ctx, member:discord.Member, points):
      amount = int(points)
      remove_points(member, amount)
      embed = discord.Embed(title=f"remove {amount} pack points", description=f'removed {amount} points from {member}!', color=0x00ff00)
      await ctx.send(embed=embed)


    @commands.command(brief='ol')
    @commands.has_permissions(ban_members=True)
    async def padd(self, ctx, member:discord.Member, amount):
      amount = int(amount)
      add_points(member, amount)
      embed = discord.Embed(title=f"add {amount} pack points", description=f"added {amount} to {member}", color=0x00ff00)
      await ctx.send(embed=embed)



    @commands.command(brief='shows how many pack points you have')
    async def pbalance(self, ctx, member:discord.Member = None):

        if member == None:
            member = ctx.message.author

        id = member.id
        id = str(id)

        if id in users:
            points = users[id]["points"]
            embed = discord.Embed(title="pack point balance", description=f'{member} has {points} points!', color=0x00ff00)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="pack point balance", description=f'{member} hasnt got any points registered', color=0x00ff00)
            await ctx.send(embed=embed)





def setup(client):
    client.add_cog(ListPoints(client))


    



    