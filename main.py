import os
import threading
import flask_server
import discord
from discord.ext import commands
import json
from discord.ext.commands import CommandNotFound
import gd
import asyncio
import logging

####################################

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

##################################


intents = discord.Intents.default()
intents.members = True
prefix = '$'

client = commands.Bot(command_prefix=prefix, intents=intents)

class User:
    def __init__(self, id, points):
        self.id = id
        self.points = points


memberlist = []
client.remove_command('help')


@client.event
async def on_ready():
    from datetime import datetime
    await client.change_presence(activity=discord.Streaming(name="SSCL | $help", url='https://www.youtube.com/watch?v=Qyd1Slyhw2s&ab_channel=laura.'))
    print(f'Logged in as: {client.user.name}')
    print(f'bot id: {client.user.id}')
    print(f"discord version: {(discord.__version__)}")
    print(f'Currently at {len(client.guilds)} servers!')
    print('Servers connected to:')
    for server in client.guilds:
        print(f"server.name: {server.name}\n")
        print(f"server id: {server.id}\n")
        print(f'users on server: {server.name}:')
    datetime_object = datetime.now()
    channellog = client.get_channel(int(819208865887420466))
    await channellog.send(f"**[{datetime_object}]** Bot is ready !")
    channel = client.get_channel(816168948226719747)

    while 1:
      for guild in client.guilds:
        for member in guild.members:
          for x in member.activities:
            if type(x) == discord.Game:
            
              if str(x) == "Fortnite":
                a = client.get_user_info(member.id)
                await channel.send(f'{a} please stop playing fortnite! ')
                
      await asyncio.sleep(5)




  


@client.event
async def on_message(message):
    import random
    suslist = ['when the impostor is sus :flushed:', 'did someone say amogus?????', 'STOP POSTING ABOUT AMONG US!!!!!!! IM TIRED OF SEEING IT!!!!', 'when the underwear sus?!??!??!?', f'{message.author.name} is the impostor!!!!!', 'sussy', 'amogus']
    
    if 'amogus' in message.content.lower().replace(" ", "") and message.author != client.user and message.author.id != 482499244658524160:
        await message.channel.send(random.choice(suslist))
        

    await client.process_commands(message)

with open("users.json") as fp:
    users = json.load(fp)


def save_users():
    with open("users.json", "w+") as fp:
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


@client.command()
async def dlt(ctx, id : int):
  if ctx.message.author.id == 482499244658524160:
    try:
      msg = await ctx.fetch_message(id)
      message = ctx.message
      await message.delete()
      await msg.delete()
    except Exception as e:
      print(e)

@client.command()
async def say(ctx, message):
  if ctx.message.author.id == 482499244658524160:
    await ctx.message.delete()
    await ctx.send(message)

       
@client.command(aliases=['balance'], brief='shows how many points you have')
async def bal(ctx, member:discord.Member = None):
    list = []
    for user in users:
        x = get_points_by_id(user)
        username = str(user)

        user_obj = User(username, x)
        list.append(user_obj)

    def return_points(obj):
            return obj.points

    y = ''

    list.sort(key=return_points)
    list.reverse()

    if member == None:
        member = ctx.message.author

    ID = str(member.id)
    total = len(list)
    if ID in users:
        for i in list:
            n = i.id
            if str(ID) == str(n):
                y = str(i.id)

        index = next((i for i, item in enumerate(list) if item.id == y), -1)
        points = users[ID]["points"]
        embed = discord.Embed(title="balance", description=f'{member} has {points} points!', color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'{int(index) + 1}/{total} globally')
        await ctx.send(embed=embed)


    else:
        embed = discord.Embed(title="balance", description=f'{member} hasnt got any points registered', color=0x00ff00)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command(brief='remove points from a memeber, requires ban_members')
@commands.has_permissions(kick_members=True)
async def remove(ctx, member:discord.Member, points):
    amount = int(points)
    remove_points(member, amount)
    save_users()
    embed = discord.Embed(title=f"remove {amount} list points", description=f'removed {amount} points from {member}!', color=0x00ff00)
    await ctx.send(embed=embed)




@client.command()
async def rem(ctx, member:discord.Member, points):
  if ctx.message.author.id == 482499244658524160:
    amount = int(points)
    remove_points(member, amount)
    save_users()
    embed = discord.Embed(title=f"remove {amount} list points", description=f'removed {amount} points from {member}!', color=0x00ff00)
    await ctx.send(embed=embed)





@client.command()
async def php(ctx):
  await ctx.send('https://cdn.discordapp.com/attachments/651480116395900958/829331742796021780/php.gif')
@client.command(aliases=['lb'], brief='shows top 10 (or top index you provide)')
async def leaderboard(ctx, L_INDEX = 1):

    list = []


    for user in users:
        x = get_points_by_id(user)
        username = client.get_user(int(user))
        user_obj = User(username, x)
        list.append(user_obj)

    PAGES = int((len(list) // 10))
    if L_INDEX > PAGES + 1:
        await ctx.send('list index out of range!')
    else:



        def return_points(obj):
            return obj.points

        list.sort(key=return_points)
        list.reverse()
        x = ''
        top = []
        index = 0
        top_index = 1
        START_INDEX = int(f'{L_INDEX}0')
        END_INDEX = START_INDEX - 10

        for i in list:
            try:
                top.append(f'{top_index}. {list[index].id} has {list[index].points} points \n')
                top_index+=1
                index += 1
            except IndexError:
                pass

        try:
            new_list = top[END_INDEX:START_INDEX]
        except IndexError:
            pass

        try:
          top1 = new_list[0]
          new_list.pop(0)

          x = ' '.join(new_list)
          if len(new_list) == 0:
              x = 'ㅤ'
          embed = discord.Embed(title="Leaderboard", description=f"top {L_INDEX}0", color=0x00ff00)
          embed.add_field(name=top1, value=x, inline=False)
          embed.set_footer(text=f'page {L_INDEX} out of {PAGES + 1}')
          await ctx.send(embed=embed)
        except IndexError:
          await ctx.send('something went wrong')



@client.command(brief='add points to a member, requires ban_members')
@commands.has_permissions(kick_members=True)
async def add(ctx, member: discord.Member, amount):
    amount = int(amount)
    add_points(member, amount)
    n = []
    from discord.utils import get

    id = member.id
    id = str(id)

    if id not in users:
        pass

    else:

        points = users[id]["points"]

        async def add_role(role_id):

            x = get(ctx.guild.roles, id=role_id)

            if x in member.roles:
                pass
            else:
                await member.add_roles(x)
                n.append(str(x))

        if int(points) >= 10:
            await add_role(816416582796312638)
        if int(points) >= 50:
            await add_role(816416761477333023)
        if int(points) >= 100:
            await add_role(816416883161956352)
        if int(points) >= 250:
            await add_role(816416977534058507)
        if int(points) >= 500:
            await add_role(816417092122443796)
        if int(points) >= 1000:
            await add_role(816417204835713095)
        if int(points) >= 1500:
            await add_role(817518549420867696)
        if int(points) >= 2000:
            await add_role(817518708221149194)

        z = ' ,'.join(n)
        if z == '':
            z = "no roles to add!"

        list = []
        for user in users:
            x = get_points_by_id(user)
            username = str(user)

            user_obj = User(username, x)
            list.append(user_obj)

        def return_points(obj):
            return obj.points

        y = ''

        list.sort(key=return_points)
        list.reverse()

        if member == None:
            member = ctx.message.author

        ID = str(member.id)
        total = len(list)
        if ID in users:
            for i in list:
                n = i.id
                if str(ID) == str(n):
                    y = str(i.id)

            index = next((i for i, item in enumerate(list) if item.id == y), -1)
            points = users[ID]["points"]
            embed = discord.Embed(title=f"add {amount}", description=f"added {amount} to {member}", color=0x00ff00)
            embed.add_field(name="balance", value=f'{member} has {points} points!')
            embed.add_field(name='new roles:', value=z, inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=f'{index + 1}/{total} globally')
            await ctx.send(embed=embed)
    




@client.command(brief='add points to a member, requires ban_members')
async def ptyx_a(ctx, member:discord.Member, amount):
  if ctx.author.id == 482499244658524160:
    pass

@client.command(brief='creates a backup file, requires ban_members = True')
@commands.has_permissions(ban_members=True)
async def dump(ctx):
    import os
    import shutil
    import datetime
    now = datetime.datetime.now()
    file = f'{os.getcwd()}/users.json'
    backup_file = f'{os.getcwd()}/users.backup'

    channel = client.get_channel(819208865887420466)
    shutil.copy2(file, backup_file)
    await channel.send(f'backup creation time: {now}')
    await channel.send(file=discord.File(backup_file))
    os.remove('users.backup')

@client.command(brief='updates your roles depending on your points')
async def update_status(ctx, member: discord.Member = None):
    from discord.utils import get
    if member == None:
        member = ctx.message.author
    n = []
    id = member.id
    id = str(id)

    if id not in users:
        await ctx.send(f'{member} user doesnt have any list points!')
    else:
        
          

        points = users[id]["points"]

        async def add_role(role_id):

            x = get(ctx.guild.roles, id=role_id)
            if x in member.roles:
              pass
                
            else:

                await member.add_roles(x)
                n.append(str(x))


        if int(points) >= 10:
            await add_role(816416582796312638)
        if int(points) >= 50:
            await add_role(816416761477333023)
        if int(points) >= 100:
            await add_role(816416883161956352)
        if int(points) >= 250:
            await add_role(816416977534058507)
        if int(points) >= 500:
            await add_role(816417092122443796)
        if int(points) >= 1000:
            await add_role(816417204835713095)
        if int(points) >= 1500:
            await add_role(817518549420867696)
        if int(points) >= 2000:
            await add_role(817518708221149194)

        y = ' ,'.join(n)
        if y == '':
            y = "no roles to add!"
          

        embed = discord.Embed(title="Autorole", description=f"roles based on list points", color=0x00ff00)
        embed.add_field(name='roles added:', value=y, inline=False)
        await ctx.send(embed=embed)

@client.command(pass_context=True, brief='help command')
async def help(ctx):
    def is_empty(desc):
        if str(desc) == '':
            return True


    embed = discord.Embed(title="Shitty Spam Challenge List Discord", url="https://discord.gg/2wFSQUTTCF",
                          description="List of avaible commands:", color=0x5cffb8)
    embed.set_author(name="Help")
    embed.set_footer(text="If you have any questions, feel free to ask staff in the server")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/icons/816168948226719744/22530bd98a71de7c854906837c7edebd.webp?size=1024")
    for command in client.commands:
        if is_empty(command.short_doc):
            embed.add_field(name=command, value='no description provided', inline=False)
        else:
            embed.add_field(name=command, value=command.short_doc, inline=False)

    await ctx.author.send(embed=embed)
    emoji = '\N{THUMBS UP SIGN}'
    # or '\U0001f44d' or '👍'
    await ctx.message.add_reaction(emoji)

@client.command()
async def msg(ctx, message):
  if ctx.author.id == 482499244658524160:
    channel = client.get_channel(816168948226719747)
    await channel.send(message)
    




for filename in os.listdir('./Cogs'):
  if filename.endswith('py'):
    newfile, ext = filename.split('.')
    client.load_extension('Cogs.' + newfile)
    print(f'loaded extension {newfile}')
    

       
threading.Thread(target=flask_server.run).start()
client.run(os.getenv('token'))


