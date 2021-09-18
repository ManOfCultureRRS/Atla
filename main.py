import discord
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
from discord import Status
from discord.ext import commands, tasks
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import topgg
import datetime
import random
import time
import pytz
import json
import os
import asyncio
import dotenv
import praw
from replit import db
import numpy as np
import math
from math import sin, cos, tan
import dbl
import sys
import logging
import aiohttp
from aiohttp import request
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv
from datetime import date
import keep_alive
import voteopenaccfunc


intents =intents = discord.Intents.default()
client = commands.AutoShardedBot(command_prefix=['t ', 'T '],
                      help_command=None,
                      case_insensitive=True,
                      intents=intents,
                      chunk_guilds_at_startup=False, owner_id=727170051777626234)

slash = SlashCommand(client, sync_commands=True, override_type = True)
load_dotenv('.env')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



#-----------------------------VOTE WEBHOOK-------------------------------
client.topgg_webhook = topgg.WebhookManager(client).dbl_webhook("/dblwebhook", "atlaauth123456")
client.topgg_webhook.run(8080)

@client.event
async def on_dbl_vote(data):
  """An event that is called whenever someone votes for the bot on Top.gg."""
  if data["type"] == "test":
      # this is roughly equivalent to
      # return await on_dbl_test(data) in this case
      return client.dispatch('dbl_test', data)

  print(f"Received a vote:\n{data}")
  user = data["user"]
  user.id = int(data["user"])
  users = await get_bank_data()
  await voteopenaccfunc.vote_open_account(user)
  x = data["isWeekend"]
  if x == True:
    users[str(user)]["rare"] += 2
    users[str(user)]["bank"] += 20
  elif x == False:
    users[str(user)]["rare"] += 1
    users[str(user)]["bank"] += 10
  
  with open("mainbank.json","w") as f:
          json.dump(users,f)

@client.event
async def on_dbl_test(data):
  """An event that is called whenever someone tests the webhook system for your bot on Top.gg."""
  print(f"Received a test vote:\n{data}")
  user = data["user"]
  
  users = await get_bank_data()
  await voteopenaccfunc.vote_open_account(user)
  x = data["isWeekend"]
  if x == True:
    users[str(user)]["rare"] += 2
    users[str(user)]["bank"] += 20
  elif x == False:
    users[str(user)]["rare"] += 1
    users[str(user)]["bank"] += 10
  
  with open("mainbank.json","w") as f:
          json.dump(users,f)

#--------------------------------------------------------------------------


#--------------------top.gg server count auto poster----------------------
dbl_token = os.getenv('dbl_token')  # set this to your bot's Top.gg token
client.topggpy = topgg.DBLClient(client, dbl_token, autopost=True, post_shard_count=True)

@client.event
async def on_autopost_success():
    print(f'Posted server count and shard count to top.gg successfully')

#---------------------------------------------------------------------------------

@client.event
async def on_ready():
    
    try:
      DiscordComponents(client)
      print("Discord components loaded successfully")
    except Exception as componentloaderror:
      print("Error while loading Discord components: ", componentloaderror)

    try:
      client.load_extension("cogs.music")
      print("Cog: MusicCommands.py loaded successfully")
    except Exception as err:
      print("Error while loading music cog : "+str(err))

    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="t help | v1.6.0 "))
    print("================================")
    print("The bot is now online\nSession started at " + str(datetime.datetime.now()))
    print(f"Logged in as {client.user}")
    activeservers = client.guilds
    print(f"Currently Serving {len(activeservers)} Guilds")
    print(f"Running on {client.shard_count} shard instances")
    print("================================")

    
admins = [727170051777626234, 443310481764253696]
testers = [592778520640618496, 478102899101138944, 829407629997899797]
global maintenancemode
maintenancemode = False
global adminmode
adminmode = True





@client.command(aliases=["sp", "prefix"])
async def setprefix(ctx, prefix):
  with open("mainbank.json", "w") as f:
        json.dump(users, f)

@client.command()
async def rules(ctx):
    embed = discord.Embed(
        title="Rules ",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        description=
        "Failure in following and/or breaking these rules will result in severe action !"
    )
    embed.set_author(
        name="Atla Bot - Rules",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        icon_url=
        "https://cdn.discordapp.com/avatars/767624993507901470/fe1efb7b2390edfd7ef811c8102a7a6a.webp?size=1024"
    )

    embed.add_field(
        name="Rule 1 - No Sharing Exploits ",
        value=
        "Taking advantage of exploits and sharing them with other players will result in a ban and a blacklist !",
        inline=False)
    embed.add_field(
        name="Rule 2 - Do Not Use The Bot To Abuse",
        value=
        "Using the bot for any of these activities will lead to severe action being taken against you.",
        inline=False)
    embed.add_field(
      name="Rule 3 - No Using Alts/Macros/Scripts/Self-Bots To Farm",
      value="Performing such activities will be automatically detected by the bot and you will be blacklisted !", inline = False
    )
    await ctx.send(embed=embed)


#bot mains
@client.command()
@commands.is_owner()
async def shutdown(ctx):
  
      await ctx.send("Changing client presence to `Offline`")
      await asyncio.sleep(1)
      await ctx.send("Finshing all active tasks ...")
      await asyncio.sleep(1)
      await ctx.send("Closing Discord Websocket Connection...")
      await ctx.send(f" Goodbye ! Client Session Closed at {datetime.datetime.now()}")
      await client.close()
      await client.logout()

@shutdown.error
async def shutdown_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        msg = "<:xs:818502085326405652> ID does not match. You are not the owner of the bot !\nReporting remote shutdown request by unauthorised entity. . ."
        await ctx.send(msg)
        print(f"{ctx.author} (User ID: {ctx.author.id}) tried to shutdown the bot")
    else:
        raise error


@client.command()
async def ping(ctx):
    await ctx.send(f'>>> Pong! Client Latency : `{round(client.latency * 1000)}ms`'
                   )
    await ctx.send("Did you know that Atla can now play music ? Check it out at `t commandlist` !")


@client.command()
async def add(ctx, num1: float=None, num2: float=None):
  if num1 == None or num2 == None:
    await ctx.send("You must mention two numbers to add like this : `t add 1 2`")
  else:
    embed=discord.Embed(colour=000000)
    embed.set_author(name="Addition Calculator")
    embed.add_field(name=f"Input : {num1} + {num2}\t|\tResult :  {num1 + num2}", value=f"Check out the `t math` command to do more complex and longer math", inline=True)
    
    await ctx.reply(embed=embed)
   


@client.command(aliases = ["sub"])
async def subtract(ctx, num1: float=None, num2: float=None):
  if num1 == None or num2 == None:
    await ctx.send("You must mention two numbers to subtract like this : `t sub 1 2`")
  else:
    embed=discord.Embed(colour=000000)
    embed.set_author(name="Subtraction Calculator")
    embed.add_field(name=f"Input : {num1} - {num2}\t|\tResult :  {num1 - num2}", value=f"Check out the `t math` command to do more complex and longer math", inline=True)
    await ctx.reply(embed=embed)

@client.command(aliases = ["mult"])
async def multiply(ctx, num1: float=None, num2: float=None):
  if num1 == None or num2 == None:
    await ctx.send("You must mention two numbers to multiply like this : `t mult 1 2`")
  else:
    embed=discord.Embed(colour=000000)
    embed.set_author(name="Multiplication Calculator")
    embed.add_field(name=f"Input : {num1} x {num2}\t|\tResult :  {num1 * num2}", value=f"Check out the `t math` command to do more complex and longer math", inline=True)
    await ctx.reply(embed=embed)


@client.command(aliases = ["div"])
async def divide(ctx, num1: float=None, num2: float=None):
  if num1 == None or num2 == None:
    await ctx.send("You must mention two numbers to divide like this : `t div 1 2`")
  else:
    embed=discord.Embed(colour=000000)
    embed.set_author(name="Division Calculator")
    embed.add_field(name=f"Input : {num1} / {num2}\t|\tResult :  {num1 / num2}", value=f"Check out the `t math` command to do more complex and longer math", inline=True)
    await ctx.reply(embed=embed)

@client.command()
async def exponentiate(ctx, num1: float=None, num2: float=None):
  if num1 == None or num2 == None:
    await ctx.send("You must mention a number and a power to exponentiate like this : `t add 1 2`")
  else:
    result = num1 ** num2
    await ctx.reply(f"{num1} raised to the power {num2} is equals to {result}")



@client.command()
async def help(ctx):
    one = Button(style=ButtonStyle.URL, label="Join Our Official Server", id="embed1", emoji="🪧", url="https://discord.gg/7e4auv3DHN")
    two = Button(style=ButtonStyle.URL, label="Bot Invite Link", id="embed2", emoji="🤖", url="https://discord.com/api/oauth2/authorize?client_id=767624993507901470&permissions=8&scope=applications.commands%20bot")
    four = Button(style=ButtonStyle.URL, label="Detailed Bot Info", id="embed4", emoji="ℹ️", url="https://top.gg/bot/767624993507901470")
    three = Button(style=ButtonStyle.URL, label="Please Consider Voting\nFor The Bot Here", id="embed1", emoji="🗳️", url="https://top.gg/bot/767624993507901470/vote")
    embed = discord.Embed(
        title="Help Menu",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0cc0ed)
    
    embed.add_field(
        name="What is the bot about?",
        value=
        "An all-purpose bot with music playback in voice channels, fun image generation commands, powerful moderation tools, which can host giveaways, and includes an exclusive Demon Slayer Game !!",
        inline=False)
    embed.add_field(
        name="Bot Usage",
        value=
        "The universal bot command prefix is `t` (Commands are case insensitive)\nFor a list of commands you can visit `t commandlist` !",
        inline=False)
    
    embed.add_field(
        name="Our Official Server",
        value=
        "Join our [support server](https://discord.gg/7e4auv3DHN) for massive giveaways, instant updates and help !"
    )
    embed.add_field(
        name="Info Desk",
        value=
        "For more info on a particular area and its usage , visit `t info`",
        inline=False)
    await ctx.send(embed=embed, components=[[one,two],[four,three]])
    await ctx.send("Did you know that Atla can now play music ? Check it out at `t commandlist` !")

@client.command(aliases=["bi"])
async def botinfo(ctx):
  channel=ctx.channel
  async with channel.typing():
    url = "https://top.gg/api/bots/767624993507901470/stats"
    async with request("GET", url, headers={"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NzYyNDk5MzUwNzkwMTQ3MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEzOTExNTA2fQ.xkdJu5JEd4bTuj_-pTOG-drE5aC-JtGuvRfg0Jn8i_c"}) as response:
    
      url1 = "https://top.gg/api/bots/767624993507901470"
      async with request("GET", url1, headers={"Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NzYyNDk5MzUwNzkwMTQ3MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEzOTExNTA2fQ.xkdJu5JEd4bTuj_-pTOG-drE5aC-JtGuvRfg0Jn8i_c"}) as response1:

        if response.status == 200:
          data = await response.json()
          scount = data["server_count"]
          shards = data["shards"]
          shardscount = data["shard_count"]

          embed = discord.Embed(
            title="Bot Information :bar_chart:",
            url=
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
            color=0x0062ff)
          embed.set_author(name="Atla Bot - Info & Stats", icon_url="https://cdn.discordapp.com/avatars/767624993507901470/fe1efb7b2390edfd7ef811c8102a7a6a.webp?")
        
          if response1.status == 200:
            data1 = await response1.json()

            embed.add_field(name="Bot ID :card_index:",
                          value=f'{data1["id"]}',
                          inline=True)
            embed.add_field(name="Bot Owner :label:",
                          value=f'{await client.fetch_user(727170051777626234)}',
                          inline=True)
            embed.add_field(name="Server Count :placard:",
                          value=f"{scount} Guilds",
                          inline=True)
            embed.add_field(name="Total Upvotes On __top.gg__ :ballot_box:",
                          value=f'{data1["points"]}',
                          inline=True)
          else:
            await ctx.send(f"Bot info request returned a {response1.status}")

            
            

          
          embed.add_field(name="Shards Count ",
                          value=f"{shardscount} ",
                          inline=True)
          embed.add_field(name="Servers Per Shard ",
                          value=f"{shards} ",
                          inline=True)
          

          embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/458276816071950337/c100108f7602bd84ffef257993f77d66.jpg")
          await ctx.send(embed=embed)

        else:
          await ctx.send(f"Bot info request returned a {response.status}")
  
@client.command(aliases=["commands", "command", "commandlist", "cl"])
async def cmdlist(ctx):
    one = Button(style=ButtonStyle.blue, label="General", id="embed1", emoji="📜")
    two = Button(style=ButtonStyle.blue, label="Moderation ", id="embed2", emoji="👨‍⚖️")
    three = Button(style=ButtonStyle.blue, label="Giveaways", id="embed3", emoji="💰")
    four = Button(style=ButtonStyle.blue, label="Demon Slayer Game", id="embed4", emoji="⚔️")
    five = Button(style=ButtonStyle.blue, label="Images", id="embed5", emoji="🖼️")
    six = Button(style=ButtonStyle.blue, label="Music", id="embed6", emoji="💿")
    seven = Button(style=ButtonStyle.blue, label="Utility ", id="embed7", emoji="🛠️")
    eight = Button(style=ButtonStyle.red, label="Close", id="embed8", emoji="✖")
    embed = discord.Embed(
        title="Atla Bot - Command List",
        description="**Click any button to view the list !**",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    
    embed.add_field(name=":one: General Commands  :scroll:",
                    value="All purpose general commands of the bot !",
                    inline=False)
    embed.add_field(
        name=":two: Moderation Commands :man_judge:",
        value=
        "Powerful moderation tools !  (These require certain permissions to use) ",
        inline=False)
    embed.add_field(name=":three: Giveaway Commands  :moneybag:",
                    value="Host giveaways with these commands !",
                    inline=False)
    embed.add_field(name=":four: Utility Commands  :tools: `Work In Progress`",
                    value="Commands to make life easier !",
                    inline=False)
    embed.add_field(name=":five: Demon Slayer Game Commands  :crossed_swords:",
                    value="Exclusive, detailed fun Demon Slayer themed game !",
                    inline=False)
    embed.add_field(name=":six: Fun Image Generation Commands :frame_photo:",
                    value="Fun, cool image generation commands !",
                    inline=False)
    embed.add_field(name=":seven: Music Commands :cd: `NEW`",
                    value="Listen to music on a VC with an advanced queue system, features like pause and much more !",
                    inline=False)
    

    embed.set_footer(
        text="Start interacting with the bot using these commands !")
    mes = await ctx.send(embed=embed, components=[[one,two,three, seven],[four,five,six, eight]])

    

    
    embed1 = discord.Embed(
        title="Command List",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    embed1.set_author(name="Atla Bot - Helpdesk")
    embed1.add_field(name=":one: General  :scroll:",
                    value="All purpose general commands of the bot !",
                    inline=False)
    embed1.add_field(
        name="__Help - `help`__",
        value=
        "Guidance on using the bot and shows the invite link.\n**Usage**: `t help`",
        inline=True)
    embed1.add_field(
        name="__Vote - `vote`__",
        value=
        "Vote for the bot and claim your reward!\n**Usage**: `t vote`",
        inline=True)

    embed1.add_field(
        name="__Bot Information - `botinfo`__",
        value="Returns detailed info on the bot !\n**Usage**: `t botinfo`",
        inline=True)

    embed1.add_field(
        name="__Client Latency - `ping`__",
        value="Returns the latency of the bot !\n**Usage**: `t ping`",
        inline=True)

    embed1.add_field(
        name="__Command List - `commandlist`__",
        value=
        "Lists all available commands.\n**Aliases**: `commands`  `cl`\n**Usage**: `t commandlist`",
        inline=True)

    embed1.add_field(
        name="__Information - `info`__",
        value=
        "Find info on everything and command syntaxes. here\n**Usage**: `t info <category>`",
        inline=True)

    embed1.add_field(
        name="__User Information - `userinfo`__",
        value=
        "Gives more info on a member !\n**Aliases**: `ui`\n**Usage**: `t userinfo <@user>`",
        inline=True)

    embed1.add_field(
        name="__Server Information - `serverinfo`__",
        value=
        "Gives more info about the guild\n**Aliases**: `si`\n**Usage**: `t serverinfo`",
        inline=True)
    embed1.add_field(
        name="__User Avatar - `avatar`__",
        value=
        "Displays the avatar of a user !\n**Aliases**: `av` \n**Usage**: `t avatar <@user (leave empty to view your pfp)>`"
    )

    



    embed2 = discord.Embed(
        title="Command List",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    embed2.set_author(name="Atla Bot - Helpdesk")
    embed2.add_field(name=":two: Moderation :man_judge:",
                  value="Powerful moderation tools ! ",
                  inline=False)
    embed2.add_field(
        name="__Clear - `clear`__",
        value=
        "Deletes messages in a channel !\n**Aliases**: `purge`\n**Usage**: `t clear <number of messages>`",
        inline=True)
    embed2.add_field(
        name="__Kick - `kick`__",
        value=
        "Kicks a member !\n**Usage**: `t kick <@user> <reason (optional)>`",
        inline=True)
    embed2.add_field(
        name="__Snipe - `snipe`__",
        value=
        "Displays the last deleted message (with any attachments) !\n**Usage**: `t snipe`",
        inline=True)
    embed2.add_field(
        name="__Ban - `ban`__",
        value=
        "Bans a member !\n**Usage**: `t ban <@user> <reason (optional)>`",
        inline=True)
    embed2.add_field(
        name="__Unban - `unban`__",
        value=
        "Unbans a member !\n**Usage**: `t unban user#1234 (capital letters in the user name matters)`",
        inline=True)
    embed2.add_field(
        name="__Lock - `lock`__",
        value=
        "Locks a channel preventing people from sending messages in it !\n**Usage**: `t lock <channel (optional)>`",
        inline=True)
    embed2.add_field(
        name="__Unlock - `unlock`__",
        value=
        "Unocks a locked channel re-enabling people to send messages in it !\n**Usage**: `t unlock <channel (optional)>`",
        inline=True)
    
    embed2.add_field(
        name="__Lockdown - `lockdown`__",
        value=
        "Locks all channels preventing people from sending messages in them !\n**Usage**: `t lockdown`",
        inline=True)

    embed2.add_field(
        name="__Remove Lockdown - `removelockdown`__",
        value=
        "Unlocks all channels re-enabling people to send messages in them !\n**Usage**: `t removelockdown`",
        inline=True)
    embed2.add_field(
        name="__Mute - `mute`__",
        value=
        "Mutes a member !\n**Usage**: `t mute <@user> <reason(optional)>`",
        inline=True)
    embed2.add_field(
        name="__Temporary Mute - `tempmute`__",
        value=
        "Mutes a member for a finite duration !\n**Usage**: `t mute <@user> <time> <s/m/h> <reason(optional)>`",
        inline=True)
   
   

    embed2.add_field(
        name="Note: These commands require certain permissions.",
        value="To see what permissions are needed, visit `t info modtools`",
        inline=False)


    embed3 = discord.Embed(
        title="Command List",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    embed3.set_author(name="Atla Bot - Helpdesk")
    embed3.add_field(name=":three: Giveaways  :moneybag:",
                    value="Host giveaways with these commands !",
                    inline=False)
    embed3.add_field(
        name="__Giveaway - `giveaway`__",
        value=
        "Run this command to start a giveaway!\n**Usage:** `t giveaway <time> <unit> <winner count> <prize name>`\nTime must be an integer/decimal. Units can be h/m/d. The winner count must be specified as '1w', '2w' etc.(Maximum 2 winners are supported. In the upcoming update, upto 5 will be supported)\n**Example:** ` t giveaway 12 h 2w discord nitro` would start a giveaway with a duration of 12 hours, with 2 winners and a prize of discord nitro.\n**Aliases:** `ga`  `lottery`",
        inline=False)
    embed3.add_field(
        name="__Reroll - `reroll`__",
        value=
        "Rerolls and selects a new winner of a giveaway !\n**Usage**: `t reroll <#channel> <Giveaway ID (Mentioned in the winner notice)>`",
        inline=False)

  
    embed4 = discord.Embed(
        title="Command List",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    embed4.set_author(name="Atla Bot - Helpdesk")
    embed4.add_field(
        name=":four: Demon Slayer Game :crossed_swords:",
        value="Exclusive, detailed fun Demon Slayer themed game !",
        inline=False)

    embed4.add_field(name="__Balance - `balance`__, `bal`",
                    value="View your wallet balance!",
                    inline=True)
    embed4.add_field(name="__Bag - `bag`__",
                    value="View your bag and owned items!",
                    inline=True)
    embed4.add_field(name="__Daily Reward - `daily`__",
                    value="Claim your daily reward!",
                    inline=True)
    embed4.add_field(
        name="__Profile - `profile`__",
        value=
        "View your profile, level, slayer corps rank and much more stats!",
        inline=False)
    embed4.add_field(
        name=
        "__Mines - `mine1`/`m1` , `mine2`/`m2` , `mine3`/`m3` , `mine4`/`m4` , `mine5`/`m5` , `mine6`/`m6`__",
        value=
        "Mine for items !  Note: There is a minimum lvl restriction for each mine",
        inline=False)
    embed4.add_field(
        name=
        "__Wisteria Market (Shop, Loot Crate Shop) - `shop`__",
        value=
        "Visit and purchase items or loot crates !\nSyntax: `t shop` for menu",
        inline=False)
    embed4.add_field(
        name=
        "__Item Info - `iteminfo`__",
        value=
        "View more info such as sell price etc. of an item\nAliases: `ii`\nSyntax: `t iteminfo <Item ID (in shop)>`",
        inline=False)
    embed4.add_field(
        name=
        "__Level & Rank - `level`__",
        value=
        "View your level and rank progress\nAliases: `lvl`\nSyntax: `t lvl <@user/user id (optional)>`",
        inline=False)
    embed4.add_field(
        name=
        "__Open Loot Crates - `crate`__",
        value=
        "Open loot crates from your bag or pay to open one instantly !\nSyntax: `t crate <rarity>` example `t crate epic`",
        inline=False)
    embed4.add_field(
        name="__Forging Items & Equipment- `forge`__",
        value=
        "View forging menu !\nSyntax: `t forge` for menu or `t forge <item id> <quantity(defaults to 1)>` for forging",
        inline=False)
    embed4.add_field(
        name="__Buy and Sell `buy` , `sell`__",
        value=
        "Buy and sell items from the Wisteria Market with \n`t buy <item id> <quantity(defaults to 1)>` for buying \nand `t sell <item id> <quantity(defaults to 1)>` for selling",
        inline=False)
    embed4.add_field(name="__Missions - COMING SOON__",
                    value="Go on missions assigned by the Slayer Corps",
                    inline=True)
    embed4.add_field(name="__My Moves and Move List - COMING SOON__",
                    value="View your owned moves !",
                    inline=True)
  
    embed5 = discord.Embed(
        title="Command List",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    embed5.set_author(name="Atla Bot - Helpdesk")
    embed5.add_field(name=":five: Fun Image Generation :frame_photo:",
                value="Fun, cool image generation commands !",
                inline=False)
    embed5.add_field(name="__Drip - `drip`__",
                    value="Make someone look drip !\n**Usage**: `t drip @user`",
                    inline=True)
    embed5.add_field(name="__Wasted - `wasted`__",
                    value="Waste someone GTA style !\n**Usage**: `t wasted @user`",
                    inline=True)
    embed5.add_field(name="__Low Quality - `lowquality`__",
                    value="Returns low quality profile pictures of a user !`\n**Usage**: `t lowquality @user`",
                    inline=True)
    embed5.add_field(name="__I Raised That Boy - `raisedthatboy`__",
                    value="Generates the `Raised that boy` meme with yourself and another user of choice!\n**Aliases**: `chibirun`\n**Usage**: `t nezukorun @user`",
                    inline=True)
    embed5.add_field(name="__Omae Wa Mou Shindeiru - `omaewamoushindeiru`__",
                    value="Generates the `You are already dead` meme with yourself and another user of choice !\n**Aliases**: `owms`\n**Usage**: `t omaewamoushindeiru @user`",
                    inline=True)
    embed5.add_field(name="__Nezuko Run - `nezukorun`__",
                    value="Generates the `Nezuko chibi run` meme with yourself and another user of choice !\n**Aliases**: `chibirun`\n**Usage**: `t nezukorun @user`",
                    inline=True)
    
    embed6 = discord.Embed(
        title="Command List",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0062ff)
    embed6.set_author(name="Atla Bot - Helpdesk")
    embed6.add_field(name=":six: Music :cd: `NEW`",
                value="Listen to music on a VC with an advanced queue system, features like pause and much more !",
                inline=False)
    embed6.add_field(name="__Join - `join`__",
                    value="Makes the bot join your VC\n**Usage**: `t join`",
                    inline=True)
    embed6.add_field(name="__Pause - `pause`__",
                    value="Pauses the current song\n**Usage**: `t pause`",
                    inline=True)
    embed6.add_field(name="__Resume - `resume`__",
                    value="Resumes the paused song\n**Usage**: `t resume`",
                    inline=True)
    embed6.add_field(name="__Stop - `stop`__",
                    value="Stops the current playing song and clears the queue\n**Usage**: `t stop`",
                    inline=True)
    embed6.add_field(name="__Leave - `leave`__",
                    value="Makes the bot leave the VC it is connected\n**Usage**: `t leave`",
                    inline=True)
    embed6.add_field(name="__Play - `play`__",
                    value="PLay a song with this command\n**Usage**: `t play SongNameHere` or `t play YoutubeLinkHere`",
                    inline=True)
    embed6.add_field(name="__Skip - `skip`__",
                    value="Skips to the next track based on a vote system.\n**Usage**: `t skip`",
                    inline=True)
    embed6.add_field(name="__Force Skip - `forceskip`__",
                    value="Forcefully skips to the next track.\n**Aliases: `fs`**\n**Usage**: `t skip`",
                    inline=True)
    embed6.add_field(name="__Now Playing - `now`__",
                    value="Shows the currently playing song\n**Aliases: `current`, `nowplaying`**\n**Usage**: `t now`",
                    inline=True)
    embed6.add_field(name="__Volume - `volume`__",
                    value="Changes the volume of the player (if supported by track)\n**Aliases: `vol`**\n**Usage**: `t volume <volume (1-100)>`",
                    inline=True)
    embed6.add_field(name="__Queue - `queue`__",
                    value="View the current song queue of the server.\n**Usage**: `t queue <page number (default-1)`",
                    inline=True)

  
    buttons = {"embed1":embed1, "embed2":embed2,"embed3":embed3,"embed4":embed4,"embed5":embed5,"embed6":embed6}
    
    while True:
      res = await client.wait_for("button_click")
      if res.channel is not ctx.channel:
        return
      if res.channel==ctx.channel:
        response = buttons.get(res.component.id)
        if response is None:
          await ctx.send("Something went wrong. Buttons are at testing stage in this bot. We apologise for the inconvenience. Please head over to our support server for any assistance. Thanks!")
        else:
          await mes.edit(embed=response)
          await res.respond(
            type=InteractionType.UpdateMessage,
            content="\u200b")

    


@client.command()
async def modules(ctx):
    embed = discord.Embed(
        title="Available Modules",
        description=
        "Check the command list see how to enable or disable modules.",
        color=0x1a53ff)
    embed.set_author(name="Warpy Bot")
    embed.add_field(name="| Utility Modules |",
                    value="Helpful Modules for Utilities",
                    inline=False)
    embed.add_field(
        name="Time Converter Module",
        value=
        "*ID-*module1 |  Use this module to convert time across various time zones in your server . Useful in cases where servers host members from different countries. Module ON by default.",
        inline=False)
    embed.add_field(
        name="Lottery Module",
        value=
        "*ID-*module2 |  Use this module to hold lotteries and giveaways on your server ! Easy to use, fully automated system. Module ON by default.",
        inline=False)
    embed.add_field(name="| Anime & Movie Related Fun Modules |",
                    value="Fun Command packs related to anime or movies ",
                    inline=False)
    embed.add_field(
        name="Demon Slayer Module",
        value=
        "*ID-*module3 | Use this fun module and immerse yourself in a realistic demon slayer anime world.",
        inline=True)
    embed.set_footer(text="Viewing Page 1 of 3")
    await ctx.send(embed=embed)


@client.command()
async def info(ctx, rg=None, page=1):
    arr = [
        "demon slayer", "ds", "demon slayer game", "demon slayer minigame",
        "demon"
    ]
    if rg == None:

        await ctx.send(
            "You need to mention something to see more info on like this: `t info <feature_of_choice>`\nInfo Available for:\n:one: Demon Slayer Game - `t info ds <page number 1/2/3>`\n:two: Moderation Tools - `t info modtools`"
        )
    elif rg.lower() in arr:
        if page == 1:
            embed = discord.Embed(
                title="Demon Slayer Game",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
                color=0xf61e1e)
            embed.set_author(
                name="Information Desk",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
            )
            embed.add_field(
                name="What Is It ?",
                value=
                "A full fledged fun Demon Slayer themed discord game !\nMine ores, forge things, buy and sell things, open loot crates, go on slayer corps missions, collect epic moves and much more !!",
                inline=False)
            embed.add_field(
                name="Currency, Wallet and Bag",
                value=
                "Two currencies are in use : \n:one: :yen: Cash\nThe most frequently used currency. Can only be earned from selling items, missions, daily rewards and loot crates !\n:two: <:slayersgem:785765850862059520> Slayer's Gems\nThe rarer and hard to come across, valuable currency. Can only be earned from missions, and Rare or Higher Rarity Loot Crates !\n\n**Wallet Balance**\nCheck your current balance using `t balance` (Aliases: `t bal`)\n\n**Bag & Inventory**\nView your owned items using `t bag` !",
                inline=True)

            embed.add_field(
                name="Mines",
                value=
                "There are 6 mines, ranging from `mine1` to `mine6`. Each mine is unlocked upon reaching a certain level.\nTo view how rewards change, visit `t info minerewards`\nTo run the command type `t mine<mine number>`. ex: `t mine2`, `t mine6`",
                inline=False)
            embed.set_footer(text="Viewing Page 1 of 3")
            await ctx.send(embed=embed)
        elif page == 2:
            embed = discord.Embed(
                title="Demon Slayer Game",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
                color=0xf61e1e)
            embed.set_author(
                name="Information Desk",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
            )
            embed.add_field(
                name="Wisteria Market :shopping_bags:",
                value=
                "**Wisteria Shop** - `t wistshop` (Aliases : `t ws`)\n Buy and sell materials, goods and more here !\nFor more info on a particular item, run : `t wistshop <item id>` \n(Item ID mentioned below each item's name)\n\n**Loot Crate Shop :gift:** - `t crateshop` (Aliases : `t cs`)\nBuy Loot Crates Here !\nTo open a crate, run : `t crate <crate id>`. ex: `t crate rare`\n\n**Buying And Selling**\nBuy items / crates from the Wisteria Market by `t buy <item / crate id> <quantity (defaults to 1)>` using :yen: (Cash) or <:slayersgem:785765850862059520> Slayer's Gems\n\nSell items by `t sell <item id> <quantity (defaults to 1)>`. Sell prices are roughly 50% of the buy price. For precise amounts, view the item info !\n*Note:* Loot Crates cannot be sold",
                inline=False)
            embed.add_field(
                name="Forging Items :hammer_pick:",
                value=
                "Forge Items and Equipment here !\n\nView the Forging Menu for forge-able items and materials required at `t forge`\nForge something by `t forge < item id> <quantity (defaults to 1)>`\n\n*Note:* There are limits to how many of an item can be forged !",
                inline=True)

            embed.set_footer(text="Viewing Page 2 of 3")
            await ctx.send(embed=embed)
        elif page == 3:
            embed = discord.Embed(
                title="Demon Slayer Game",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
                color=0xf61e1e)
            embed.set_author(
                name="Information Desk",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
            )
            embed.add_field(
                name="Missions (COMING SOON)",
                value=
                "Play missions assigned by the Demon Slayer Corps Here !\n\nTo view the missions menu, run : `t missions`\n\nTo view mission details, rewards and more info, run : `t missions view <mission number>`\nTo accept a mission, run: `command work in progress`",
                inline=True)
            embed.set_footer(text="Viewing Page 3 of 3")
            await ctx.send(embed=embed)
        else:
            pass
    elif rg.lower() == "modtools":
        embed = discord.Embed(
            title="Moderation Tools",
            url=
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
            color=0x55dda2)
        embed.set_author(
            name="Information Desk",
            url=
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
        )
        embed.add_field(
            name="Purge",
            value=
            "Clears messages in a channel.\n__Permissions Required__: `Manage Messages`",
            inline=True)
        embed.add_field(
            name="Kick",
            value=
            "Kicks a member from the server.\n__Required Permissions__: `Kick Members`",
            inline=True)
        embed.add_field(
            name="Ban",
            value=
            "Bans a member from the server.\n__Permissions Required__: `Ban Members`",
            inline=True)
        embed.add_field(
            name="Unban",
            value=
            "Unbans a member from the server.\n__Permissions Required__: `Ban Members`",
            inline=True)
        embed.add_field(
            name="Lock/Unlock",
            value=
            "Locks or Unlocks a channel in the server.\n__Permissions Required__: `Manage Channels`",
            inline=True)
        embed.add_field(
            name="Mute / Unmute",
            value=
            "Mutes/Unmutes a member from the server.\n__Required Permissions__: `Manage Channels` `Manage Roles` `Manage Messages`",
            inline=True)

        await ctx.send(embed=embed)

    elif rg.lower() == "minerewards":
        embed = discord.Embed(
            title="Mine Rewards",
            url=
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
            color=0x55dda2)
        embed.set_author(
            name="Information Desk",
            url=
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
        )
        embed.add_field(
            name="Mine 1 ",
            value=
            "**Unlocked At** : `Level 0`\n**Item Quantity Rates **: 1 Item - 80% |    2 Items - 15% |  3 Items - 5%\n**Mine Rewards **: Scarlet Crimson Iron Ore Fragment, Scarlet Crimson Iron Dust, Coal, Ancient Crystal Shards  ",
            inline=False)
        embed.add_field(
            name="Mine 2",
            value=
            "**Unlocked At** : `Level 3`\n**Item Quantity Rates **: 1 Item - 80% |    2 Items - 15% |  3 Items - 5%\n**Mine Rewards **: Scarlet Crimson Iron Ore Fragment, Scarlet Crimson Iron Dust, Coal, Ancient Crystal Shards  ",
            inline=False)
        embed.add_field(
            name="Mine 3",
            value=
            "**Unlocked At** : `Level 5`\n**Item Quantity Rates **: 1 Item - 60% |    2 Items - 30% |  3 Items - 10%\n**Mine Rewards **: Scarlet Crimson Iron Ore Fragment, Scarlet Crimson Iron Dust, Scarlet Crimson Iron Sand,  Coal, Ancient Crystal Shards  ",
            inline=False)
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(
            name="Mine 4",
            value=
            "**Unlocked At** : `Level 8`\n**Item Quantity Rates **: 1 Item - 50% |    2 Items - 40% |  3 Items - 10%\n**Mine Rewards **: Scarlet Crimson Iron Ore Fragment, Scarlet Crimson Iron Dust, Scarlet Crimson Iron Sand Coal, Ancient Crystal Shards  ",
            inline=False)
        embed.add_field(
            name="Mine 5",
            value=
            "**Unlocked At** : `Level 10`\n**Item Quantity Rates **: 1 Item - 35% |    2 Items - 45% |  3 Items - 20%\n**Mine Rewards **: Scarlet Crimson Iron Ore Fragment, Scarlet Crimson Iron Dust, Scarlet Crimson Iron Sand Coal, Ancient Crystal Shards  ",
            inline=False)
        embed.add_field(
            name="Mine 6",
            value=
            "**Unlocked At** : `Level 13`\n**Item Quantity Rates **: 1 Item - 25% |    2 Items - 50% |  3 Items - 25%\n**Mine Rewards **: Scarlet Crimson Iron Ore Fragment, Scarlet Crimson Iron Dust, Scarlet Crimson Iron Sand Coal, Ancient Crystal Shards  ",
            inline=True)
        embed.set_footer(
            text=
            "Please note that the bot rolls whether you get any rewards first. If it happens to not land on that, you will get nothing"
        )
        await ctx.send(embed=embed)


#time module
@client.command()
async def mytime(ctx):
    await ctx.send(datetime.datetime.now())


@client.command()
async def timein(ctx):
    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    await ctx.send("Time in NY is:")
    await ctx.send(datetime_NY.strftime("%H:%M:%S"))


@client.command()
async def uaetoist(ctx, a: int, b: int):
    await ctx.send('The time in India is')
    if b + 30 >= 60:
        await ctx.send(a + 2)
        await ctx.send((b + 30) - 60)
    elif a == 12:
        await ctx.send('Command Work in progress')
    else:
        await ctx.send((a + 1), (b + 30))
        await ctx.send(b + 30)




#lottery module


@client.command(aliases=['giveaway', 'ga'])
@commands.guild_only()
async def lottery(ctx, time: float, unit: str, wi: str, *, arg):
    channel = ctx.message.channel.id
    sponsor = ctx.author.mention
    if unit == "m":
        time1 = time * 60
    elif unit == "h":
        time1 = time * 3600
    elif unit == "d":
        time1 = time * 3600 * 24
    now = datetime.datetime.utcnow() + datetime.timedelta(seconds=(time1))
    embnow = datetime.datetime.utcnow()
    embno = embnow.strftime('%d')
    newnow = now.strftime('%Y/%m/%d  %H:%M:%S')

    tomtime = datetime.datetime.utcnow() + datetime.timedelta(seconds=(86400))
    embno1 = now.strftime('%d')
    embno2 = tomtime.strftime('%d')
    sameday = now.strftime('%H:%M:%S')

    prize = arg
    embed = discord.Embed(title="Ongoing Giveaway  :tada:",
                          timestamp=datetime.datetime.utcnow(),
                          color=0xf78708)

    embed.add_field(name="Sponsored By ", value=str(sponsor), inline=True)
    embed.add_field(name="Giveaway Prize ", value=" " + str(arg) + " ", inline=True)
    
    global gawunit69
    if unit == "m":
        gawunit69="Minutes"
    elif unit == "h":
      gawunit69="Hours"
       
    elif unit == "d":
        gawunit69="Days"
    global gaw69
    if wi == "1w":
        gaw69 = 1
    elif wi == "2w":
        gaw69 = 2
    elif wi == "3w":
        gaw69 = 3

    
    if embno == embno1:
        embed.add_field(
            name=f"React with :moneybag: __within {str(time)} {gawunit69}__ to join the giveaway.\n\nGiveaway ends **Today at " + str(sameday) + " UTC (GMT)**",
            value=
            "For your time zone, visit [here !](https://en.wikipedia.org/wiki/List_of_time_zones_by_country)",
            inline=False)
    elif (int(embno) + 1) == int(embno2):
        embed.add_field(
            name="Giveaway ends **Tomorrow at " + str(sameday) +
            " UTC (GMT)**",
            value=
            "For your time zone, visit [here !](https://en.wikipedia.org/wiki/List_of_time_zones_by_country)",
            inline=False)
    elif (int(embno) + 2) == int(embno2):
        embed.add_field(
            name="Giveaway ends **Day After Tomorrow at " + str(sameday) +
            " UTC (GMT)**",
            value=
            "For your time zone, visit [here !](https://en.wikipedia.org/wiki/List_of_time_zones_by_country)",
            inline=False)

    embed.set_footer(text=f"{gaw69} Winners | Giveaway Started")
    await ctx.message.delete()
    my_msg = await ctx.send(embed=embed)
    await my_msg.add_reaction("\U0001F4B0")
    await asyncio.sleep(time1)
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    x = len(users)
    if x < 1:
        pp = abc = new_msg.jump_url
        emb = discord.Embed(color=0xed0707)
        emb.set_author(name="This Giveaway Has Ended ⏰")
        emb.add_field(name="Sponsored By ", value=str(sponsor), inline=True)
        emb.add_field(name="Prize ", value="" + str(arg) + " ", inline=True)
        emb.add_field(name="Winner ",
                      value="No winners :c",
                      inline=True)
        emb.add_field(
            name="Giveaway ended at " + str(newnow) + " UTC (GMT)",
            value=f"{x} people entered this giveaway.",
            inline=False)

        
        await my_msg.edit(embed=emb)
        e = discord.Embed(color=0xed0707)
      
        e.add_field(
            name="A Giveaway Has Ended ⏰",
            value="No one joined [this]({}) giveaway within the time limit.".
            format(pp),
            inline=False)
        await ctx.send(embed=e)
    else:
        prize = arg
        abc = new_msg.jump_url

        embe = discord.Embed(color=0x07ed22)
        embe.set_author(name="This Giveaway Has Ended 🎉⏰")
        embe.add_field(name="Sponsored By ", value=str(sponsor), inline=True)
        embe.add_field(name="Giveaway Prize ", value=" " + str(arg) + " ", inline=True)
        if wi == "1w":
            winnero = random.choice(users)
            embe.add_field(name="Winner ",
                           value=str(winnero.mention),
                           inline=True)
            emb = discord.Embed(color=0x07ed22)
            emb.add_field(name="Giveaway Winner Notice 💰 :tada:",
                          value=str(winnero.mention) +
                          " won **[this]({})** giveaway.".format(abc),
                          inline=False)
            
            ping = f"{winnero.mention}, please contact {sponsor} to claim your prize.\nTo reroll for a new winner, run `t reroll #{ctx.channel} {my_msg.id}`"
                                  
            await ctx.send(ping, embed=emb)
            em = discord.Embed(color=0x07ed22)
            em.add_field(
                name="Giveaway Winner Notice 💰 :tada:",
                value=  
                f"You won [this]({abc}) giveaway \nPlease contact {sponsor} in **{ctx.guild.name}** to claim your prize !",
                inline=False)

            await winnero.send(embed=em)

        elif wi == "2w":
            winner1 = random.choice(users)

            if len(users) >= 2:
                users.pop(users.index(winner1))
                winner2 = random.choice(users)
                emb1 = discord.Embed(color=0x07ed22)
                emb1.add_field(
                    name="Giveaway Winner Notice 💰 :tada:",
                    value=
                    f"{winner1.mention} and {winner2.mention} won [this]({abc}) giveaway",
                    inline=False)
                ping = f"{winner1.mention}, {winner2.mention} please contact {sponsor} to claim your prize."
                
                await ctx.send(ping, embed=emb1)
                embe.add_field(name="Winners :",
                               value=str(winner1.mention) + ", " +
                               str(winner2.mention),
                               inline=True)

                em = discord.Embed(color=0x07ed22)
                em.add_field(
                    name="Giveaway Winner Notice 💰 :tada:",
                    value=
                    f"You won [this]({abc}) giveaway \nPlease contact {sponsor} in **{ctx.guild.name}** to claim your prize !",
                    inline=False)

                await winner1.send(embed=em)
                await winner2.send(embed=em)
            else:
                second = "2nd"
                embe.add_field(name="Winners :",
                               value=str(winner1.mention) + f", {second} winner N/A",
                               inline=True)
                emb2 = discord.Embed(color=0x07ed22)
                emb2.add_field(
                    name="Giveaway Winner Notice 💰 :tada:",
                    value=
                    f"{winner1.mention} won [this]({abc}) giveaway.",
                    inline=False)
                
                ping = f"{winner1.mention}, please contact {sponsor} to claim your prize.\n The {second} winner couldn\'t be chosen as there weren\'t enough people who joined"
                em1 = discord.Embed(color=0x07ed22)
                em1.add_field(
                    name="Giveaway Winner Notice 💰 :tada:",
                    value=
                    f"You won [this]({abc}) giveaway \nPlease contact {sponsor} in **{ctx.guild.name}** to claim your prize !",
                    inline=False)

                await ctx.send(ping, embed=emb2)
                await winner1.send(embed=em1)

        elif wi == "3w":
            winner1 = random.choice(users)
            users.pop(users.index(winner1))
            winner2 = random.choice(users)
            users.pop(users.index(winner2))
            if len(users) >= 2:

                embe.add_field(name="Winners :",
                               value=str(winner1.mention) + ", " +
                               str(winner2.mention),
                               inline=True)
            elif len(users) >= 3:
                winner3 = random.choice(users)
                embe.add_field(name="Winner :",
                               value=str(winner1.mention) + ", " +
                               str(winner2.mention),
                               inline=True)

        embe.add_field(
            name="Giveaway ended at " + str(newnow) + " UTC (GMT)",
            value=
            "For your time zone, visit [here !](https://en.wikipedia.org/wiki/List_of_time_zones_by_country)",
            inline=False)
        await my_msg.edit(embed=embe)


@client.command()
async def reroll(ctx, channel: discord.TextChannel, id_: int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The Giveaway Embed ID is incorrect !")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}.!"
                       )


#demon slayer module


#money and economy
@client.command()
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
      if 'lvl' not in users[str(user.id)].keys():
        res=await levels(user)
        users[str(user.id)]["lvl"] =int(res[0])
      else:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["xp"] = 0
        users[str(user.id)]["twostar"] = 0
        users[str(user.id)]["threestar"] = 0
        users[str(user.id)]["fourstar"] = 0
        users[str(user.id)]["fivestar"] = 0
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["coal"] = 0
        users[str(user.id)]["ore"] = 0
        users[str(user.id)]["fragment"] = 0
        users[str(user.id)]["chunk"] = 0
        users[str(user.id)]["dust"] = 0
        users[str(user.id)]["sand"] = 0
        users[str(user.id)]["nichirin"] = 0
        users[str(user.id)]["common"] = 0
        users[str(user.id)]["rare"] = 0
        users[str(user.id)]["epic"] = 0
        users[str(user.id)]["legendary"] = 0
        users[str(user.id)]["mystical"] = 0
        users[str(user.id)]["crystal"] = 0
        users[str(user.id)]["shard"] = 0
        users[str(user.id)]["blade"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def open_moves(user):
    users = await get_moves_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["swordlvl"] = 0
        users[str(user.id)]["engaged"] = 0
        users[str(user.id)]["TCform1"] = 0
        users[str(user.id)]["Wform1"] = 0
        users[str(user.id)]["Wform2"] = 0
        users[str(user.id)]["Wform3"] = 0
        users[str(user.id)]["Wform4"] = 0
        users[str(user.id)]["Wform5"] = 0
        users[str(user.id)]["Wform6"] = 0
        users[str(user.id)]["Wform7"] = 0
        users[str(user.id)]["Wform8"] = 0
        users[str(user.id)]["Wform8"] = 0
        users[str(user.id)]["Wform9"] = 0
        users[str(user.id)]["Wform10"] = 0
        users[str(user.id)]["Wform11"] = 0
        users[str(user.id)]["Tform1.1"] = 0
        users[str(user.id)]["Tform1.2"] = 0
        users[str(user.id)]["Tform2"] = 0
        users[str(user.id)]["Tform3"] = 0
        users[str(user.id)]["Tform4"] = 0
        users[str(user.id)]["Tform5"] = 0
        users[str(user.id)]["Tform6"] = 0
        users[str(user.id)]["Tform7"] = 0
        users[str(user.id)]["Tform8"] = 0
        users[str(user.id)]["Fform1"] = 0
        users[str(user.id)]["Fform2"] = 0
        users[str(user.id)]["Fform3"] = 0
        users[str(user.id)]["Fform4"] = 0
        users[str(user.id)]["Fform5"] = 0
        users[str(user.id)]["Fform9"] = 0

    with open("moves.json", "w") as f:
        json.dump(users, f)
    return True

async def open_newitems(user):
  users = await get_newitems_data()
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["vial"] = 0
    users[str(user.id)]["jar"] = 0
    users[str(user.id)]["rustykey"] = 0
    users[str(user.id)]["keybp"] = 0
    users[str(user.id)]["key"] = 0
    users[str(user.id)]["fiveash"] = 0
    users[str(user.id)]["artifactcrate"] = 0
    users[str(user.id)]["votecrate"] = 0
    users[str(user.id)]["fiveash"] = 0
    users[str(user.id)]["fourash"] = 0
    users[str(user.id)]["threeash"] = 0
    users[str(user.id)]["twoash"] = 0
    users[str(user.id)]["upgrade1"] = 0
    users[str(user.id)]["upgrade2"] = 0
    users[str(user.id)]["upgrade3"] = 0
    users[str(user.id)]["upgrade4"] = 0
    users[str(user.id)]["upgrade5"] = 0

  with open("newitems.json", "w") as f:
        json.dump(users, f)
  return True


async def open_cd(user):
  users = await get_cd_data()
  if str(user.id) in users:
        return False
  else:
        users[str(user.id)] = {}
        users[str(user.id)]["premium"] = 0

  with open("cd.json", "w") as f:
      json.dump(users, f)
  return True

async def levels(user):
    
    users = await get_bank_data()
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    global uslvl
    global lv
    global lim
    if users[str(user.id)]["xp"] in range(0, 99):
        uslvl = "0"
        lv = 100 - users[str(user.id)]["xp"]
        lim = 100
        users[str(user.id)]["lvl"] = 0
    elif users[str(user.id)]["xp"] in range(100, 249):
        uslvl = "1"
        lv = 250 - users[str(user.id)]["xp"]
        lim = 250
        users[str(user.id)]["lvl"] = 1
    elif users[str(user.id)]["xp"] in range(250, 499):
        uslvl = "2"
        lv = 500 - users[str(user.id)]["xp"]
        lim = 500
        users[str(user.id)]["lvl"] = 2
    elif users[str(user.id)]["xp"] in range(500, 699):
        uslvl = "3"
        lv = 700 - users[str(user.id)]["xp"]
        lim = 700
        users[str(user.id)]["lvl"] = 3
    elif users[str(user.id)]["xp"] in range(700, 949):
        uslvl = "4"
        lv = 950 - users[str(user.id)]["xp"]
        lim = 950
        users[str(user.id)]["lvl"] = 4
    elif users[str(user.id)]["xp"] in range(950, 1199):
        uslvl = "5"
        lv = 1200 - users[str(user.id)]["xp"]
        lim = 1200
        users[str(user.id)]["lvl"] = 5
    elif users[str(user.id)]["xp"] in range(1200, 1399):
        uslvl = "6"
        lv = 1400 - users[str(user.id)]["xp"]
        lim = 1400
        users[str(user.id)]["lvl"] = 6
    elif users[str(user.id)]["xp"] in range(1400, 1699):
        uslvl = "7"
        lv = 1700 - users[str(user.id)]["xp"]
        lim = 1700
        users[str(user.id)]["lvl"] = 7
    elif users[str(user.id)]["xp"] in range(1700, 1999):
        uslvl = "8"
        lv = 2000 - users[str(user.id)]["xp"]
        lim = 2000
        users[str(user.id)]["lvl"] = 8
    elif users[str(user.id)]["xp"] in range(2000, 2199):
        uslvl = "9"
        lv = 2200 - users[str(user.id)]["xp"]
        lim = 2200
        users[str(user.id)]["lvl"] = 9
    elif users[str(user.id)]["xp"] in range(2200, 2399):
        uslvl = "10"
        lv = 2400 - users[str(user.id)]["xp"]
        lim = 2400
        users[str(user.id)]["lvl"] = 10
    elif users[str(user.id)]["xp"] in range(2400, 2599):
        uslvl = "11"
        lv = 2600 - users[str(user.id)]["xp"]
        lim = 2600
        users[str(user.id)]["lvl"] = 11
    elif users[str(user.id)]["xp"] in range(2600, 2899):
        uslvl = "12"
        lv = 2900 - users[str(user.id)]["xp"]
        lim = 2900
        users[str(user.id)]["lvl"] = 12
    elif users[str(user.id)]["xp"] in range(2900, 3099):
        uslvl = "13"
        lv = 3100 - users[str(user.id)]["xp"]
        lim = 3100
        users[str(user.id)]["lvl"] = 13
    elif users[str(user.id)]["xp"] in range(3100, 3499):
        uslvl = "14"
        lv = 3500 - users[str(user.id)]["xp"]
        lim = 3500
        users[str(user.id)]["lvl"] = 14
    elif users[str(user.id)]["xp"] in range(3500, 3799):
        uslvl = "15"
        lv = 3800 - users[str(user.id)]["xp"]
        lim = 3800
        users[str(user.id)]["lvl"] = 15
    elif users[str(user.id)]["xp"] in range(3800, 4099):
        uslvl = "16"
        lv = 4100 - users[str(user.id)]["xp"]
        lim = 4100
        users[str(user.id)]["lvl"] = 16
    elif users[str(user.id)]["xp"] in range(4100, 4399):
        uslvl = "17"
        lv = 4400 - users[str(user.id)]["xp"]
        lim = 4400
        users[str(user.id)]["lvl"] = 17
    elif users[str(user.id)]["xp"] in range(4400, 4699):
        uslvl = "18"
        lv = 4700 - users[str(user.id)]["xp"]
        lim = 4700
        users[str(user.id)]["lvl"] = 18
    elif users[str(user.id)]["xp"] in range(4700, 4999):
        uslvl = "19"
        lv = 5000 - users[str(user.id)]["xp"]
        lim = 5000
        users[str(user.id)]["lvl"] = 19
    elif users[str(user.id)]["xp"] in range(5000, 5299):
        uslvl = "20"
        lv = 5300 - users[str(user.id)]["xp"]
        lim = 5300
        users[str(user.id)]["lvl"] = 20
    elif users[str(user.id)]["xp"] in range(5300, 5599):
        uslvl = "21"
        lv = 5600 - users[str(user.id)]["xp"]
        lim = 5600
        users[str(user.id)]["lvl"] = 21
    elif users[str(user.id)]["xp"] in range(5600, 5899):
        uslvl = "22"
        lv = 5900 - users[str(user.id)]["xp"]
        lim = 5900
        users[str(user.id)]["lvl"] = 22
    elif users[str(user.id)]["xp"] in range(5900, 6199):
        uslvl = "23"
        lv = 6200 - users[str(user.id)]["xp"]
        lim = 6200
        users[str(user.id)]["lvl"] = 23
    elif users[str(user.id)]["xp"] in range(6200, 6499):
        uslvl = "24"
        lv = 6500 - users[str(user.id)]["xp"]
        lim = 6500
        users[str(user.id)]["lvl"] = 24
    elif users[str(user.id)]["xp"] in range(6500, 6799):
        uslvl = "25"
        lv = 6800 - users[str(user.id)]["xp"]
        lim = 6800
        users[str(user.id)]["lvl"] = 25
    elif users[str(user.id)]["xp"] in range(6800, 7099):
        uslvl = "26"
        lv = 7100 - users[str(user.id)]["xp"]
        lim = 7100
        users[str(user.id)]["lvl"] = 26
    elif users[str(user.id)]["xp"] in range(7100, 7399):
        uslvl = "27"
        lv = 7400 - users[str(user.id)]["xp"]
        lim = 7400
        users[str(user.id)]["lvl"] = 27
    elif users[str(user.id)]["xp"] in range(7400, 7699):
        uslvl = "28"
        lv = 7700 - users[str(user.id)]["xp"]
        lim = 7700
        users[str(user.id)]["lvl"] = 28
    elif users[str(user.id)]["xp"] in range(7700, 8099):
        uslvl = "29"
        lv = 8100 - users[str(user.id)]["xp"]
        lim = 8100
        users[str(user.id)]["lvl"] = 29
    elif users[str(user.id)]["xp"] in range(8100, 8399):
        uslvl = "30"
        lv = 8400 - users[str(user.id)]["xp"]
        lim = 8400
        users[str(user.id)]["lvl"] = 30
    elif users[str(user.id)]["xp"] in range(8400, 8699):
        uslvl = "31"
        lv = 8700 - users[str(user.id)]["xp"]
        lim = 8700
        users[str(user.id)]["lvl"] = 31
    elif users[str(user.id)]["xp"] in range(8700, 8999):
        uslvl = "32"
        lv = 9000 - users[str(user.id)]["xp"]
        lim = 9000
        users[str(user.id)]["lvl"] = 32
    elif users[str(user.id)]["xp"] in range(9000, 9299):
        uslvl = "33"
        lv = 9300 - users[str(user.id)]["xp"]
        lim = 9300
        users[str(user.id)]["lvl"] = 33
    elif users[str(user.id)]["xp"] in range(9300, 9599):
        uslvl = "34"
        lv = 9600 - users[str(user.id)]["xp"]
        lim = 9600
        users[str(user.id)]["lvl"] = 34
    elif users[str(user.id)]["xp"] in range(9600, 9899):
        uslvl = "35"
        lv = 9900 - users[str(user.id)]["xp"]
        lim = 9900
        users[str(user.id)]["lvl"] = 35
    elif users[str(user.id)]["xp"] in range(9900, 10199):
        uslvl = "36"
        lv = 10200 - users[str(user.id)]["xp"]
        lim = 10200
        users[str(user.id)]["lvl"] = 36
    elif users[str(user.id)]["xp"] in range(10200, 10499):
        uslvl = "37"
        lv = 10500 - users[str(user.id)]["xp"]
        lim = 10500
        users[str(user.id)]["lvl"] = 37
    elif users[str(user.id)]["xp"] in range(10500, 10799):
        uslvl = "38"
        lv = 10800 - users[str(user.id)]["xp"]
        lim = 10800
        users[str(user.id)]["lvl"] = 38
    elif users[str(user.id)]["xp"] in range(10800, 11099):
        uslvl = "39"
        lv = 11100 - users[str(user.id)]["xp"]
        lim = 11100
        users[str(user.id)]["lvl"] = 39
    elif users[str(user.id)]["xp"] in range(11100, 11399):
        uslvl = "40"
        lv = 11400 - users[str(user.id)]["xp"]
        lim = 11400
        users[str(user.id)]["lvl"] = 40
    
    elif users[str(user.id)]["xp"] in range(11400, 11799):
        uslvl = "41"
        lv = 11800 - users[str(user.id)]["xp"]
        lim = 11800
        users[str(user.id)]["lvl"] = 41
    
    elif users[str(user.id)]["xp"] in range(11800, 12199):
        uslvl = "42"
        lv = 12200 - users[str(user.id)]["xp"]
        lim = 12200
        users[str(user.id)]["lvl"] = 42
    elif users[str(user.id)]["xp"] in range(12200, 12599):
        uslvl = "43"
        lv = 12600 - users[str(user.id)]["xp"]
        lim = 12600
        users[str(user.id)]["lvl"] = 43
    elif users[str(user.id)]["xp"] in range(12600, 13099):
        uslvl = "44"
        lv = 13100 - users[str(user.id)]["xp"]
        lim = 13100
        users[str(user.id)]["lvl"] = 44
    
    elif users[str(user.id)]["xp"] in range(13100, 13599):
        uslvl = "45"
        lv = 13600 - users[str(user.id)]["xp"]
        lim = 13600
        users[str(user.id)]["lvl"] = 45
    elif users[str(user.id)]["xp"] in range(13600, 13999):
        uslvl = "46"
        lv = 14000 - users[str(user.id)]["xp"]
        lim = 14000
        users[str(user.id)]["lvl"] = 46
    elif users[str(user.id)]["xp"] in range(14000, 13399):
        uslvl = "47"
        lv = 14400 - users[str(user.id)]["xp"]
        lim = 14400
        users[str(user.id)]["lvl"] = 47
    elif users[str(user.id)]["xp"] in range(14400, 14799):
        uslvl = "48"
        lv = 14800 - users[str(user.id)]["xp"]
        lim = 14800
        users[str(user.id)]["lvl"] = 48
    elif users[str(user.id)]["xp"] in range(14800, 15199):
        uslvl = "49"
        lv = 15200 - users[str(user.id)]["xp"]
        lim = 15200
        users[str(user.id)]["lvl"] = 49
    elif users[str(user.id)]["xp"] in range(15200, 15599):
        uslvl = "50"
        lv = 15600 - users[str(user.id)]["xp"]
        lim = 15600
        users[str(user.id)]["lvl"] = 50
    elif users[str(user.id)]["xp"] in range(15600, 15999):
        uslvl = "51"
        lv = 16000 - users[str(user.id)]["xp"]
        lim = 16000
        users[str(user.id)]["lvl"] = 51
    elif users[str(user.id)]["xp"] in range(16000, 16399):
        uslvl = "52"
        lv = 16400 - users[str(user.id)]["xp"]
        lim = 16400
        users[str(user.id)]["lvl"] = 52
    elif users[str(user.id)]["xp"] in range(16400, 16799):
        uslvl = "53"
        lv = 16800 - users[str(user.id)]["xp"]
        lim = 16800
        users[str(user.id)]["lvl"] = 53
    elif users[str(user.id)]["xp"] in range(16800, 17199):
        uslvl = "54"
        lv = 17200 - users[str(user.id)]["xp"]
        lim = 17200
        users[str(user.id)]["lvl"] = 54
    elif users[str(user.id)]["xp"] in range(17200, 17599):
        uslvl = "55"
        lv = 17600 - users[str(user.id)]["xp"]
        lim = 17600
        users[str(user.id)]["lvl"] = 55
    elif users[str(user.id)]["xp"] in range(17600, 17999):
        uslvl = "56"
        lv = 18000 - users[str(user.id)]["xp"]
        lim = 18000
        users[str(user.id)]["lvl"] = 56
    elif users[str(user.id)]["xp"] in range(18000, 18399):
        uslvl = "57"
        lv = 18400 - users[str(user.id)]["xp"]
        lim = 18400
        users[str(user.id)]["lvl"] = 57
    elif users[str(user.id)]["xp"] in range(18400, 18799):
        uslvl = "58"
        lv = 18800 - users[str(user.id)]["xp"]
        lim = 18800
        users[str(user.id)]["lvl"] = 58
    elif users[str(user.id)]["xp"] in range(18800, 19199):
        uslvl = "59"
        lv = 19200 - users[str(user.id)]["xp"]
        lim = 19200
        users[str(user.id)]["lvl"] = 59
    elif users[str(user.id)]["xp"] in range(19200, 19599):
        uslvl = "60"
        lv = 19600 - users[str(user.id)]["xp"]
        lim = 19600
        users[str(user.id)]["lvl"] = 60
    elif users[str(user.id)]["xp"] in range(19600, 19999):
        uslvl = "61"
        lv = 20000 - users[str(user.id)]["xp"]
        lim = 20000
        users[str(user.id)]["lvl"] = 61
    elif users[str(user.id)]["xp"] in range(20000, 20399):
        uslvl = "62"
        lv = 20400 - users[str(user.id)]["xp"]
        lim = 20400
        users[str(user.id)]["lvl"] = 62
    elif users[str(user.id)]["xp"] in range(20400, 20799):
        uslvl = "63"
        lv = 20800 - users[str(user.id)]["xp"]
        lim = 20800
        users[str(user.id)]["lvl"] = 63
    elif users[str(user.id)]["xp"] in range(20800, 21199):
        uslvl = "64"
        lv = 21200 - users[str(user.id)]["xp"]
        lim = 21200
        users[str(user.id)]["lvl"] = 64
    elif users[str(user.id)]["xp"] in range(21200, 21599):
        uslvl = "65"
        lv = 21600 - users[str(user.id)]["xp"]
        lim = 21600
        users[str(user.id)]["lvl"] = 65
    elif users[str(user.id)]["xp"] in range(21600, 21999):
        uslvl = "66"
        lv = 22000 - users[str(user.id)]["xp"]
        lim = 22000
        users[str(user.id)]["lvl"] = 66
    elif users[str(user.id)]["xp"] in range(22000, 22399):
        uslvl = "67"
        lv = 22400 - users[str(user.id)]["xp"]
        lim = 22400
        users[str(user.id)]["lvl"] = 67
    elif users[str(user.id)]["xp"] in range(22400, 22799):
        uslvl = "68"
        lv = 22800 - users[str(user.id)]["xp"]
        lim = 22800
        users[str(user.id)]["lvl"] = 68
    elif users[str(user.id)]["xp"] in range(22800, 23199):
        uslvl = "68"
        lv = 23200 - users[str(user.id)]["xp"]
        lim = 23200
        users[str(user.id)]["lvl"] = 69
    elif users[str(user.id)]["xp"] in range(23200, 23599):
        uslvl = "70"
        lv = 23600 - users[str(user.id)]["xp"]
        lim = 23600
        users[str(user.id)]["lvl"] = 70
    elif users[str(user.id)]["xp"] in range(23600, 23999):
        uslvl = "71"
        lv = 24000 - users[str(user.id)]["xp"]
        lim = 24000
        users[str(user.id)]["lvl"] = 71
    elif users[str(user.id)]["xp"] in range(24000, 24399):
        uslvl = "72"
        lv = 24400 - users[str(user.id)]["xp"]
        lim = 24400
        users[str(user.id)]["lvl"] = 72
    elif users[str(user.id)]["xp"] in range(24400, 24799):
        uslvl = "73"
        lv = 24800 - users[str(user.id)]["xp"]
        lim = 24800
        users[str(user.id)]["lvl"] = 73
    elif users[str(user.id)]["xp"] in range(24800, 25199):
        uslvl = "74"
        lv = 25200 - users[str(user.id)]["xp"]
        lim = 25200
        users[str(user.id)]["lvl"] = 74
    elif users[str(user.id)]["xp"] in range(25200, 25599):
        uslvl = "75"
        lv = 25600 - users[str(user.id)]["xp"]
        lim = 25600
        users[str(user.id)]["lvl"] = 75
    else:
        uslvl = "100"
        lv = users[str(user.id)]["xp"]
        lim = users[str(user.id)]["xp"]
    
    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    return uslvl, lv, lim, users[str(user.id)]["xp"]


async def invitems(user):
    await open_account(user)
    users = await get_bank_data()
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    coal_amt = users[str(user.id)]["coal"]
    ore_amt = users[str(user.id)]["ore"]
    sand_amt = users[str(user.id)]["sand"]
    nichirin_amt = users[str(user.id)]["nichirin"]
    common_amt = users[str(user.id)]["common"]
    rare_amt = users[str(user.id)]["rare"]
    epic_amt = users[str(user.id)]["epic"]
    legendary_amt = users[str(user.id)]["legendary"]
    mystical_amt = users[str(user.id)]["mystical"]
    shard_amt = users[str(user.id)]["shard"]
    blade_amt = users[str(user.id)]["blade"]
    crystal_amt = users[str(user.id)]["crystal"]
    twoamt = users[str(user.id)]["twostar"]
    threeamt = users[str(user.id)]["threestar"]
    fouramt = users[str(user.id)]["fourstar"]
    fiveamt = users[str(user.id)]["fivestar"]
    return coal_amt, ore_amt, sand_amt, nichirin_amt, common_amt, rare_amt, epic_amt, legendary_amt, mystical_amt, shard_amt, blade_amt, crystal_amt, twoamt, threeamt, fouramt, fiveamt

async def dumpvial(amount, user):
  await open_newitems(user)
  with open("newitems.json", "r") as f:
        users = json.load(f)
  users[str(user.id)]["vial"] += amount
  with open("newitems.json", "w") as f:
        json.dump(users, f)

async def dumpjar(amount, user):
  await open_newitems(user)
  with open("newitems.json", "r") as f:
        users = json.load(f)
  users[str(user.id)]["jar"] += amount
  with open("newitems.json", "w") as f:
        json.dump(users, f)

async def dumpbp(amount, user):
  await open_newitems(user)
  with open("newitems.json", "r") as f:
        users = json.load(f)
  users[str(user.id)]["keybp"] += amount
  with open("newitems.json", "w") as f:
        json.dump(users, f)

async def dump(amount, user):
  await open_newitems(user)
  with open("newitems.json", "r") as f:
        users = json.load(f)
  users[str(user.id)]["vial"] += amount
  with open("newitems.json", "w") as f:
        json.dump(users, f)

#0- coal  1-ore 2-sand 3-nichirin 4-common 5-rare 6-epic 7-legendary 8-mystical 9-shard 10-blade 11-crystal 12-2star 13-3star 14-4star 15-5star


async def get_moves_data():
    with open("moves.json", "r") as f:
        users = json.load(f)
    return users

async def get_newitems_data():
    with open("newitems.json", "r") as f:
        users = json.load(f)
    return users 

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

async def get_cd_data():
  with open("cd.json", "r") as f:
        users = json.load(f)
  return users

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    balance = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return balance



@client.command(aliases=["bal"])
async def balance(ctx, member: discord.Member=None):
    if member == None:
      member = ctx.author

    await open_account(member)
    await levels(member)
    user = member
    users = await get_bank_data()
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    em = discord.Embed(title=f"{member.name}'s Balance", color=0xff0000)
    em.set_thumbnail(url=member.avatar_url)
    em.add_field(name=":yen:  Cash",
                 value="|    " + str(wallet_amt) + " |",
                 inline=True)
    em.add_field(name="\u200b", value="\u200b", inline=True)
    em.add_field(name="<:slayersgem:785765850862059520> Slayer's Gems",
                 value="|    " + str(bank_amt) + " |",
                 inline=True)

    await ctx.send(embed=em)


@client.command()
@commands.cooldown(1, 13, commands.BucketType.user)
async def profile(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author
    await open_account(member)
    await open_moves(member)
    await open_newitems(member)
    await levels(member)
    users = await get_bank_data()
    user = member
    z = users[str(user.id)]["crystal"]
    y = member
    x = users[str(user.id)]["xp"]
    twoamt = users[str(user.id)]["twostar"]
    threeamt = users[str(user.id)]["threestar"]
    fouramt = users[str(user.id)]["fourstar"]
    fiveamt = users[str(user.id)]["fivestar"]
    blade_amt = users[str(user.id)]["blade"]
    invmats = users[str(user.id)]["coal"] + users[str(
        user.id)]["ore"] + users[str(user.id)]["sand"] + users[str(
            user.id)]["nichirin"]
    invcrates = users[str(user.id)]["common"] + users[str(
        user.id)]["rare"] + users[str(user.id)]["epic"] + users[str(
            user.id)]["legendary"] + users[str(user.id)]["mystical"]
    invcomba = int(twoamt) + int(threeamt) + int(fouramt) + int(fiveamt) + int(
        blade_amt)
    invitems = invmats + invcrates + invcomba
    global dscrank
    global li
    global li1
    if x in range(0, 499):
        dscrank = "Mizunoto | Rank X"
        li = 500 - x
        li1 = 500
    elif x in range(500, 1899):
        dscrank = "Mizunoe | Rank IX"
        li = 1900 - x
        li1 = 1900
    elif x in range(1900, 2799):
        dscrank = "Kanoto | Rank VIII"
        li = 2800 - x
        li1 = 2800
    elif x in range(2800, 3899):
        dscrank = "Kanoe | Rank VII"
        li = 3900 - x
        li1 = 3900
    elif x in range(3900, 4999):
        dscrank = "Tsuchinoto | Rank VI"
        li = 5000 - x
        li1 = 5000
    elif x in range(5000, 6499):
        dscrank = "Tsuchinoe | Rank V"
        li = 6500 - x
        li1 = 6500
    elif x in range(6500, 7899):
        dscrank = "Hinoto | Rank IV"
        li = 7900 - x
        li1 = 7900
    elif x in range(7900, 9099):
        dscrank = "Hinoe | Rank III"
        li = 9100 - x
        li1 = 9100
    elif x in range(9100, 11499):
        dscrank = "Kinoto | Rank II"
        li = 11500 - x
        li1 = 11500
    elif x in range(11500, 14999):
        dscrank = "Kinoe | Rank I"
        li = 15000 - x
        li1 = 15000
    elif x in range(15000, 999999999):
        dscrank = "Hashira | Rank MAX"
        li1 = "`MAX`"
        li = "`MAX`"

    else:
        dscrank = "Error retrieving data"
        li1 = "Error retrieving data"
        li = "Error retrieving data"
    res = await levels(user)
    uslvl = users[str(user.id)]["lvl"]
    lv = res[1]
    lim = res[2]
    aut = member.id
    
    embed = discord.Embed(color=0x2670e8)
    embed.set_author(name=f"{y}'s Profile", icon_url=member.avatar_url)
    if aut in admins and adminmode == True:
      embed.add_field(name="User Information, Level And Statistics",
                      value="---------------------------------------------------",
                      inline=False)
      embed.add_field(name=":sparkles: This User Is A Bot Admin", value="\u200b", inline=False)
    elif aut in testers:
      embed.add_field(name="User Information, Level And Statistics",
                      value="---------------------------------------------------",
                      inline=False)
      embed.add_field(name=":tools: This User Is A Bot Tester", value="\u200b", inline=False)
    else:
      embed.add_field(name="User Information, Level And Statistics",
                      value="\u200b",
                      inline=False)

    embed.add_field(name="Current Wallet Balance",
                    value=str(users[str(user.id)]["wallet"]) +
                    "  :yen:  Cash \n" + str(users[str(user.id)]["bank"]) +
                    "  <:slayersgem:785765850862059520>  Slayer's Gems\n",
                    inline=True)
    embed.add_field(name="Current Bag Item Status",
                    value=str(invitems) + " :briefcase: Total Items \n " +
                    str(invmats) + " :pick: Materials \n" + str(invcrates) +
                    " :gift:  Loot Crates \n" + str(invcomba) +
                    " :crossed_swords: Combat",
                    inline=True)
  
    embed.add_field(name="Learned Moves Count (`Coming Soon`)", value="★★★★★ `N/A`\n★★★★☆ `N/A`\n★★★☆☆ `N/A`\n★★☆☆☆ `N/A`", inline=True)
    

    if member.id in admins and adminmode == True:
        embed.add_field(name=" Demon Slayer Corps Rank",
                        value="Hashira | Rank ∞ MAX",
                        inline=True)
    else:
      embed.add_field(name=" Demon Slayer Corps Rank",
                        value=dscrank,
                        inline=True)

    if member.id in admins and adminmode == True:
      embed.add_field(name="Experience Until Next Rank ",
                      value="`MAX RANK`",
                      inline=True)
    else:
      embed.add_field(name="Experience Until Next Rank ",
                      value=str(li),
                      inline=True)

    if member.id in admins and adminmode == True:
      embed.add_field(name="Rank Progress",
                        value=str(x) + "/ ∞ ",
                        inline=True)
    else:
      embed.add_field(name="Rank Progress",
                      value=str(x) + "/ "+str(li1)+" Experience",
                      inline=True)
    if member.id in admins and adminmode == True:
        embed.add_field(name="Player Level",
                        value="∞ MAX",
                        inline=True)
    else:
        embed.add_field(name="Player Level", value=str(uslvl), inline=True)
    if member.id in admins and adminmode == True:
      embed.add_field(name="XP Required For Next Level",
                    value="`MAX LEVEL`",
                    inline=True)
    else:
      embed.add_field(name="XP Required For Next Level",
                      value=str(lv),
                      inline=True)
    if member.id in admins and adminmode == True:
      embed.add_field(name="Level Progress",
                    value=str(x) + "/ ∞ ",
                    inline=True)
    else:
      embed.add_field(name="Level Progress",
                      value=str(x) + "/" + str(lim) + " Experience",
                      inline=True)
    embed.add_field(name="Learned Moves (`Coming Soon`)",
                    value=":dash: Total Concentration Breathing `N/A`\n:zap: Thunder Breathing `N/A`\n :ocean:  Water Breathing `N/A`",
                    inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

    
@profile.error
async def profile_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Due to high bot activity and a possibility of exceeding Discord's ratelimits, a temporary cooldown of 15 seconds has been imposed on this command !\nPlease **try again in {:.2f} seconds**!".format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


#admin / testers

@client.command(aliases = ["fm"])
async def freemoney(ctx, amt: int, ctype: str):
  await open_account(ctx.author)
  await open_moves(ctx.author)
  await open_newitems(ctx.author)
  await levels(ctx.author)
  users = await get_bank_data()
  user = ctx.author
  with open("mainbank.json", "r") as f:
        users = json.load(f)
  try:
    if ctx.author.id in admins or ctx.author.id in testers:
      if ctype.lower() == "cash":
        users[str(user.id)]["wallet"] += amt
        with open("mainbank.json", "w") as f:
                    json.dump(users, f)
        await ctx.send(f"{amt} :yen: Cash generated and added to {ctx.author}'s wallet")

      elif ctype.lower() == "gem" or ctype.lower() == "gems":
        users[str(user.id)]["bank"] += amt
        with open("mainbank.json", "w") as f:
                    json.dump(users, f)
        await ctx.send(f"{amt} <:slayersgem:785765850862059520>  Slayer's Gems generated and added to {ctx.author}'s wallet")
      
      else:
        await ctx.send("error")

    else:
      await ctx.send("This command is accessible only to testers and admins")
  except Exception as er:
    await ctx.send(er)



#mines
@client.command(aliases=['m1'])
@commands.cooldown(1, 30, commands.BucketType.user)
async def mine1(ctx):
    individualmaintenance = False
    if maintenancemode == True:
      await ctx.send("The bot is under maintenance :tools: :gear:\nTry again in a few minutes")

    elif individualmaintenance == True:
      
      await ctx.send("This command is under maintenance :tools: :gear:\nTry again in a few minutes.\nBrand new mining system in works ! Please be patient !")

      
    
    else:
      
      xpm1 = ['8', '9', '10', '11', '12']
      mine1rewardno = [
          '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2',
          '2', '2', '3', '3', '3', '4'
      ]  #2 rate =80%  3 rate =15% 4 rate=5%
      minerewards = [
          'Scarlet Crimson Iron Dust', 'Scarlet Crimson Iron Ore Fragment', 'a',
          'Scarlet Crimson Iron Ore Fragment', 'a', 'Scarlet Crimson Iron Dust',
          'Scarlet Crimson Iron Dust', 'Scarlet Crimson Iron Ore Fragment',
          'Coal', 'Coal', 'Ancient Crystal Shard',
          'Scarlet Crimson Iron Ore Fragment', 'Scarlet Crimson Iron Sand'
      ]
      item = random.choice(minerewards)
      m1r = random.choice(mine1rewardno)
      m1x = random.choice(xpm1)

      embed=discord.Embed(title="Mine 1  :pick:", description="Where do you want to search in Mine 1 ?", color=0xff7b00)
      embed.add_field(name="Choose from the reactions !", value="\u200b", inline=False)
      embed.set_thumbnail(url="https://i.imgur.com/VOTg0zO.png")
      m1msg = await ctx.send(embed=embed)
      
      await m1msg.add_reaction("\U00002b06") #Up arrow
      await asyncio.sleep(0.24)
      await m1msg.add_reaction("\U00002b05") #left arrow
      await asyncio.sleep(0.24)
      await m1msg.add_reaction("\U000027a1") #right arrow
      await asyncio.sleep(0.24)
      await m1msg.add_reaction("\U00002196") #upper left arrow
      await asyncio.sleep(0.24)
      await m1msg.add_reaction("\U00002197") #upper right arrow
      await asyncio.sleep(0.24)
      await m1msg.add_reaction("\U00002199") #lower left arrow
      await asyncio.sleep(0.24)
      await m1msg.add_reaction("\U00002198") #lower right arrow
      
      @client.event
      async def on_reaction_add(reaction, user):
        emoji = reaction.emoji
        if user.bot:
            return
        else:
          global direction
          if emoji == "\U00002b06" and user == ctx.author: 
            direction = "Straight"
          elif emoji == "\U00002b05" and user == ctx.author: 
            direction = "Left"
          elif emoji == "\U000027a1" and user == ctx.author: 
            direction = "Right"
          elif emoji == "\U00002197" and user == ctx.author: 
            direction = "The Far Right"
          elif emoji == "\U00002196" and user == ctx.author: 
            direction = "The Far Left"
          elif emoji == "\U00002198" and user == ctx.author: 
            direction = "The Front Right"
          elif emoji == "\U00002199" and user == ctx.author: 
            direction = "The Front Left"
        
        await open_account(ctx.author)
        await levels(ctx.author)

        users = await get_bank_data()
        user = ctx.author
        

        if item == 'Scarlet Crimson Iron Ore Fragment':
          users[str(user.id)]["fragment"] += int(m1r)
          
          users[str(user.id)]["xp"] += int(m1x)
          
          
        elif item == 'Scarlet Crimson Iron Dust':
            users[str(user.id)]["dust"] += int(m1r)
            
            users[str(user.id)]["xp"] += int(m1x)
            
            

        elif item == 'Scarlet Crimson Iron Sand':
            users[str(user.id)]["sand"] += int(m1r)
            
            users[str(user.id)]["xp"] += int(m1x)
            

            
        elif item == 'Coal':
            users[str(user.id)]["coal"] += int(m1r)
            
            users[str(user.id)]["xp"] += int(m1x)
            

           
        elif item == 'Ancient Crystal Shard':
            users[str(user.id)]["shard"] += int(m1r)
            
            users[str(user.id)]["xp"] += int(m1x)
        
        elif item == "a":
          pass
        
        else:
            await ctx.send("Error : Item obtained not in database\nPlease report this at our official server (`t help` for invite link`)")
        
        with open("mainbank.json", "w") as f:
                json.dump(users, f)
        with open("mainbank.json", "w") as f:
                json.dump(users, f)

        extrachance = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "0"]

        yesorno = random.choice(extrachance)
        await m1msg.clear_reaction("\U00002b06") #Up arrow
        await asyncio.sleep(0.24)
        await m1msg.clear_reaction("\U00002b05") #left arrow
        await asyncio.sleep(0.24)
        await m1msg.clear_reaction("\U000027a1") #right arrow
        await asyncio.sleep(0.24)
        await m1msg.clear_reaction("\U00002196") #upper left arrow
        await asyncio.sleep(0.24)
        await m1msg.clear_reaction("\U00002197") #upper right arrow
        await asyncio.sleep(0.24)
        await m1msg.clear_reaction("\U00002199") #lower left arrow
        await asyncio.sleep(0.24)
        await m1msg.clear_reaction("\U00002198") #lower right arrow
        

        if item == "a":
          embed1=discord.Embed(title="You Ventured Into Mine 1  :pick: . . .", description=f"You have searched **{direction}** in Mine 1 !", color=0xff7b00)
          embed1.add_field(name=f"Unfortunately You Obtained Nothing and earned 0 Experience Orbs", value="\u200b", inline=False)
          if yesorno == "1":
            pass
          elif yesorno == "0":
            embed1.add_field(name="You see something shining far inside the mine.", value="To check out what it is and for a possibility to __gain a special reward__, react with :white_check_mark:")
            await m1msg.add_reaction("\U00002705")
          
          embed1.set_thumbnail(url="https://i.imgur.com/VOTg0zO.png")
          
          await m1msg.edit(embed=embed1)
          
        
        else:
          embed2=discord.Embed(title="You Ventured Into Mine 1  :pick: . . .", description=f"You have searched **{direction}** in Mine 1 !", color=0xff7b00)
          embed2.add_field(name=f"You Obtained __{m1r} {item}__ and earned __{m1x} Experience Orbs__", value="\u200b", inline=False)
          if yesorno == "1":
            pass
          elif yesorno == "0":
            embed2.add_field(name="You see something shining far inside the mine.", value="To check out what it is and for a possibility to __gain a special reward__, react with :white_check_mark:")
            await m1msg.add_reaction("\U00002705")
          
          
          embed2.set_thumbnail(url="https://i.imgur.com/VOTg0zO.png")
         
          await m1msg.edit(embed=embed2)
          

        
       

@client.command(aliases=['m2'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def mine2(ctx):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await levels(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    xpm2 = ['5', '6', '7', '8', '9', '10', '11']
    mine2rewardno = [
        '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
        '2', '2', '2', '2', '2', '3'
    ]  #1 rate =70%  2 rate =25% 3 rate =5%
    minerewards = [
        'Scarlet Crimson Iron Dust', 'a', 'Scarlet Crimson Iron Ore Fragment',
        'Scarlet Crimson Iron Dust', 'a', 'Scarlet Crimson Iron Ore Fragment',
        'Coal', 'Coal', 'Ancient Crystal Shard'
    ]
    item = random.choice(minerewards)
    m2r = random.choice(mine2rewardno)
    m2x = random.choice(xpm2)
    res = await levels(user)
    uslvl = users[str(user.id)]["lvl"]

    if int(uslvl) < 3:
        await ctx.send("**Mine 2** is unlocked upon reaching **Level 3** !")
    else:

        if item == 'Scarlet Crimson Iron Ore Fragment':
            users[str(user.id)]["fragment"] += int(m2r)
            
            users[str(user.id)]["xp"] += int(m2x)
            
            await ctx.send("You ventured into mine 2...\nYou found **" +
                           str(m2r) + " " + str(item) + " ** and gained **" +
                           str(m2x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Dust':
            users[str(user.id)]["dust"] += int(m2r)
            
            users[str(user.id)]["xp"] += int(m2x)
           
            await ctx.send("You ventured into mine 2...\nYou found **" +
                           str(m2r) + " " + str(item) + " ** and gained **" +
                           str(m2x) + " Experience Orbs**")

        elif item == 'Coal':
            users[str(user.id)]["coal"] += int(m2r)
            
            users[str(user.id)]["xp"] += int(m2x)
            

            await ctx.send("You ventured into mine 2...\nYou found **" +
                           str(m2r) + " " + str(item) + " ** and gained **" +
                           str(m2x) + " Experience Orbs**")
        elif item == 'Ancient Crystal Shard':
            users[str(user.id)]["shard"] += int(m2r)
            
            users[str(user.id)]["xp"] += int(m2x)
           

            await ctx.send("You ventured into mine 2...\nYou found **" +
                           str(m2r) + " " + str(item) + " ** and gained **" +
                           str(m2x) + " Experience Orbs**")
        
        
        elif item == 'a':
            await ctx.send(
                "You ventured into mine 2...\nUnfortunately, you found nothing !"
            )
        with open("mainbank.json", "w") as f:
                json.dump(users, f)


@client.command(aliases=["m3"])
@commands.cooldown(1, 17, commands.BucketType.user)
async def mine3(ctx):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await levels(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    xpm3 = ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    mine3rewardno = [
        '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '2',
        '2', '2', '2', '2', '3', '3'
    ]  #1 rate =60%  2 rate =30% 3 rate =10%
    minerewards = [
        'Scarlet Crimson Iron Dust', 'Scarlet Crimson Iron Ore Fragment',
        'Scarlet Crimson Iron Dust', 'a', 'Scarlet Crimson Iron Ore Fragment',
        'Scarlet Crimson Iron Dust', 'Scarlet Crimson Iron Ore Chunk',
        'Scarlet Crimson Iron Sand', 'Ancient Crystal Shard', 'a',
        'Scarlet Crimson Iron Ore Fragment', 'Coal', 'Coal'
    ]
    item = random.choice(minerewards)
    m3r = random.choice(mine3rewardno)
    m3x = random.choice(xpm3)
    res = await levels(user)
    uslvl = users[str(user.id)]["lvl"]
    if int(uslvl) >= 5:

        if item == 'Scarlet Crimson Iron Ore Fragment':
            users[str(user.id)]["fragment"] += int(m3r)
            
            users[str(user.id)]["xp"] += int(m3x)
            
            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Ore Chunk':
            users[str(user.id)]["chunk"] += int(m3r)
            
            users[str(user.id)]["xp"] += int(m3x)
           
            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Dust':
            users[str(user.id)]["dust"] += int(m3r)
          
            users[str(user.id)]["xp"] += int(m3x)
            
            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Sand':
            users[str(user.id)]["sand"] += int(m3r)
            
            users[str(user.id)]["xp"] += int(m3x)
           

            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")
        elif item == 'Scarlet Crimson Iron Ore':
            users[str(user.id)]["ore"] += int(m3r)
      
            users[str(user.id)]["xp"] += int(m3x)
      

            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")
        elif item == 'Coal':
            users[str(user.id)]["coal"] += int(m3r)
         
            users[str(user.id)]["xp"] += int(m3x)
   

            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")
        elif item == 'Ancient Crystal Shard':
            users[str(user.id)]["shard"] += int(m3r)
        
            users[str(user.id)]["xp"] += int(m3x)
      

            await ctx.send("You ventured into mine 3...\nYou found **" +
                           str(m3r) + " " + str(item) + " ** and gained **" +
                           str(m3x) + " Experience Orbs**")
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
        elif item == 'a':
            await ctx.send(
                "You ventured into mine 3...\nUnfortunately, you found nothing !"
            )
    else:
        await ctx.send("**Mine 3** is unlocked upon reaching **Level 5** !")


@client.command(aliases=["m4"])
@commands.cooldown(1, 19, commands.BucketType.user)
async def mine4(ctx):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await levels(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    xpm4 = [
        '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
        '17', '18'
    ]
    mine4rewardno = [
        '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '2', '2', '2', '2',
        '2', '2', '2', '2', '3', '3'
    ]  #1 rate =50% 2 rate =40% 3 rate = 10%
    minerewards = [
        'Scarlet Crimson Iron Sand', 'Scarlet Crimson Iron Dust',
        'Scarlet Crimson Iron Dust', 'Scarlet Crimson Iron Ore Chunk',
        'Scarlet Crimson Iron Sand', 'Scarlet Crimson Iron Ore Fragment',
        'Scarlet Crimson Iron Ore Fragment', 'Ancient Crystal Shard', 'a',
        'Scarlet Crimson Ore', 'Coal', 'Coal'
    ]
    item = random.choice(minerewards)
    m4r = random.choice(mine4rewardno)
    m4x = random.choice(xpm4)
    res = await levels(user)
    uslvl = uslvl = users[str(user.id)]["lvl"]
    lv = res[1]
    lim = res[2]
    if int(uslvl) < 8:
        await ctx.send("**Mine 4** is unlocked upon reaching **Level 8** !")
    else:
        if item == 'Scarlet Crimson Iron Ore Fragment':
            users[str(user.id)]["fragment"] += int(m4r)
            
            users[str(user.id)]["xp"] += int(m4x)
            
            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Ore Chunk':
            users[str(user.id)]["chunk"] += int(m4r)
            
            users[str(user.id)]["xp"] += int(m4x)
            
            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Dust':
            users[str(user.id)]["dust"] += int(m4r)
            
            users[str(user.id)]["xp"] += int(m4x)
            
            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")
        elif item == 'Scarlet Crimson Iron Sand':
            users[str(user.id)]["sand"] += int(m4r)
            
            users[str(user.id)]["xp"] += int(m4x)
           

            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")
        elif item == 'Scarlet Crimson Ore':
            users[str(user.id)]["ore"] += int(m4r)
           
            users[str(user.id)]["xp"] += int(m4x)
            

            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")
        elif item == 'Coal':
            users[str(user.id)]["coal"] += int(m4r)
            
            users[str(user.id)]["xp"] += int(m4x)
            

            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")
        elif item == 'Ancient Crystal Shard':
            users[str(user.id)]["shard"] += int(m4r)
           
            users[str(user.id)]["xp"] += int(m4x)
           

            await ctx.send("You ventured into mine 4...\nYou found **" +
                           str(m4r) + " " + str(item) + " ** and gained **" +
                           str(m4x) + " Experience Orbs**")
        elif item == 'a':
            await ctx.send(
                "You ventured into mine 4...\nUnfortunately, you found nothing !"
            )
        with open("mainbank.json", "w") as f:
                json.dump(users, f)


@client.command(aliases=["m5"])
@commands.cooldown(1, 21, commands.BucketType.user)
async def mine5(ctx):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await levels(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    xpm5 = [
        '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
        '17', '18', '19', '20', '21', '22'
    ]
    mine5rewardno = [
        '1', '1', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2',
        '2', '2', '3', '3', '3', '3'
    ]  #1 rate =35% 2 rate =45% 3 rate = 20%
    minerewards = [
        'Ancient Crystal Shard', 'Scarlet Crimson Iron Ore', 'a',
        'Scarlet Crimson Iron Ore Chunk', 'Scarlet Crimson Iron Dust',
        'Ancient Crystal Shard', 'Scarlet Crimson Iron Ore', 'Coal', 'Coal'
    ]
    item = random.choice(minerewards)
    m5r = random.choice(mine5rewardno)
    m5x = random.choice(xpm5)
    res = await levels(user)
    uslvl=users[str(user.id)]["lvl"]
    lv = res[1]
    lim = res[2]
    if int(uslvl) < 10:
        await ctx.send("**Mine 5** is unlocked upon reaching **Level 10** !")
    else:
        if item == 'Scarlet Crimson Iron Ore Fragment':
            users[str(user.id)]["fragment"] += int(m5r)
            
            users[str(user.id)]["xp"] += int(m5x)
            
            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Ore Chunk':
            users[str(user.id)]["chunk"] += int(m5r)
           
            users[str(user.id)]["xp"] += int(m5x)
            
            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Dust':
            users[str(user.id)]["dust"] += int(m5r)
            
            users[str(user.id)]["xp"] += int(m5x)
            
            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")
        elif item == 'Scarlet Crimson Iron Sand':
            users[str(user.id)]["sand"] += int(m5r)
            
            users[str(user.id)]["xp"] += int(m5x)
            

            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")
        elif item == 'Scarlet Crimson Iron Ore':
            users[str(user.id)]["ore"] += int(m5r)
            
            users[str(user.id)]["xp"] += int(m5x)
            

            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")
        elif item == 'Coal':
            users[str(user.id)]["coal"] += int(m5r)
            
            users[str(user.id)]["xp"] += int(m5x)
           

            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")
        elif item == 'Ancient Crystal Shard':
            users[str(user.id)]["shard"] += int(m5r)
           
            users[str(user.id)]["xp"] += int(m5x)
            

            await ctx.send("You ventured into mine 5...\nYou found **" +
                           str(m5r) + " " + str(item) + " ** and gained **" +
                           str(m5x) + " Experience Orbs**")
        elif item == 'a':
            await ctx.send(
                "You ventured into mine 5...\nUnfortunately, you found nothing !"
            )
        with open("mainbank.json", "w") as f:
                json.dump(users, f)


@client.command(aliases=["m6"])
@commands.cooldown(1, 23, commands.BucketType.user)
async def mine6(ctx):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await levels(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    xpm6 = [
        '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
        '17', '18', '19', '20', '21', '22', '23', '24', '25'
    ]
    mine6rewardno = [
        '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '2', '2', '2', '2',
        '2', '3', '3', '3', '3', '3'
    ]  #1 rate =25% 2 rate =50% 3 rate = 25%
    minerewards = [
        'Scarlet Crimson Iron Sand', 'Ancient Crystal Shard',
        'Scarlet Crimson Iron Ore', 'a', 'Scarlet Crimson Iron Ore Chunk',
        'Scarlet Crimson Iron Dust', 'Ancient Crystal Shard',
        'Scarlet Crimson Iron Ore', 'Coal', 'Coal'
    ]
    item = random.choice(minerewards)
    m6r = random.choice(mine6rewardno)
    m6x = random.choice(xpm6)
    res = await levels(user)
    uslvl = users[str(user.id)]["lvl"]
    lv = res[1]
    lim = res[2]
    if int(uslvl) < 13:
        await ctx.send("**Mine 6** is unlocked upon reaching **Level 13** !")
    else:
        if item == 'Scarlet Crimson Iron Ore Fragment':
            users[str(user.id)]["fragment"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
            
            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Ore Chunk':
            users[str(user.id)]["chunk"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
            
            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Dust':
            users[str(user.id)]["dust"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
            
            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")

        elif item == 'Scarlet Crimson Iron Sand':
            users[str(user.id)]["sand"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
            

            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")
        elif item == 'Scarlet Crimson Iron Ore':
            users[str(user.id)]["ore"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
           

            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")
        elif item == 'Coal':
            users[str(user.id)]["coal"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
            

            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")
        elif item == 'Ancient Crystal Shard':
            users[str(user.id)]["shard"] += int(m6r)
            
            users[str(user.id)]["xp"] += int(m6x)
            

            await ctx.send("You ventured into mine 6...\nYou found **" +
                           str(m6r) + " " + str(item) + " ** and gained **" +
                           str(m6x) + " Experience Orbs**")
        elif item == 'a':
            await ctx.send(
                "You ventured into mine 6...\nUnfortunately, you found nothing !"
            )
        with open("mainbank.json", "w") as f:
                json.dump(users, f)


@mine1.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      embed=discord.Embed(description=f"You've already searched this mine ! You can only search this mine __every 30 seconds__\nYou can explore this mine again __in {error.retry_after:.2f} seconds__", color=0xff7b00)
      embed.set_author(name="Let The Mine Regenerate !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
        
    else:
        raise error


@mine2.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited to **once per 15 seconds** !\nPlease **try again in {:.2f} seconds**!'.format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@mine3.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited to **once per 17 seconds** !\nPlease **try again in {:.2f} seconds**!'.format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@mine4.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited to **once per 19 seconds** !\nPlease **try again in {:.2f} seconds**!'.format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@mine5.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited to **once per 21 seconds** !\nPlease **try again in {:.2f} seconds**!'.format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@mine6.error
async def mine_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited to **once per 23 seconds** !\nPlease **try again in {:.2f} seconds**!'.format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


@client.command(aliases=["dailyreward"])
@commands.cooldown(1, 85800, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)
    
    user = ctx.author
    users = await get_bank_data()
    users[str(user.id)]["bank"] += 15
    users[str(user.id)]["wallet"] += 500
    users[str(user.id)]["xp"] += 40
    users[str(user.id)]["shard"] += 10

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
        
    embed = discord.Embed(title="Daily Reward  :alarm_clock:", color=0x000000)
    embed.add_field(name="Claimed Daily Reward !",
                    value="Claim your next reward in 23h50m !",
                    inline=False)
    embed.add_field(
        name="Rewards Received",
        value=
        "`15` <:slayersgem:785765850862059520> `Slayer\'s Gems` ,   `10 Ancient Crystal Shards` ,\n`500` :yen: `Cash`,  `50 Experience Orbs`",
        inline=False)
    await ctx.send(embed=embed)


@daily.error
async def daily_error(ctx, error):
    err = int(error.retry_after)
    new = err/3600
    if isinstance(error, commands.CommandOnCooldown):
        if new < 1:
          msg = "You've already claimed your daily reward !\nNext reward available in **{:.2f} minutes**!".format(new*60)
          await ctx.send(msg)
        else:

          msg1 = "You've already claimed your daily reward !\nNext reward available in **{:.2f} hours**!".format(
              new)
          await ctx.send(msg1)
    else:
        raise error


#shop

@client.command(aliases=["s"])
async def shop(ctx):
  await open_moves(ctx.author)
  await open_account(ctx.author)
  await open_moves(ctx.author)
  await open_newitems(ctx.author)

  one = Button(style=ButtonStyle.blue, label="Wisteria Shop", id="embed1", emoji="⛩️")
  two = Button(style=ButtonStyle.blue, label="Loot Crate Store", id="embed2", emoji="🎁")
  three = Button(style=ButtonStyle.blue, label="Artifacts & Antiques Store", id="embed3", emoji="🎋")
  four = Button(style=ButtonStyle.blue, label="Return To Main Menu", id="embed4", emoji="🛍️")

  av = ctx.author.avatar_url
  embed=discord.Embed(title="**Wisteria Market  :shopping_bags:**", description="The shopping street of the Taisho Era. Buy and sell all sorts of items here !", color=0xde0202)
  embed.add_field(name="Which Shop Do You Wish To Go To?", value="Click on the reactions to choose !", inline=False)
  embed.add_field(name=":shinto_shrine:  Wisteria Shop", value="Find high-grade materials for forging and a wide variety of general items !", inline=False)
  embed.add_field(name=":gift:  Loot Crate Store", value="Buy Loot Crates here !", inline=False)
  embed.add_field(name=":tanabata_tree:  Artifacts & Antiques Store", value="Find various items to aid your adventure and artifacts (coming soon) here !", inline=True)
  shopmenu = await ctx.send(embed=embed, components=[[one,two,three]])
  
  embeds = discord.Embed(
            title="**:shinto_shrine:  Wisteria Shop  :shinto_shrine:**",
            description=
            "Find high-grade materials for forging and a wide variety of general items !",
            color=0xff0000)
  
  
  embeds.add_field(
    name="** **",
    value=
    "**[Scarlet Crimson Iron Ore Fragment](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)  -  200 :yen:**\n**ID-**`fragment` | A fragment of a bright red ore that constantly absorbs sunlight.",
    inline=False)
  embeds.add_field(
    name="** **",
    value=
    "**[Scarlet Crimson Iron Ore Chunk](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)  -  420 :yen:**\n**ID-**`chunk` | A chunk of a bright red ore that constantly absorbs sunlight",
    inline=True)
  embeds.add_field(
    name="** **",
    value=
    "**[Scarlet Crimson Iron Ore](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92) - Can Only Be Sold**\n**ID-**`ore` | Bright red ore that constantly absorbs sunlight.",
    inline=False)
  embeds.add_field(
    name="** **",
    value=
    "**[Scarlet Crimson Iron Dust](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)  - 180 :yen:**\n**ID-**`dust` | Iron dust that constantly soaks in sunlight.",
    inline=False)
  
  embeds.add_field(
    name=
    "**For sell price and more info on an item, run `t iteminfo <Item Id>`\n**To buy an item run : `t buy <Item ID> <quantity (default-1)>`\nTo sell an item run : `t sell <Item ID> <quantity (default-1)>`",
    value="\u200b",
    inline=False)
  
  embeds.set_footer(text="Viewing Page 1 of 2\nReact with \U000027a1 to view the next page", icon_url=av)

#=============================================

  embeds1 = discord.Embed(
            title="**:shinto_shrine:  Wisteria Shop  :shinto_shrine:**",
            description=
            "Find high-grade materials for forging and a wide variety of general items !",
            color=0xff0000)

  embeds1.add_field(
    name="** **",
    value=
    "**[Scarlet Crimson Iron Sand](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92) - Can Only Be Sold**\n**ID-**`sand` | Iron sand that constantly soaks in sunlight.",
    inline=False)
  embeds1.add_field(
    name="** **",
    value=
    "**[Nichirin Ore](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92) - 30 <:slayersgem:785765850862059520>**\n**ID-**`nichirin` | A peculiar alloy forged using Scarlet Crimson Ore and Iron Sand.",
    inline=False)
  embeds1.add_field(
    name="** **",
    value=
    "**[Coal](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92) - 125 :yen:**\n**ID-**`coal` |Coal used for crafting and forging purposes. Sold to earn money.",
    inline=False)
  embeds1.add_field(
    name="** **",
    value=
    "**[Ancient Crystals](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92) - Can Only Be Sold**\n**ID-**`crystals` | Valuable ancient crystals needed for forging"
  )
  embeds1.add_field(
    name=
    "**For sell price and more info on an item, run `t iteminfo <Item Id>`\n**To buy an item run : `t buy <Item ID> <quantity (default-1)>`\nTo sell an item run : `t sell <Item ID> <quantity (default-1)>`",
    value="\u200b",
    inline=False)
  embeds1.set_footer(text="Viewing Page 2 of 2\nReact with \U00002b05 to view the previous page", icon_url=av)

  #========================================================

  embedc = discord.Embed(
        title=":gift:  Loot Crate Store  :gift: ",
        description=
        "Buy loot crates here !",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0xff0000)
    
    
  embedc.add_field(
      name="** **",
      value=
      "**[Common Loot Crate](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 5000 :yen:\nChance of containing Common items and cash.",
      inline=False)
  embedc.add_field(
      name="** **",
      value=
      "**[Rare Loot Crate](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 10000 :yen:\nChance of containing Rare items and Slayer's Gems and cash.",
      inline=False)
  embedc.add_field(
      name="** **",
      value=
      "**[Epic Loot Crate](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 50000 :yen:\nChance of containing Slayer's Gems, Epic items and `★★☆☆☆` or `★★★☆☆` Move Scrolls and cash.",
      inline=False)
  embedc.add_field(
      name="** **",
      value=
      "**[Legendary Loot Crate](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 90000 :yen:\nChance of containing Slayer Moves, Legendary Items and `★★★☆☆` or `★★★★☆` Move Scrolls and cash",
      inline=False)
  embedc.add_field(
      name="** **",
      value=
      "**[Mystical Loot Crate](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 250 <:slayersgem:785765850862059520> Slayer's Gems\nChance of containing `★★★★☆` or `★★★★★` Slayer Move Scrolls, Slayer's Gems and Legendary items and cash.",
      inline=False)
  embedc.add_field(
      name=
      "**To buy a crate, run: `t buy <crate rarity> <quantity(defaults to 1)>`\nTo use a crate, run: `t crate <crate rarity>`**",
      value="\u200b",
      inline=False)
  av1 = ctx.author.avatar_url
  embedc.set_footer(text="Viewing Page 1 of 1", icon_url=av1)

  #==========================================
  
  embeda = discord.Embed(
        title="**:tanabata_tree:  Artifacts & Antiques Store** ",
        description=
        "Find various items to aid your adventure and artifacts (coming soon) here !",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0xff0000)
    
    
  embeda.add_field(
      name="** **",
      value=
      "**[Vial Of Experience Orbs](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 30 <:slayersgem:785765850862059520> Slayer's Gems\n**ID**-`vial` | A vial containing experience orbs. When used, will instantly provide 500 experience. **COMING SOON**",
      inline=False)
  embeda.add_field(
      name="** **",
      value=
      "**[Jar Of Experience Orbs](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 60 <:slayersgem:785765850862059520> Slayer's Gems\n**ID**-`jar` | A jar containing experience orbs. When used, will instantly provide 1000 experience. **COMING SOON**",
      inline=False)
  embeda.add_field(
      name="** **",
      value=
      "**[Artifact Crate Key Blueprint](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - 35 <:slayersgem:785765850862059520> Slayer's Gems\n**ID**-`keyblueprint` | A blueprint required to forge an Artifact Crate Key. **COMING SOON**",
      inline=False)
  embeda.add_field(
      name="** **",
      value=
      "**[★★★★★ Scroll Ash](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - Can Only Be Sold\n**ID**-`fivestarash` | Ash obtained after burning a used ★★★★★ Move Scroll. **COMING SOON**",
      inline=False)
  embeda.add_field(
      name="** **",
      value=
      "**[★★★★☆ Scroll Ash](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - Can Only Be Sold\n**ID**-`fourstarash` | Ash obtained after burning a used ★★★★☆ Move Scroll. **COMING SOON**",
      inline=False)
 
  
  embeda.add_field(
    name=
    "**For sell price and more info on an item, run `t iteminfo <Item Id>`\n**To buy an item run : `t buy <Item ID> <quantity (default-1)>`\nTo sell an item run : `t sell <Item ID> <quantity (default-1)>`",
    value="\u200b",
    inline=False)

  av1 = ctx.author.avatar_url
  embeda.set_footer(text="Viewing Page 1 of 2\nReact with \U000027a1 to view the next page", icon_url=av1)
  
  embeda1 = discord.Embed(
        title="**:tanabata_tree:  Artifacts & Antiques Store** ",
        description=
        "Find various items to aid your adventure and artifacts (coming soon) here !",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0xff0000)
  
  
  embeda1.add_field(
      name="** **",
      value=
      "**[★★★☆☆ Scroll Ash](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - Can Only Be Sold\n**ID**-`threestarash` | Ash obtained after burning a used ★★★☆☆ Move Scroll. **COMING SOON**",
      inline=False)
  
  embeda1.add_field(
      name="** **",
      value=
      "**[Nichirin Blade Upgrade Blueprint I](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - XXXXX :yen:\n**ID**-`bladeblueprint1` | A blueprint required to upgrade a nichirin blade to Level 1. **COMING SOON**",
      inline=False)
  embeda1.add_field(
      name="** **",
      value=
      "**[Nichirin Blade Upgrade Blueprint II](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - XXXXX :yen:\n**ID**-`bladeblueprint2` | A blueprint required to upgrade a nichirin blade to Level 2. **COMING SOON**",
      inline=False)
  embeda1.add_field(
      name="** **",
      value=
      "**[Nichirin Blade Upgrade Blueprint III](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - XXXXX :yen:\n**ID**-`bladeblueprint3` | A blueprint required to upgrade a nichirin blade to Level 3. **COMING SOON**",
      inline=False)
  embeda1.add_field(
      name="** **",
      value=
      "**[Nichirin Blade Upgrade Blueprint IV](https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92)** - XXXXX :yen:\n**ID**-`bladeblueprint4` | A blueprint required to upgrade a nichirin blade to Level 4. **COMING SOON**",
      inline=False)
  embeda1.add_field(
    name=
    "**For sell price and more info on an item, run `t iteminfo <Item Id>`\n**To buy an item run : `t buy <Item ID> <quantity (default-1)>`\nTo sell an item run : `t sell <Item ID> <quantity (default-1)>`",
    value="\u200b",
    inline=False)
  
  embeda1.set_footer(text="Viewing Page 2 of 2", icon_url=av1)

  buttons = {"embed1":embeds, "embed2":embedc,"embed3":embeda,"embed4":embed}
  await shopmenu.clear_reaction("\U000026e9")
  await shopmenu.clear_reaction("\U0001f381")
  await shopmenu.clear_reaction("\U0001f38b")
  while True:
    res = await client.wait_for("button_click")
    if res.channel is not ctx.channel:
      return
    if res.channel==ctx.channel:
      response = buttons.get(res.component.id)
      if response is None:
        await ctx.send("Something went wrong. Buttons are at testing stage in this bot")
      else:
        await shopmenu.edit(embed=response)
        resp = await res.respond(
            type=InteractionType.UpdateMessage,
            content="\u200b"
        )
        
        if response == embeds:
          await shopmenu.add_reaction("\U000027a1")
          @client.event
          async def on_reaction_add(reaction, user):
            emoji = reaction.emoji
            if user.bot:
                return

            if emoji == "\U000027a1" and user == ctx.author:
              await shopmenu.clear_reaction("\U000027a1")
              await shopmenu.clear_reaction("\U00002b05")
              await shopmenu.edit(embed=embeds1)
              await shopmenu.clear_reaction("\U000027a1")
              await shopmenu.add_reaction("\U00002b05")
            if emoji == "\U00002b05" and user == ctx.author:
              await shopmenu.edit(embed=embeds)
              await shopmenu.add_reaction("\U000027a1")
              await shopmenu.clear_reaction("\U00002b05")
        elif response == embedc:
          await shopmenu.clear_reaction("\U000027a1")
        elif response == embeda:
            await shopmenu.clear_reaction("\U000027a1")
            await shopmenu.clear_reaction("\U00002b05")
            await shopmenu.edit(embed=embeda)
            await shopmenu.clear_reaction("\U000026e9")
            await shopmenu.clear_reaction("\U0001f381")
            await shopmenu.clear_reaction("\U0001f38b")
            await shopmenu.add_reaction("\U000027a1")
            @client.event
            async def on_reaction_add(reaction, user):
              emoji = reaction.emoji
              if user.bot:
                  return

              if emoji == "\U000027a1" and user == ctx.author:
                await shopmenu.edit(embed=embeda1)
                await shopmenu.clear_reaction("\U000027a1")
                await shopmenu.add_reaction("\U00002b05")
              if emoji == "\U00002b05" and user == ctx.author:
                await shopmenu.edit(embed=embeda)
                await shopmenu.add_reaction("\U000027a1")
                await shopmenu.clear_reaction("\U00002b05")
            await ctx.send("This shop is under works, and is coming soon ! To be instantly notified when it comes out, why not join our support server (`t help` for invite link). We also have massive giveaways frequently !")
        
  @client.event
  async def on_reaction_add(reaction, user):
      emoji = reaction.emoji
      if user.bot:
          return

      if emoji == "\U000026e9" and user == ctx.author:
        await shopmenu.edit(embed=embeds)
        await shopmenu.clear_reaction("\U000026e9")
        await shopmenu.clear_reaction("\U0001f381")
        await shopmenu.clear_reaction("\U0001f38b")
        await shopmenu.add_reaction("\U000027a1")
        @client.event
        async def on_reaction_add(reaction, user):
          emoji = reaction.emoji
          if user.bot:
              return

          if emoji == "\U000027a1" and user == ctx.author:
            await shopmenu.edit(embed=embeds1)
            await shopmenu.clear_reaction("\U000027a1")
            await shopmenu.add_reaction("\U00002b05")
          if emoji == "\U00002b05" and user == ctx.author:
            await shopmenu.edit(embed=embeds)
            await shopmenu.add_reaction("\U000027a1")
            await shopmenu.clear_reaction("\U00002b05")
        
      elif emoji == "\U0001f381" and user == ctx.author:
          await shopmenu.edit(embed=embedc)
          await shopmenu.clear_reaction("\U000026e9")
          await shopmenu.clear_reaction("\U0001f381")
          await shopmenu.clear_reaction("\U0001f38b")
      elif emoji == "\U0001f38b" and user == ctx.author:

          await shopmenu.edit(embed=embeda)
          await shopmenu.clear_reaction("\U000026e9")
          await shopmenu.clear_reaction("\U0001f381")
          await shopmenu.clear_reaction("\U0001f38b")
          await shopmenu.add_reaction("\U000027a1")
          @client.event
          async def on_reaction_add(reaction, user):
            emoji = reaction.emoji
            if user.bot:
                return

            if emoji == "\U000027a1" and user == ctx.author:
              await shopmenu.edit(embed=embeda1)
              await shopmenu.clear_reaction("\U000027a1")
              await shopmenu.add_reaction("\U00002b05")
            if emoji == "\U00002b05" and user == ctx.author:
              await shopmenu.edit(embed=embeda)
              await shopmenu.add_reaction("\U000027a1")
              await shopmenu.clear_reaction("\U00002b05")
          await ctx.send("This shop is under works, and is coming soon ! To be instantly notified when it comes out, why not join our support server (`t help` for invite link). We also have massive giveaways frequently !")
      



@client.command(aliases=["ii"])
async def iteminfo(ctx, a=None):
  if a == None:
    await ctx.send("You need to mention an Item Id (find the ID in the shop) to view its information like this:\n`t iteminfo coal` etc.")
  
  elif a.lower() == "ore":
        embed = discord.Embed(
            title="Item Info",
            description=
            "Find more information about the prices and items here.",
            color=0xff0000,
            url=
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
        )
        embed.set_author(name="| Wisteria Shop |")
        embed.add_field(name="Scarlet Crimson Ore",
                        value="ID-ore | Ore that constantly absorbs sunlight.",
                        inline=False)
        embed.add_field(name="Buy Price", value="1250 :yen:", inline=True)
        embed.add_field(name="Sell Price", value="625 :yen:", inline=True)
        embed.add_field(name="Item Rank", value="Epic", inline=True)
        await ctx.send(embed=embed)

  elif a.lower() == "fragment":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      embed.set_author(name="| Wisteria Shop |")
      embed.add_field(
          name="Scarlet Crimson Iron Ore Fragment",
          value=
          "*ID-*`fragment` | A fragment of a bright red ore that constantly absorbs sunlight.",
          inline=False)
      embed.add_field(name="Buy Price", value="200 :yen:", inline=True)
      embed.add_field(name="Sell Price", value="100 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Common", inline=True)
      await ctx.send(embed=embed)

  elif a.lower() == "chunk":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      embed.set_author(name="| Wisteria Shop |")
      embed.add_field(
          name="Scarlet Crimson Iron Ore Chunk",
          value=
          "*ID-*`chunk` | A chunk of a bright red ore that constantly absorbs sunlight",
          inline=False)
      embed.add_field(name="Buy Price", value="420 :yen:", inline=True)
      embed.add_field(name="Sell Price", value="210 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Rare", inline=True)
      await ctx.send(embed=embed)

  elif a.lower() == "dust":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      
      embed.add_field(
          name="Scarlet Crimson Iron Dust",
          value="*ID-*`dust` | Iron dust that constantly soaks in sunlight.",
          inline=False)
      embed.add_field(name="Buy Price", value="180 :yen:", inline=True)
      embed.add_field(name="Sell Price", value="90 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Common", inline=True)
      await ctx.send(embed=embed)

  elif a.lower() == "sand":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      
      embed.add_field(
          name="Scarlet Crimson Iron Sand",
          value="ID-sand | Iron sand that constantly soaks in sunlight.",
          inline=False)
      embed.add_field(name="Buy Price", value="1000 :yen:", inline=True)
      embed.add_field(name="Sell Price", value="500 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Rare", inline=True)
      await ctx.send(embed=embed)

  elif a.lower() == "nichirin":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      
      embed.add_field(
          name="Nichirin Ore",
          value=
          "ID-nichirin | A peculiar alloy forged using Scarlet Crimson Ore and Iron Sand.",
          inline=False)
      embed.add_field(name="Buy Price",
                      value="30 <:slayersgem:785765850862059520>",
                      inline=True)
      embed.add_field(name="Sell Price", value="20000 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Legendary", inline=True)
      await ctx.send(embed=embed)

  elif a.lower() == "coal":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      
      embed.add_field(
          name="Coal",
          value=
          "ID-coal | Coal used for crafting and forging purposes. Sold to earn money.",
          inline=False)
      embed.add_field(name="Buy Price", value="300 :yen:", inline=True)
      embed.add_field(name="Sell Price", value="125 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Common", inline=True)
      await ctx.send(embed=embed)

  elif a.lower() == "crystals":
      embed = discord.Embed(
          title="Item Info",
          description=
          "Find more information about the prices and items here.",
          color=0xff0000,
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
      )
      
      embed.add_field(
          name="Ancient Crystals",
          value="ID-crystals | Valuable ancient crystals needed for forging.",
          inline=False)
      embed.add_field(name="Buy Price",
                      value="Cannot Be Purchased",
                      inline=True)
      embed.add_field(name="Sell Price", value="820 :yen:", inline=True)
      embed.add_field(name="Item Rank", value="Epic", inline=True)
      await ctx.send(embed=embed)
  

@client.command(aliases=["ws"])
async def wistshop(ctx):
  embed=discord.Embed(title=":x: This Command Is No Longer Available", description="**All shops have been permanently moved to  `t shop` . To view info on an item, use `t iteminfo <Item ID>`**", color=0xf50000)
  await ctx.send(embed=embed)
    


@client.command(aliases=["cs"])
async def crateshop(ctx):
    embed=discord.Embed(title=":x: This Command Is No Longer Available", description="**All shops have been permanently moved to  `t shop`**", color=0xf50000)
    await ctx.send(embed=embed)


@client.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await open_newitems(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    users1 = await get_newitems_data()
    if item == "coal":
        bill = int(amount) * 125
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Coal !")
        else:
            users[str(user.id)]["coal"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            
            embed = discord.Embed(description=f"You purchased {amount} Coal for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) + " Coal for " +
                           str(bill) + " cash !")

    elif item.lower() == "fragment":
        bill = int(amount) * 200

        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Scarlet Crimson Iron Ore Fragment !")
        else:
            users[str(user.id)]["fragment"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            
            embed = discord.Embed(description=f"You purchased {amount} Scarlet Crimson Iron Ore Fragment for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) +
                           " Scarlet Crimson Iron Ore Fragment for " +
                           str(bill) + " cash !")

    elif item.lower() == "chunk":
        bill = int(amount) * 420
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Scarlet Crimson Iron Ore Chunk !")
        else:
            users[str(user.id)]["chunk"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            
            embed = discord.Embed(description=f"You purchased {amount} Scarlet Crimson Iron Ore Chunk for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) +
                           " Scarlet Crimson Iron Ore Chunk for " + str(bill) +
                           " cash !")

    elif item.lower() == "dust":
        bill = int(amount) * 180
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Scarlet Crimson Iron Dust !")
        else:
            users[str(user.id)]["dust"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)

            embed = discord.Embed(description=f"You purchased {amount} Scarlet Crimson Iron Dust for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) +
                           " Scarlet Crimson Iron Dust for " + str(bill) +
                           " cash !")

    elif item.lower() == "sand":

        await ctx.send("This item can only be sold ! Item obtained by forging or mining at higher level mines.")

    elif item.lower() == "nichirin":
        bill = int(amount) * 30
        wall = users[str(user.id)]["bank"] - bill
        if wall < 0:
            await ctx.send(
                "Not enough <:slayersgem:785765850862059520> to purchase " +
                str(amount) + " Nichirin Ore !")
        else:
            users[str(user.id)]["nichirin"] += int(amount)
            users[str(user.id)]["bank"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Nichirin Ore for {bill} <:slayersgem:785765850862059520>", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    
    elif item.lower() == "vial":
        bill = int(amount) * 30
        wall = users[str(user.id)]["bank"] - bill
        if wall < 0:
            await ctx.send(
                "Not enough <:slayersgem:785765850862059520> to purchase " +
                str(amount) + " Vial Of Experience Orbs !")
        else:
            await dumpvial(amount, ctx.author)
            users[str(user.id)]["bank"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Vial Of Experience Orbs for {bill} <:slayersgem:785765850862059520>", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            
    elif item.lower() == "jar":
        bill = int(amount) * 60
        wall = users[str(user.id)]["bank"] - bill
        if wall < 0:
            await ctx.send(
                "Not enough <:slayersgem:785765850862059520> to purchase " +
                str(amount) + " Jar Of Experience Orbs !")
        else:
            await dumpjar(amount, ctx.author)
            users[str(user.id)]["bank"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Jar Of Experience Orbs for {bill} <:slayersgem:785765850862059520>", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    

    elif item.lower() == "common":
        bill = int(amount) * 5000
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           "  Common Loot Crate(s) !")
        else:
            users[str(user.id)]["common"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Common Loot Crate for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) + " Common Loot Crate(s)"
                           " for " + str(bill) + " cash !")
    elif item.lower() == "rare":
        bill = int(amount) * 10000
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Rare Loot Crate(s) !")
        else:
            users[str(user.id)]["rare"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Rare Loot Crate for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) + " Rare Loot Crate(s)"
                           " for " + str(bill) + " cash !")
    elif item.lower() == "epic":
        bill = int(amount) * 50000
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Epic Loot Crate(s) !")
        else:
            users[str(user.id)]["epic"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Epic Loot Crate for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) + " Epic Loot Crate(s)"
                           " for " + str(bill) + " cash !")
    elif item.lower() == "legendary":
        bill = int(amount) * 90000
        wall = users[str(user.id)]["wallet"] - bill
        if wall < 0:
            await ctx.send("Not enough cash to purchase " + str(amount) +
                           " Legendary Loot Crate(s) !")
        else:
            users[str(user.id)]["legendary"] += int(amount)
            users[str(user.id)]["wallet"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Legendary Loot Crate for {bill} :yen:", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) +
                           " Legendary Loot Crate(s)"
                           " for " + str(bill) + " cash !")
    elif item.lower() == "mystical":
        bill = int(amount) * 250
        wall = users[str(user.id)]["bank"] - bill
        if wall < 0:
            await ctx.send("Not enough Slayer's Gems to purchase " +
                           str(amount) + " Mystical Loot Crate(s) !")
        else:
            users[str(user.id)]["mystical"] += int(amount)
            users[str(user.id)]["bank"] -= int(bill)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)
            embed = discord.Embed(description=f"You purchased {amount} Mystical Loot Crate for {bill} <:slayersgem:785765850862059520> Slayer's Gems", color=0x52eb00)
            embed.set_author(name="Successful Purchase", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            await ctx.send("Purhased " + str(amount) +
                           " Mystical Loot Crate(s)"
                           " for " + str(bill) +
                           " <:slayersgem:785765850862059520> Slayer's Gems !")

    elif item.lower() == "crystals":
        await ctx.send(
            "Ancient Crystals cannot be purchased. Obtained from forging")

    else:
        await ctx.send("That item doesn't exist !")
    await ctx.send("Check out the new `t level` command!")

@client.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    if amount < 0:
      embed = discord.Embed(description="Cannot sell a negative quantity of items ", color=0xf00505)
      embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
    else:

        if item == "coal":
            gain = int(amount) * 70
            bagcoal = users[str(user.id)]["coal"]

            if bagcoal < amount:
              embed = discord.Embed(description="Not enough Coal in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              
            else:
                users[str(user.id)]["coal"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                
                embed = discord.Embed(description=f"You sold {amount} Coal for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                

        
        elif item == "ore":
            gain = int(amount) * 625
            bagore = users[str(user.id)]["ore"]

            if bagore < amount:
              embed = discord.Embed(description="Not enough Scarlet Crimson Iron Ore in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              
            else:
                users[str(user.id)]["ore"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                    embed = discord.Embed(description=f"You sold {amount} Scarlet Crimson Iron Ore for {gain} :yen:", color=0x52eb00)
                    embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
               

        elif item == "chunk":
            gain = int(amount) * 210
            bagor = users[str(user.id)]["chunk"]

            if bagor < amount:
              embed = discord.Embed(description="Not enough Scarlet Crimson Iron Ore Chunks in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              
            else:
                users[str(user.id)]["chunk"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                
                embed = discord.Embed(description=f"You sold {amount} Scarlet Crimson Iron Ore Chunk for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                

        elif item == "fragment":
            gain = int(amount) * 100
            bagoree = users[str(user.id)]["fragment"]

            if bagoree < amount:
              embed = discord.Embed(description="Not enough Scarlet Crimson Iron Ore Fragments in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
             
            else:
                users[str(user.id)]["fragment"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                embed = discord.Embed(description=f"You sold {amount} Scarlet Crimson Iron Ore Fragment for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                

        elif item == "sand":
            gain = int(amount) * 500
            bagsand = users[str(user.id)]["sand"]

            if bagsand < amount:
              embed = discord.Embed(description="Not enough Scarlet Crimson Iron Sand in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              
            else:
                users[str(user.id)]["sand"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                
                embed = discord.Embed(description=f"You sold {amount} Scarlet Crimson Iron Sand for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
               

        elif item == "dust":
            gain = int(amount) * 90
            bagsan = users[str(user.id)]["dust"]

            if bagsan < amount:
              embed = discord.Embed(description="Not enough Scarlet Crimson Iron Dust in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              
            else:
                users[str(user.id)]["dust"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                
                embed = discord.Embed(description=f"You sold {amount} Scarlet Crimson Iron Dust for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                

        elif item == "nichirin":
            gain = int(amount) * 22000
            bagnichirin = users[str(user.id)]["nichirin"]

            if bagnichirin < amount:
              embed = discord.Embed(description="Not enough Nichirin Ore in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
            else:
                users[str(user.id)]["nichirin"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                
                embed = discord.Embed(description=f"You sold {amount} Nichirin Ore for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                

        elif item.lower() == "common":
          embed = discord.Embed(description=":gift: Common Loot Crates cannot be sold !", color=0xf00505)
          embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
          
        elif item.lower() == "rare":
          
          embed = discord.Embed(description=":gift: Rare Loot Crates cannot be sold !", color=0xf00505)
          embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
        elif item.lower() == "epic":
          
          embed = discord.Embed(description=":gift: Epic Loot Crates cannot be sold !", color=0xf00505)
          embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
        elif item.lower() == "legendary":
         
          embed = discord.Embed(description=":gift: Legendary Loot Crates cannot be sold !", color=0xf00505)
          embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
        elif item.lower() == "mystical":
          
          embed = discord.Embed(description=":gift: Mystical Loot Crates cannot be sold !", color=0xf00505)
          embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
        elif item.lower() == "crystals":
            gain = int(amount) * 800
            bagcryst = users[str(user.id)]["crystal"]

            if bagcryst < amount:
              embed = discord.Embed(description="Not enough Ancient Crystals in Bag", color=0xf00505)
              embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              
              
            else:
                users[str(user.id)]["crystal"] -= int(amount)
                users[str(user.id)]["wallet"] += int(gain)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                embed = discord.Embed(description=f"You sold {amount} Ancient Crystals for {gain} :yen:", color=0x52eb00)
                embed.set_author(name="Successful Sale", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                
        else:
          embed = discord.Embed(description="That item doesn't exist !\nCheck for the Item ID at the shop !", color=0xf00505)
          embed.set_author(name="Unsuccessful Sale", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
        await ctx.send("Check out the new `t level` command!")


@client.command()
async def bag(ctx, member: discord.Member = None):
  if member == None:
    member = ctx.author
  else:
    pass
  await open_account(member)
  await open_moves(member)
  await open_newitems(member)
  user = member
  users = await get_bank_data()
  users1 = await get_newitems_data()
  res = await invitems(user)
  invcrate = users[str(user.id)]["common"] + users[str(
      user.id)]["rare"] + users[str(user.id)]["epic"] + users[str(
          user.id)]["legendary"] + users[str(user.id)]["mystical"]

  coal_amt = users[str(user.id)]["coal"]
  ore_amt = users[str(user.id)]["ore"]
  sand_amt = users[str(user.id)]["sand"]
  nichirin_amt = users[str(user.id)]["nichirin"]
  common_amt = users[str(user.id)]["common"]
  rare_amt = users[str(user.id)]["rare"]
  epic_amt = users[str(user.id)]["epic"]
  legendary_amt = users[str(user.id)]["legendary"]
  mystical_amt = users[str(user.id)]["mystical"]
  shard_amt = users[str(user.id)]["shard"]
  blade_amt = users[str(user.id)]["blade"]
  crystal_amt = users[str(user.id)]["crystal"]
  chunk_amt = users[str(user.id)]["chunk"]
  fragment_amt = users[str(user.id)]["fragment"]
  dust_amt = users[str(user.id)]["dust"]
  twoamt = users[str(user.id)]["twostar"]
  threeamt = users[str(user.id)]["threestar"]
  fouramt = users[str(user.id)]["fourstar"]
  fiveamt = users[str(user.id)]["fivestar"]
  vial_amt = users1[str(user.id)]["vial"]
  jar_amt = users1[str(user.id)]["jar"]
  keybp_amt = users1[str(user.id)]["keybp"]
  key_amt = users1[str(user.id)]["key"]
  rkey_amt = users1[str(user.id)]["rustykey"]
  
  invcombat = int(twoamt) + int(threeamt) + int(fouramt) + int(
      fiveamt) + int(blade_amt)
  invmat = chunk_amt + fragment_amt + dust_amt + users[str(
      user.id)]["coal"] + users[str(user.id)]["ore"] + users[str(
          user.id)]["sand"] + users[str(user.id)]["nichirin"] + users[str(
              user.id)]["shard"] + users[str(user.id)]["crystal"]

  one = Button(style=ButtonStyle.blue, label="View Materials", id="embed1", emoji="⛏️")
  two = Button(style=ButtonStyle.blue, label="View Loot Crates", id="embed2", emoji="🎁")
  three = Button(style=ButtonStyle.blue, label="View Combat & Other Items", id="embed3", emoji="⚔️")

  embed = discord.Embed(title=f"Viewing {user}'s Bag :briefcase:",
                        color=0xff0000)

  embed.add_field(name=":one:  Materials :pick: (" + str(invmat) + " Items in Bag)",
                  value="View your crafting and selling materials here.",
                  inline=False)
  embed.add_field(name=":two: Loot Crates :gift: (" + str(invcrate) +
                  " Crates in Bag)",
                  value="View owned loot crates here.",
                  inline=True)
  embed.add_field(name=":three: Combat & Others :crossed_swords: (" + str(invcombat) +
                  " Items in Bag)",
                  value="View owned combat related items, artifacts or antique items here.",
                  inline=False)
  embed.add_field(
      name="**Click any button to view items**",
      value="Nothing is wrong if it says \"This interaction failed.\"",
      inline=False)
  embed.set_thumbnail(url=member.avatar_url)
  message = await ctx.send(embed=embed, components=[[one,two,three]])

  


  em1 = discord.Embed(title=f"{member.name}'s Bag", color=0xff0000)
  em1.add_field(name="Materials  :pick:",
                value="Crafting and Selling Materials",
                inline=False)
  em1.add_field(name="Coal ", value=coal_amt, inline=True)
  em1.add_field(name="Nichirin Ore", value=nichirin_amt, inline=True)
  em1.add_field(name="\u200b", value="\u200b", inline=True)
  em1.add_field(name="Scarlet Crimson Iron Ore Fragment",
                value=fragment_amt,
                inline=True)
  em1.add_field(name="Scarlet Crimson Iron Ore Chunk ",
                value=chunk_amt,
                inline=True)
  em1.add_field(name="Scarlet Crimson Iron Ore",
                value=ore_amt,
                inline=True)
  em1.add_field(name="Scarlet Crimson Iron Dust",
                value=dust_amt,
                inline=True)
  em1.add_field(name="Scarlet Crimson Iron Sand",
                value=sand_amt,
                inline=True)
  em1.add_field(name="\u200b", value="\u200b", inline=True)
  em1.add_field(name="Ancient Crystal Shards",
                value=shard_amt,
                inline=True)
  em1.add_field(name="Ancient Crystals", value=crystal_amt, inline=True)
  em1.add_field(name="\u200b", value="\u200b", inline=True)
  


  em2 = discord.Embed(title=f"{member.name}'s Bag", color=0xff0000)
  em2.add_field(name="Loot Crates :gift:",
                value="Owned Loot Crates\n",
                inline=False)
  em2.add_field(name="Common Loot Crate", value=common_amt, inline=True)
  em2.add_field(name="Rare Loot Crate", value=rare_amt, inline=True)
  em2.add_field(name="Epic Loot Crate", value=epic_amt, inline=True)
  em2.add_field(name="Legendary Loot Crate",
                value=legendary_amt,
                inline=True)
  em2.add_field(name="Mystical Loot Crate",
                value=mystical_amt,
                inline=True)
  


  em3 = discord.Embed(title=f"{member.name}'s Bag", color=0xff0000)
  em3.add_field(name="Combat & Miscellaneous :crossed_swords:",
                value="Owned Combat Related And Other Items\n",
                inline=False)
  em3.add_field(name="**THESE ITEMS CANNOT BE USED YET. COMING SOON !** ",
                value="**These are valuable items, so collect them !**",
                inline=True)

  em3.add_field(name="Nichirin Blade", value=blade_amt, inline=True)
  em3.add_field(name="Vial Of Experience Orbs", value=vial_amt, inline=True)
  em3.add_field(name="Artifact Crate Key Blueprint", value=keybp_amt, inline=True)
  em3.add_field(name="Rusty Artifact Crate Key", value=rkey_amt, inline=True)
  em3.add_field(name="Artifact Crate Key", value=key_amt, inline=True)
  em3.add_field(name="★★☆☆☆ Move Scroll", value=twoamt, inline=True)
  em3.add_field(name="★★★☆☆ Move Scroll", value=threeamt, inline=True)
  em3.add_field(name="★★★★☆ Move Scroll", value=fouramt, inline=True)
  em3.add_field(name="★★★★★ Move Scroll", value=fiveamt, inline=True)

  buttons = {"embed1":em1, "embed2":em2,"embed3":em3}
  
  while True:
    res = await client.wait_for("button_click")
    if res.channel is not ctx.channel:
      return
    if res.channel==ctx.channel:
      response = buttons.get(res.component.id)
      if response is None:
        await ctx.send("Something went wrong. Buttons are at testing stage in this bot")
      else:
        await message.edit(embed=response)
  await ctx.send("Check out the new `t level` command!")
      
          
@client.command()
@commands.cooldown(1, 4, commands.BucketType.user)
async def crate(ctx, a: str):
    await open_account(ctx.author)
    await open_moves(ctx.author)
    await open_newitems(ctx.author)
    users = await get_bank_data()
    user = ctx.author
    if a.lower() == "common":

        embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
        embed.add_field(name="Open Loot Crate :gift: ", value="Common Crate")
        embed.add_field(name="Options Available:",
                        value="\u200b",
                        inline=False)
        embed.add_field(name="Open Crate from Bag (" +
                        str(users[str(user.id)]["common"]) +
                        " Common Crates Owned)",
                        value="Respond with 'bag' within 30 seconds",
                        inline=False)
        embed.add_field(name="Pay 5000 :yen: to open Crate instantly",
                        value="Respond with 'pay' within 30 seconds",
                        inline=False)
        embed.add_field(name="Cancel Loot Crate Opening",
                        value="Respond with 'cancel' within 30 seconds",
                        inline=False)

        message = await ctx.send(embed=embed)

        def check(meesg69):
            return meesg69.author == ctx.author and meesg69.channel == ctx.channel and \
            meesg69.content.lower() in ["bag", "cancel", "pay"]

        try:
            meesg69 = await client.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Purchase cancelled.")

        if meesg69.content.lower() == "pay":
            x = users[str(user.id)]["wallet"] - 5000
            if x < 0:
                await ctx.send(
                    "Not enough cash to purchase Crate. Purchase cancelled !")
            else:
                global ccrewards1
                ccrewards1 = [
                    '20 Coal', '4 Scarlet Crimson Iron Sand',
                    '4 Scarlet Crimson Ore', '3000 Cash',
                    '4 Scarlet Crimson Ore', '20 Ancient Crystal Shards',
                    '4 Scarlet Crimson Ore', '20 Coal',
                    '4 Scarlet Crimson Iron Sand'
                ]
                global prize1
                prize1 = random.choice(ccrewards1)
                global prize2
                prize2 = random.choice(ccrewards1)

                users[str(user.id)]["wallet"] -= 5000
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send("Successfully paid 5000 :yen:")

                if prize1 == "20 Coal":
                    users[str(user.id)]["coal"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "4 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "4 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "3000 Cash":
                    users[str(user.id)]["wallet"] += 3000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "20 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if prize2 == "20 Coal":
                    users[str(user.id)]["coal"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "4 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "4 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "3000 Cash":
                    users[str(user.id)]["wallet"] += 3000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "20 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Common Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Common Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Common Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name=":gift: Common Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(prize1) +
                                "`\n`" + str(prize2) +
                                "`\nfrom a Common Loot Crate !!!",
                                value="Reward Credited to Bag",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg69.content.lower() == "bag":
            e = users[str(user.id)]["common"] - 1
            if e < 0:
                await ctx.send("Not enough Common Crates in bag !")
            else:
                global ccrewards2
                ccrewards2 = [
                    '20 Coal', '4 Scarlet Crimson Iron Sand',
                    '4 Scarlet Crimson Ore', '3000 Cash',
                    '4 Scarlet Crimson Ore', '20 Ancient Crystal Shards',
                    '4 Scarlet Crimson Ore', '20 Coal',
                    '4 Scarlet Crimson Iron Sand'
                ]

                prize1 = random.choice(ccrewards2)

                prize2 = random.choice(ccrewards2)
                users[str(user.id)]["common"] -= 1
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                if prize1 == "20 Coal":
                    users[str(user.id)]["coal"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "4 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "4 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "20 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize1 == "3000 Cash":
                    users[str(user.id)]["wallet"] += 3000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if prize2 == "20 Coal":
                    users[str(user.id)]["coal"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "4 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "4 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 4
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "20 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 20
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif prize2 == "3000 Cash":
                    users[str(user.id)]["wallet"] += 3000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Common Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Common Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Common Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2fb125)
                embed.add_field(name=":gift: Common Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(prize1) +
                                "`\n`" + str(prize2) +
                                "`\nfrom a Common Loot Crate !!!",
                                value="Reward Credited to Bag",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg69.content.lower() == "cancel":
            await ctx.send("Crate opening cancelled successfully !")
        else:
            await ctx.send("Invalid Response. Purchase Cancelled !")

    if a.lower() == "rare":

        embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
        embed.add_field(name="Open Loot Crate :gift: ", value="Rare Crate")
        embed.add_field(name="Options Available:",
                        value="\u200b",
                        inline=False)
        embed.add_field(name="Open Crate from Bag (" +
                        str(users[str(user.id)]["rare"]) +
                        " Rare Crates Owned)",
                        value="Respond with `bag` within 20 seconds",
                        inline=False)
        embed.add_field(name="Pay 10000 :yen: to open Crate instantly",
                        value="Respond with `pay` within 20 seconds",
                        inline=False)
        embed.add_field(name="Cancel Loot Crate Opening",
                        value="Respond with `cancel` within 20 seconds",
                        inline=False)

        message = await ctx.send(embed=embed)

        def check(meesg):
            return meesg.author == ctx.author and meesg.channel == ctx.channel and \
            meesg.content.lower() in ["bag", "cancel", "pay"]

        try:
            meesg = await client.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Purchase cancelled.")

        if meesg.content.lower() == "pay":
            x = users[str(user.id)]["wallet"] - 10000
            if x < 0:
                await ctx.send(
                    "Not enough cash to purchase Crate. Purchase cancelled !")
            else:

                rcrewards = [
                    '35 Coal', '10 Scarlet Crimson Iron Sand',
                    '10 Scarlet Crimson Ore', '40 Ancient Crystal Shards',
                    '6000 Cash',
                    "15 Slayer's Gems",
                    '10 Scarlet Crimson Ore', '10 Scarlet Crimson Ore',
                    '35 Coal', '10 Scarlet Crimson Iron Sand'
                ]
                global rprize1
                rprize1 = random.choice(rcrewards)
                global rprize2
                rprize2 = random.choice(rcrewards)

                users[str(user.id)]["wallet"] -= 10000
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send("> Successfully paid 10000 :yen:")

                if rprize1 == "35 Coal":
                    users[str(user.id)]["coal"] += 35
                    
                elif rprize1 == "10 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 10
                    
                elif rprize1 == "10 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 10
                   
                elif rprize1 == "15 Slayer's Gems":
                    users[str(user.id)]["bank"] += 15
                    
                elif rprize1 == "40 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 40
                    
                elif rprize1 == "6000 :yen: Cash":
                    users[str(user.id)]["wallet"] += 6000
                    
                if rprize2 == "35 Coal":
                    users[str(user.id)]["coal"] += 35
                    
                elif rprize2 == "10 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 10
                    
                elif rprize2 == "10 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 10
                    
                elif rprize2 == "15 Slayer's Gems":
                    users[str(user.id)]["bank"] += 15
                    
                elif rprize2 == "40 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 40
                    
                elif rprize2 == "6000 Cash":
                    users[str(user.id)]["wallet"] += 6000
                
                with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Rare Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Rare Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Rare Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name=":gift: Rare Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received \n`" + str(rprize1) +
                                "`\n`" + str(rprize2) +
                                "`\nRewards credited to your bag !",
                                value="As part of our bug hunting program, we request you to view your profile immediately after this, to check if any level/xp/item reset has occured. If so please report it at our support server (`t help` for invite link)",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg.content.lower() == "bag":
            e = users[str(user.id)]["rare"] - 1
            if e < 0:
                await ctx.send("Not enough Rare Crates in bag !")
            else:
                rcrewards1 = [
                    '35 Coal', '10 Scarlet Crimson Iron Sand',
                    '10 Scarlet Crimson Ore', '40 Ancient Crystal Shards',
                    '6000 :yen: Cash',
                    "15 <:slayersgem:785765850862059520> Slayer's Gems",
                    '10 Scarlet Crimson Ore', '10 Scarlet Crimson Ore',
                    '35 Coal', '10 Scarlet Crimson Iron Sand'
                ]
                rprize11 = random.choice(rcrewards1)

                rprize22 = random.choice(rcrewards1)
                users[str(user.id)]["rare"] -= 1
                
                if rprize11 == "35 Coal":
                    users[str(user.id)]["coal"] += 35
                    
                elif rprize11 == "10 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 10
                    
                elif rprize11 == "10 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 10
                    
                elif rprize11 == "15 Slayer's Gems":
                    users[str(user.id)]["bank"] += 15
                   
                elif rprize11 == "40 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 40
                    
                elif rprize11 == "6000 Cash":
                    users[str(user.id)]["wallet"] += 6000
                    

                if rprize22 == "35 Coal":
                    users[str(user.id)]["coal"] += 35
                    
                elif rprize22 == "10 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 10
                    
                elif rprize22 == "10 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 10
                    
                elif rprize22 == "15 Slayer's Gems":
                    users[str(user.id)]["bank"] += 15
                    
                elif rprize22 == "40 Ancient Crystal Shards":
                    users[str(user.id)]["shard"] += 40
                    
                elif rprize22 == "6000 Cash":
                    users[str(user.id)]["wallet"] += 6000
                
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Rare Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Rare Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Rare Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x2670e8)
                embed.add_field(name=":gift: Rare Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received \n`" + str(rprize11) +
                                "`\n`" + str(rprize22) +
                                "`\nRewards credited to your bag !",
                                value="As part of our bug hunting program, we request you to view your profile immediately after this, to check if any level/xp/item reset has occured. If so please report it at our support server (`t help` for invite link)",
                                inline=False)
                await message.edit(embed=embed)

    elif a.lower() == "epic":

        embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
        embed.add_field(name="Open Loot Crate :gift: ", value="Epic Crate")
        embed.add_field(name="Options Available:",
                        value="\u200b",
                        inline=False)
        embed.add_field(name="Open Crate from Bag (" +
                        str(users[str(user.id)]["epic"]) +
                        " Epic Crates Owned)",
                        value="Respond with 'bag' within 30 seconds",
                        inline=False)
        embed.add_field(name="Pay 50000 :yen: to open Crate instantly",
                        value="Respond with 'pay' within 30 seconds",
                        inline=False)
        embed.add_field(name="Cancel Loot Crate Opening",
                        value="Respond with 'cancel' within 30 seconds",
                        inline=False)

        message = await ctx.send(embed=embed)

        def check(meesg691):
            return meesg691.author == ctx.author and meesg691.channel == ctx.channel and \
            meesg691.content.lower() in ["bag", "cancel", "pay"]

        try:
            meesg691 = await client.wait_for("message",
                                             check=check,
                                             timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Purchase cancelled.")

        if meesg691.content.lower() == "pay":
            x = users[str(user.id)]["wallet"] - 50000
            if x < 0:
                await ctx.send(
                    "Not enough cash to purchase Crate. Purchase cancelled !")
            else:
                global ecrewards1
                ecrewards1 = [
                    '100 Coal', '25 Scarlet Crimson Iron Sand',
                    '25 Scarlet Crimson Ore', '25 Ancient Crystals',
                    '15000 Cash', '25 Scarlet Crimson Ore',
                    '25 Scarlet Crimson Ore', '★★☆☆☆ Move Scroll', '100 Coal',
                    '25 Scarlet Crimson Iron Sand', "35 Slayer's Gems",
                    "★★★☆☆ Move Scroll"
                ]
                global eprize1
                eprize1 = random.choice(ecrewards1)
                global eprize2
                eprize2 = random.choice(ecrewards1)
                global eprize3
                eprize3 = random.choice(ecrewards1)

                users[str(user.id)]["wallet"] -= 50000
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send("Successfully paid 50000 :yen:")

                if eprize1 == "100 Coal":
                    users[str(user.id)]["coal"] += 100
                    
                elif eprize1 == "25 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 25
                    
                elif eprize1 == "25 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 25
                    
                elif eprize1 == "15000 Cash":
                    users[str(user.id)]["wallet"] += 15000
                    
                elif eprize1 == "35 Slayer's Gems":
                    users[str(user.id)]["bank"] += 35
                    
                elif eprize1 == "25 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 25
                    
                elif eprize1 == '★★☆☆☆ Move Scroll':
                    users[str(user.id)]["twostar"] += 1
                   
                elif eprize1 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    

                if eprize2 == "100 Coal":
                    users[str(user.id)]["coal"] += 100
                    
                elif eprize2 == "25 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 25
                    
                elif eprize2 == "25 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 25
                    
                elif eprize2 == "15000 Cash":
                    users[str(user.id)]["wallet"] += 15000
                    
                elif eprize2 == "35 Slayer's Gems":
                    users[str(user.id)]["bank"] += 35
                    
                elif eprize2 == "25 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 25
                    
                elif eprize2 == '★★☆☆☆ Move Scroll':
                    users[str(user.id)]["twostar"] += 1
                    
                elif eprize2 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    

                if eprize3 == "100 Coal":
                    users[str(user.id)]["coal"] += 100
                    
                elif eprize3 == "25 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 25
                    
                elif eprize3 == "25 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 25
                    
                elif eprize3 == "15000 Cash":
                    users[str(user.id)]["wallet"] += 15000
                    
                elif eprize3 == "35 Slayer's Gems":
                    users[str(user.id)]["bank"] += 35
                    
                elif eprize3 == "25 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 25
                    
                elif eprize3 == '★★☆☆☆ Move Scroll':
                    users[str(user.id)]["twostar"] += 1
                    
                elif eprize3 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                
                with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                    

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Epic Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Epic Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Epic Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name=":gift: Epic Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(eprize1) +
                                "`\n`" + str(eprize2) + "`\n`" + str(eprize3) +
                                "`\nRewards credited to your bag !",
                                value="As part of our bug hunting program, we request you to view your profile immediately after this, to check if any level/xp/item reset has occured. If so please report it at our support server (`t help` for invite link)",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg691.content.lower() == "bag":
            e = users[str(user.id)]["epic"] - 1
            if e < 0:
                await ctx.send("Not enough Epic Crates in bag !")
            else:
                users[str(user.id)]["epic"] -= 1
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                ecrewards11 = [
                    '100 Coal', '25 Scarlet Crimson Iron Sand',
                    '25 Scarlet Crimson Ore', '25 Ancient Crystals',
                    '15000 Cash', '25 Scarlet Crimson Ore',
                    '25 Scarlet Crimson Ore', '★★☆☆☆ Move Scroll', '100 Coal',
                    '25 Scarlet Crimson Iron Sand', "35 Slayer's Gems",
                    "★★★☆☆ Move Scroll"
                ]
                global eprize11
                eprize11 = random.choice(ecrewards11)
                global eprize21
                eprize22 = random.choice(ecrewards11)
                global eprize33
                eprize33 = random.choice(ecrewards11)
                if eprize11 == "100 Coal":
                    users[str(user.id)]["coal"] += 100
                    
                elif eprize11 == "25 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 25
                    
                elif eprize11 == "25 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 25
                    
                elif eprize11 == "15000 Cash":
                    users[str(user.id)]["wallet"] += 15000
                    
                elif eprize11 == "35 Slayer's Gems":
                    users[str(user.id)]["bank"] += 35
                    
                elif eprize11 == "25 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 25
                    
                elif eprize11 == '★★☆☆☆ Move Scroll':
                    users[str(user.id)]["twostar"] += 1
                   
                elif eprize11 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    

                if eprize22 == "100 Coal":
                    users[str(user.id)]["coal"] += 100
                    
                elif eprize22 == "25 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 25
                    
                elif eprize22 == "25 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 25
                    
                elif eprize22 == "15000 Cash":
                    users[str(user.id)]["wallet"] += 15000
                    
                elif eprize22 == "35 Slayer's Gems":
                    users[str(user.id)]["bank"] += 35
                    
                elif eprize22 == "25 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 25
                    
                elif eprize22 == '★★☆☆☆ Move Scroll':
                    users[str(user.id)]["twostar"] += 1
                    
                elif eprize22 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    

                if eprize33 == "100 Coal":
                    users[str(user.id)]["coal"] += 100
                    
                elif eprize33 == "25 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 25
                    
                elif eprize33 == "25 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 25
                    
                elif eprize33 == "15000 Cash":
                    users[str(user.id)]["wallet"] += 15000
                    
                elif eprize33 == "35 Slayer's Gems":
                    users[str(user.id)]["bank"] += 35
                    
                elif eprize33 == "25 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 25
                    
                elif eprize33 == '★★☆☆☆ Move Scroll':
                    users[str(user.id)]["twostar"] += 1
                    
                elif eprize33 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                
                with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Epic Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Epic Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Epic Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xe901b7)
                embed.add_field(name=":gift: Epic Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(eprize11) +
                                "`\n`" + str(eprize22) + "`\n`" +
                                str(eprize33) +
                                "`\nRewards credited to your bag !",
                                value="As part of our bug hunting program, we request you to view your profile immediately after this, to check if any level/xp/item reset has occured. If so please report it at our support server (`t help` for invite link)",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg691.content.lower() == "cancel":
            await ctx.send("Crate opening cancelled successfully !")
        else:
            await ctx.send("Invalid Response. Purchase Cancelled !")

    elif a.lower() == "legendary":

        embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
        embed.add_field(name="Open Loot Crate :gift: ",
                        value="Legendary Crate")
        embed.add_field(name="Options Available:",
                        value="\u200b",
                        inline=False)
        embed.add_field(name="Open Crate from Bag (" +
                        str(users[str(user.id)]["legendary"]) +
                        " Legendary Crates Owned)",
                        value="Respond with 'bag' within 30 seconds",
                        inline=False)
        embed.add_field(name="Pay 90000 :yen: to open Crate instantly",
                        value="Respond with 'pay' within 30 seconds",
                        inline=False)
        embed.add_field(name="Cancel Loot Crate Opening",
                        value="Respond with 'cancel' within 30 seconds",
                        inline=False)

        message = await ctx.send(embed=embed)

        def check(meesg692):
            return meesg692.author == ctx.author and meesg692.channel == ctx.channel and \
            meesg692.content.lower() in ["bag", "cancel", "pay"]

        try:
            meesg692 = await client.wait_for("message",
                                             check=check,
                                             timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Purchase cancelled.")

        if meesg692.content.lower() == "pay":
            x = users[str(user.id)]["wallet"] - 90000
            if x < 0:
                await ctx.send(
                    "Not enough  to purchase Crate. Purchase cancelled !")
            else:
                global lcrewards1
                lcrewards1 = [
                    '180 Coal', '45 Ancient Crystals',
                    '50 Scarlet Crimson Iron Sand',
                    '50 Scarlet Crimson Iron Sand', '30000 Cash', '180 Coal',
                    '45 Scarlet Crimson Ore', '45 Ancient Crystals',
                    '30000 Cash', '180 Coal', '45 Scarlet Crimson Ore',
                    '45 Scarlet Crimson Ore', '180 Coal',
                    '50 Scarlet Crimson Iron Sand', "40 Slayer's Gems",
                    "★★★☆☆ Move Scroll", '★★★★☆ Move Scroll'
                ]
                global lprize1
                lprize1 = random.choice(lcrewards1)
                global lprize2
                lprize2 = random.choice(lcrewards1)
                global lprize3
                lprize3 = random.choice(lcrewards1)
                global lprize4
                lprize4 = random.choice(lcrewards1)

                users[str(user.id)]["wallet"] -= 90000
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send("Successfully paid 90000 :yen:")

                if lprize1 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize1 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if lprize2 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize2 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if lprize3 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize3 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if lprize4 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize4 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Legendary Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Legendary Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Legendary Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name=":gift: Legendary Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(lprize1) +
                                "`\n`" + str(lprize2) + "`\n`" + str(lprize3) +
                                "`\n`" + str(lprize4) +
                                "`\nfrom a Legendary Loot Crate !!!",
                                value="Reward Credited to Bag",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg692.content.lower() == "bag":
            e = users[str(user.id)]["legendary"] - 1
            if e < 0:
                await ctx.send("Not enough Legendary Crates in bag !")
            else:
                users[str(user.id)]["legendary"] -= 1
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                global lcrewards11
                lcrewards11 = [
                    '180 Coal', '45 Ancient Crystals',
                    '50 Scarlet Crimson Iron Sand',
                    '50 Scarlet Crimson Iron Sand', '30000 Cash', '180 Coal',
                    '45 Scarlet Crimson Ore', '45 Ancient Crystals',
                    '30000 Cash', '180 Coal', '45 Scarlet Crimson Ore',
                    '45 Scarlet Crimson Ore', '180 Coal',
                    '50 Scarlet Crimson Iron Sand', "40 Slayer's Gems",
                    "★★★☆☆ Move Scroll", '★★★★☆ Move Scroll'
                ]
                global lprize11
                lprize11 = random.choice(lcrewards11)
                global lprize22
                lprize22 = random.choice(lcrewards11)
                global lprize33
                lprize33 = random.choice(lcrewards11)
                global lprize44
                lprize44 = random.choice(lcrewards11)

                if lprize11 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize11 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if lprize22 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize22 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if lprize33 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize33 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if lprize44 == "180 Coal":
                    users[str(user.id)]["coal"] += 180
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == "50 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == "45 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == "30000 Cash":
                    users[str(user.id)]["wallet"] += 30000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == "40 Slayer's Gems":
                    users[str(user.id)]["bank"] += 40
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == "45 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 45
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif lprize44 == '★★★☆☆ Move Scroll':
                    users[str(user.id)]["threestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Legendary Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Legendary Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Legendary Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0xffa70f)
                embed.add_field(name=":gift: Legendary Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(lprize11) +
                                "`\n`" + str(lprize22) + "`\n`" +
                                str(lprize33) + "`\n`" + str(lprize44) +
                                "`\nfrom a Legendary Loot Crate !!!",
                                value="Reward Credited to Bag",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg692.content.lower() == "cancel":
            await ctx.send("Crate opening cancelled successfully !")
        else:
            await ctx.send("Invalid Response. Purchase Cancelled !")

    elif a.lower() == "mystical":

        embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
        embed.add_field(name="Open Loot Crate :gift: ", value="Mystical Crate")
        embed.add_field(name="Options Available:",
                        value="\u200b",
                        inline=False)
        embed.add_field(name="Open Crate from Bag (" +
                        str(users[str(user.id)]["mystical"]) +
                        " Mystical Crates Owned)",
                        value="Respond with 'bag' within 30 seconds",
                        inline=False)
        embed.add_field(
            name=
            "Pay 250 <:slayersgem:785765850862059520> to open Crate instantly",
            value="Respond with 'pay' within 30 seconds",
            inline=False)
        embed.add_field(name="Cancel Loot Crate Opening",
                        value="Respond with 'cancel' within 30 seconds",
                        inline=False)

        message = await ctx.send(embed=embed)

        def check(meesg693):
            return meesg693.author == ctx.author and meesg693.channel == ctx.channel and \
            meesg693.content.lower() in ["bag", "cancel", "pay"]

        try:
            meesg693 = await client.wait_for("message",
                                             check=check,
                                             timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Purchase cancelled.")

        if meesg693.content.lower() == "pay":
            x = users[str(user.id)]["bank"] - 250
            if x < 0:
                await ctx.send(
                    "Not enough Slayer's Gems to purchase Crate. Purchase cancelled !"
                )
            else:
                global mcrewards1
                mcrewards1 = [
                    '200 Coal', '60 Ancient Crystals',
                    '70 Scarlet Crimson Iron Sand', "★★★★★ Move Scroll",
                    '70 Scarlet Crimson Iron Sand', '40000 Cash', '200 Coal',
                    '65 Scarlet Crimson Ore', '60 Ancient Crystals',
                    '40000 Cash', '200 Coal', '65 Scarlet Crimson Ore',
                    '65 Scarlet Crimson Ore', '200 Coal',
                    '70 Scarlet Crimson Iron Sand', "50 Slayer's Gems",
                    "★★★★★ Move Scroll", '★★★★☆ Move Scroll'
                ]
                global mprize1
                mprize1 = random.choice(mcrewards1)
                global mprize2
                mprize2 = random.choice(mcrewards1)
                global mprize3
                mprize3 = random.choice(mcrewards1)
                global mprize4
                mprize4 = random.choice(mcrewards1)
                global mprize5
                mprize5 = random.choice(mcrewards1)

                users[str(user.id)]["bank"] -= 250
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                await ctx.send(
                    "Successfully paid 250 <:slayersgem:785765850862059520> Slayer's Gems"
                )

                if mprize1 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize1 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize2 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize2 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize3 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize3 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize4 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize4 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize5 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize5 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Mystical Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Mystical Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Mystical Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name=":gift: Mystical Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(mprize1) +
                                "`\n`" + str(mprize2) + "`\n`" + str(mprize3) +
                                "`\n`" + str(mprize4) + "`\n`" + str(mprize5) +
                                "`\nfrom a Mystical Loot Crate !!!",
                                value="Reward Credited to Bag",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg693.content.lower() == "bag":
            e = users[str(user.id)]["mystical"] - 1
            if e < 0:
                await ctx.send("Not enough Mystical Crates in bag !")
            else:
                users[str(user.id)]["mystical"] -= 1
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                global mcrewards11
                mcrewards11 = [
                    '200 Coal', '60 Ancient Crystals',
                    '70 Scarlet Crimson Iron Sand', "★★★★★ Move Scroll",
                    '70 Scarlet Crimson Iron Sand', '40000 Cash', '200 Coal',
                    '65 Scarlet Crimson Ore', '60 Ancient Crystals',
                    '40000 Cash', '200 Coal', '65 Scarlet Crimson Ore',
                    '65 Scarlet Crimson Ore', '200 Coal',
                    '70 Scarlet Crimson Iron Sand', "50 Slayer's Gems",
                    "★★★★★ Move Scroll", '★★★★☆ Move Scroll'
                ]
                global mprize11
                mprize11 = random.choice(mcrewards11)
                global mprize22
                mprize22 = random.choice(mcrewards11)
                global mprize33
                mprize33 = random.choice(mcrewards11)
                global mprize44
                mprize44 = random.choice(mcrewards11)
                global mprize55
                mprize55 = random.choice(mcrewards11)

                if mprize11 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize11 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize22 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize22 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize33 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize33 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize44 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize44 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                if mprize55 == "200 Coal":
                    users[str(user.id)]["coal"] += 200
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == "70 Scarlet Crimson Iron Sand":
                    users[str(user.id)]["sand"] += 70
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == "65 Scarlet Crimson Ore":
                    users[str(user.id)]["ore"] += 65
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == "40000 Cash":
                    users[str(user.id)]["wallet"] += 40000
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == "50 Slayer's Gems":
                    users[str(user.id)]["bank"] += 50
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == "60 Ancient Crystals":
                    users[str(user.id)]["crystal"] += 60
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == '★★★★☆ Move Scroll':
                    users[str(user.id)]["fourstar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)
                elif mprize55 == '★★★★★ Move Scroll':
                    users[str(user.id)]["fivestar"] += 1
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Mystical Loot Crate **.**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Mystical Loot Crate **. .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name="Open Loot Crate :gift: ",
                                value="Opening Mystical Loot Crate **. . .**")
                await message.edit(embed=embed)
                await asyncio.sleep(0.8)

                embed = discord.Embed(title="Loot Crates ", color=0x6d08e7)
                embed.add_field(name=":gift: Mystical Crate Rewards",
                                value="\u200b",
                                inline=False)
                embed.add_field(name="You received :\n`" + str(mprize11) +
                                "`\n`" + str(mprize22) + "`\n`" +
                                str(mprize33) + "`\n`" + str(mprize44) +
                                "`\n`" + str(mprize55) +
                                "`\nfrom a Mystical Loot Crate !!!",
                                value="Reward Credited to Bag",
                                inline=False)
                await message.edit(embed=embed)

        elif meesg692.content.lower() == "cancel":
            await ctx.send("Crate opening cancelled successfully !")
        else:
            await ctx.send("Invalid Response. Purchase Cancelled !")
    else:
        pass


@crate.error
async def crate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited to **once per 4 seconds** !\nPlease **try again in {:.2f} seconds**!'.format(
            error.retry_after)
        await ctx.send(msg)
    else:
        raise error


#forging


@client.command()
async def forge(ctx, fitem="a", amount=1):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    fcoal = users[str(user.id)]["coal"]
    fore = users[str(user.id)]["ore"]
    fsand = users[str(user.id)]["sand"]
    fnichirin = users[str(user.id)]["nichirin"]
    fcrystals = users[str(user.id)]["crystal"]
    fdust = users[str(user.id)]["dust"]
    ffragment = users[str(user.id)]["fragment"]
    if fitem == "a":
        embed = discord.Embed(title="**Forging and Crafting :hammer_pick: ** ", color=0x2fb125)
       
        embed.add_field(name="Craft, Make and Forge various items !\nForge an item by: `t forge <Item ID> <Quantity>`",
                        value="\u200b",
                        inline=False)
        embed.add_field(
            name="**:one:  Ancient Crystals ** ",
            value=
            "**ID**-`crystal` |  Ancient Crystals which enhance the forging process.\n**Materials Required :**\n```✧ 5 Ancient Crystal Shards\n✧ 2 Coal```",
            inline=False)
        embed.add_field(
            name="**:two:  Nichirin Ore ** ",
            value=
            "**ID**-`nichirin` |  A peculiar alloy forged using Scarlet Crimson Ore and Iron Sand.\n**Materials Required :**\n```✧ 20 Scarlet Crimson Ore\n✧ 20 Scarlet Crimson Iron Sand\n✧ 25 Coal\n✧ 10 Ancient Crystal```",
            inline=False)
        embed.add_field(
            name="**:three:  Scarlet Crimson Iron Ore Chunk **",
            value=
            "**ID**-`chunk` | A chunk of a bright red ore that constantly absorbs sunlight.\n**Materials Required :**\n```✧ 4 Scarlet Crimson Iron Ore Fragment \n✧ 8 Ancient Crystals\n✧ 8 Coal```",
            inline=False)
        
        
        embed.set_thumbnail(
            url=
            "https://i.imgur.com/u5EwQKT.png"
        )
        embe = discord.Embed(title="**Forging and Crafting :hammer_pick: ** ", color=0x2fb125)
       
        embe.add_field(name="Craft, Make and Forge various items !",
                        value="\u200b",
                        inline=False)
        embe.add_field(
            name="**:four:  Scarlet Crimson Iron Sand **",
            value=
            "ID-`dust` |   Bright red iron sand that constantly absorbs sunlight.\n**Materials Required :**\n```✧ 5 Scarlet Crimson Iron Dust\n✧ 5 Ancient Crystals\n✧ 3 Coal```",
            inline=False)
        embe.add_field(
            name="**:five:  Scarlet Crimson Iron Ore **",
            value=
            "ID-`ore` |  A bright red ore that constantly absorbs sunlight.\n**Materials Required :**\n```✧ 2 Scarlet Crimson Iron Chunk\n✧ 5 Ancient Crystals\n✧ 3 Coal```",
            inline=False)

        embe.add_field(
            name="**:six:  Nichirin Blade :crossed_swords: **",
            value=
            "ID-`blade` |  A sturdy sword specially used for slaying demons.\n**Materials Required :**\n```✧ 3 Nichirin Ore\n✧ 25 Ancient Crystals\n✧ 50 Coal```", 
            inline=False)
        embe.set_thumbnail(
            url=
            "https://i.imgur.com/u5EwQKT.png")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("\U00002b05")
        await msg.add_reaction("\U000027a1")

        @client.event
        async def on_reaction_add(reaction, user):
          emoji = reaction.emoji
          if user.bot:
              return

          if emoji == "\U000027a1" and user == ctx.author:
            await msg.edit(embed=embe)
          if emoji == "\U00002b05" and user == ctx.author:
            await msg.edit(embed=embed)




    elif fitem.lower() == "nichirin":
        newfsand1 = fsand - (20 * amount)
        newfore1 = fore - (20 * amount)

        newfcrystals1 = fcrystals - (10 * amount)
        if newfsand1 < 0 or newfore1 < 0 or newfcrystals1 < 0 or users[str(
                user.id)]["coal"] - (25 * amount) < 0:
            await ctx.send("**Insufficient materials to forge " + str(amount) +
                           " Nichirin Ore !**")
        elif int(amount) < 0:
            await ctx.send("You cannot forge a negative quantity of items !")
        else:
            embed1 = discord.Embed(description=f"You are about to forge {amount} Nichirin Ore for {20*amount} Scarlet Crimson Iron Ore, {20*amount} Scarlet Crimson Iron Sand, {25*amount} Coal and {10*amount} Ancient Crystals.\nProceed ?", color=0x52eb00)
            embed1.set_author(name="Forge Nichirin Ore", icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=embed1)
            await msg.add_reaction("\U00002705")

            @client.event
            async def on_reaction_add(reaction, user):

              emoji = reaction.emoji
              if user.bot:
                  return

              if emoji == "\U00002705" and user == ctx.author:
                users[str(user.id)]["ore"] -= (20 * int(amount))
                users[str(user.id)]["sand"] -= (20 * int(amount))
                users[str(user.id)]["crystal"] -= (10 * int(amount))
                users[str(user.id)]["coal"] -= (25 * int(amount))
                users[str(user.id)]["nichirin"] += int(amount)
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)
                embed = discord.Embed(description=f"You forged {amount} Nichirin Ore for {20*amount} Scarlet Crimson Iron Ore, {20*amount} Scarlet Crimson Iron Sand, {25*amount} Coal and {10*amount} Ancient Crystals", color=0x52eb00)
                embed.set_author(name="Successful Forge", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            

    elif fitem.lower() == "crystal":
        fshards2 = users[str(user.id)]["shard"] - (5 * amount)
        fcoal2 = users[str(user.id)]["coal"] - (2 * amount)
        if fshards2 < 0 or fcoal2 < 0:
            await ctx.send(f"**Insufficient materials to forge {amount} Ancient Crystal(s) !**\nMissing Materials :\n{-1*fshards2} Ancient Crystal Shards, {-1*fcoal2} Coal")
        elif int(amount) < 0:
            await ctx.send("You cannot forge a negative quantity of items !")
        else:
            embed1 = discord.Embed(description=f"You are about to forge {amount} Ancient Crystals for {5*amount} Ancient Crystal Shards and {2*amount} Coal.\nProceed ?", color=0x52eb00)
            embed1.set_author(name="Forge Ancient Crystals", icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=embed1)
            await msg.add_reaction("\U00002705")

            @client.event
            async def on_reaction_add(reaction, user):

              emoji = reaction.emoji
              if user.bot:
                  return

              if emoji == "\U00002705" and user == ctx.author:
                users[str(user.id)]["shard"] -= (5 * int(amount))
                users[str(user.id)]["coal"] -= (2 * int(amount))
                users[str(user.id)]["crystal"] += (1 * int(amount))
                with open("mainbank.json", "w") as f:
                    json.dump(users, f)

                embed = discord.Embed(description=f"You forged {amount} Ancient Crystals for {5*amount} Ancient Crystal Shards and {2*amount} Coal", color=0x52eb00)
                embed.set_author(name="Successful Forge", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            

    elif fitem.lower() == "sand":
        fcrys2 = int(users[str(user.id)]["crystal"]) - (8 * amount)
        fcoal2 = users[str(user.id)]["coal"] - (8 * amount)
        fdust = users[str(user.id)]["dust"] - (5 * amount)
        if fcrys2 < 0 or fcoal2 < 0 or fdust < 0:
            await ctx.send("**Insufficient materials to forge " + str(amount) +
                           " Scarlet Crimson Iron Sand !**")
        elif int(amount) < 0:
            await ctx.send("You cannot forge a negative quantity of items !")
        else:
            users[str(user.id)]["crystal"] -= (8 * int(amount))
            users[str(user.id)]["coal"] -= (8 * int(amount))
            users[str(user.id)]["dust"] -= (5 * int(amount))
            users[str(user.id)]["sand"] += (1 * amount)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)

            await ctx.send("Successfully forged " + str(amount) +
                           " Scarlet Crimson Iron Sand !")

    elif fitem.lower() == "chunk":
        fcrys2 = int(users[str(user.id)]["crystal"]) - (8 * amount)
        fcoal2 = users[str(user.id)]["coal"] - (8 * amount)
        fdust = users[str(user.id)]["fragment"] - (4 * amount)
        if fcrys2 < 0 or fcoal2 < 0 or fdust < 0:
            await ctx.send("**Insufficient materials to forge " + str(amount) +
                           " Scarlet Crimson Iron Ore Chunk !**")
        elif int(amount) < 0:
            await ctx.send("You cannot forge a negative quantity of items !")
        else:
            users[str(user.id)]["crystal"] -= (8 * int(amount))
            users[str(user.id)]["coal"] -= (8 * int(amount))
            users[str(user.id)]["fragment"] -= (4 * int(amount))
            users[str(user.id)]["chunk"] += (1 * amount)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)

            await ctx.send("Successfully forged " + str(amount) +
                           " Scarlet Crimson Iron Ore Chunk !")

    elif fitem.lower() == "blade":
        fnichirin3 = users[str(user.id)]["nichirin"] - 2
        fcrystal3 = users[str(user.id)]["crystal"] - 25
        fcoal3 = users[str(user.id)]["coal"] - 50
        if fnichirin3 < 0 or fcrystal3 < 0:
            await ctx.send("**Insufficient materials to forge " + str(amount) +
                           " Nichirin Blade !**")
        elif int(amount) < 0:
            await ctx.send("You cannot forge a negative quantity of items !")
        elif int(amount) > 1:
            await ctx.send(
                "You cannot forge or own more than 1 Nichirin Blade at a  time !"
            )
        elif users[str(user.id)]["blade"] >= 1:
            await ctx.send(
                "You cannot own more than 1 Nichirin Blade at a  time !")

        else:

            users[str(user.id)]["crystal"] -= (25 * int(amount))
            users[str(user.id)]["nichirin"] -= (2 * int(amount))
            users[str(user.id)]["coal"] -= (50 * int(amount))
            users[str(user.id)]["blade"] += int(amount)
            with open("mainbank.json", "w") as f:
                json.dump(users, f)

            await ctx.send("Successfully forged " + str(amount) +
                           " Nichirin Blade !")
    else:
        await ctx.send("That Item doesn't exist !")


@client.command()
async def moves(ctx):
    embed = discord.Embed(title="View All Available Moves Here",
                          description="\u200b",
                          color=0xf02424)
    embed.set_author(name="Demon Slayer Movesets")
    embed.add_field(name="Breathing Styles", value="\u200b", inline=False)
    embed.add_field(
        name=":one: Total Concentration Breathing",
        value=
        "(Zen Shūchū no Kokyū), an advanced application of Breathing, is a state where a Breathing Style user inhales the maximum amount of oxygen within a specific breath pattern to raise their physical and mental prowess to their utmost limits. It is often used by Demon Slayers for a brief moment to temporarily boost their combat capabilities to prepare a decisive attack.",
        inline=False)
    embed.add_field(
        name="Moves:",
        value=
        "Total Concentration: Constant\nA Total Concentration Breathing state during the morning, noon, and night, and even while asleep that Advanced Demon Slayers, such as Hashira, can constantly maintain",
        inline=False)
    embed.add_field(
        name=":two: Water Breathing",
        value=
        "(Mizu no kokyū) is one of the five main Breathing Styles directly derived from the Sun Breathing."
    )
    embed.add_field(
        name="Moves:",
        value=
        "**First Form: Water Surface Slash**\n(Ichi no kata: Minamo Giri) - The swordsman generates enough momentum to create a powerful single concentrated slash.\n**Second Form: Water Wheel**\n(Ni no kata: Mizu Guruma) - The swordsman leaps and vertically spins forward in the air while releasing a flowing attack in a circular motion.",
        inline=False)
    embed.set_image(
        url=
        "https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/7/75/Anime_Slide.png/revision/latest/scale-to-width-down/670?cb=20201019160419"
    )
    await ctx.send(embed=embed)


@client.command()
async def mymvs(ctx):

    await open_moves(ctx.author)
    user = ctx.author
    users = await get_moves_data()

    wmv1 = users[str(user.id)]["Wform1"]
    wmv2 = users[str(user.id)]["Wform2"]
    wmv3 = users[str(user.id)]["Wform3"]
    wmv4 = users[str(user.id)]["Wform4"]
    wmv5 = users[str(user.id)]["Wform5"]
    wmv6 = users[str(user.id)]["Wform6"]
    wmv7 = users[str(user.id)]["Wform7"]
    wmv8 = users[str(user.id)]["Wform8"]
    wmv9 = users[str(user.id)]["Wform9"]
    wmv10 = users[str(user.id)]["Wform10"]
    wmv11 = users[str(user.id)]["Wform11"]
    tmv12 = users[str(user.id)]["Tform1.1"]
    tmv11 = users[str(user.id)]["Tform1.2"]
    tmv2 = users[str(user.id)]["Tform2"]
    tmv3 = users[str(user.id)]["Tform3"]
    tmv4 = users[str(user.id)]["Tform4"]
    tmv5 = users[str(user.id)]["Tform5"]
    tmv6 = users[str(user.id)]["Tform6"]
    tmv7 = users[str(user.id)]["Tform7"]

    em = discord.Embed(title=str(user) + "'s Owned Moves", color=0xb90e9c)
    em.add_field(
        name=
        ":one: Total Concentration Breathing - 5 ★ Avg Rating | 1 Move Under Category",
        value="View Unlocked Total Concentration Breathing Moves",
        inline=False)
    em.add_field(
        name=
        ":two: Water Breathing - 3.09 ★ Avg Rating | 11 Moves Under Ctegory",
        value="View Unlocked Water Breathing Moves",
        inline=False)
    em.add_field(name=":three: Thunder Breathing - 3.375 ★ Avg Rating",
                 value="View Unlocked Thunder Breathing Moves",
                 inline=False)
    message = await ctx.send(embed=em)

    def check(g):
        return g.author == ctx.author and g.channel == ctx.channel and \
        g.content.lower() in ["1", "2", "3", "cancel"]

    try:
        g = await client.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send(
            "You didn't reply in time. Unlocked moves menu closed due to inactivity"
        )

    if g.content.lower() == "2":
        em = discord.Embed(title=str(user) + "'s Owned Moves", color=0xb90e9c)
        em.add_field(name="Water Breathing - 3.09 ★ Avg Rating",
                     value="Water Breathing Moves Owned")
        if wmv1 == 69.420:
            em.add_field(
                name="First Form: Water Surface Slash",
                value="★★☆☆☆ | **DMG :** 35 - 50 | **Special Buffs:** None",
                inline=False)
        else:
            pass
        if wmv2 == 69.420:
            em.add_field(
                name="Second Form: Water Wheel",
                value=
                "★★★☆☆ | **DMG :** 25 - 35 | **Special Buffs:** Lands 3 simultaneous hits on the enemy",
                inline=False)
        else:
            pass
        if wmv3 == 69.420:
            em.add_field(
                name="Third Form: Flowing Dance",
                value=
                "★★☆☆☆ | **DMG :** 9 - 12 | **Special Buffs:** Lands 3-5 simultaneous hits on the enemy",
                inline=False)
        else:
            pass
        if wmv4 == 69.420:
            em.add_field(
                name="Fourth Form: Striking Tide",
                value=
                "★★★☆☆ | **DMG :** 30 - 40 | **Special Buffs:** CRIT Rate way up! CRIT DMG + 25",
                inline=False)
        else:
            pass
        if wmv5 == 69.420:
            em.add_field(
                name="Fifth Form: Blessed Rain After the Drought",
                value=
                "★★★☆☆ | **DMG :** 35 - 50 | **Special Buffs :** 15% Chance to instant kill enemy. *May not work on bosses*",
                inline=False)
        else:
            pass
        if wmv6 == 69.420:
            em.add_field(
                name="Sixth Form: Whirlpool",
                value=
                "★★★★☆ | **DMG :** 10 - 15 | **Special Buffs:** Lands 6 Simultaneous hits on enemy ",
                inline=False)
        else:
            pass
        if wmv7 == 69.420:
            em.add_field(
                name="Seventh Form: Piercing Rain Drop",
                value=
                "★★★★☆ | **DMG :** 45 - 75 | **Special Buffs :** 25% Chance to instant kill enemy. *May not work on bosses*",
                inline=False)
        else:
            pass
        if wmv8 == 69.420:
            em.add_field(
                name="Eighth Form: Waterfall Basin",
                value=
                "★★☆☆☆ | **DMG :** 25 - 35 | **Special Buffs: ** 30% Chance to deal 10 extra DMG",
                inline=False)
        else:
            pass
        if wmv9 == 69.420:
            em.add_field(
                name="Ninth Form: Splashing Water Flow",
                value=
                "★★★☆☆ | **DMG :** 30 - 45 | **Special Buffs:** 35 % Chance to deal 10 DMG quick shots when its *not your turn*",
                inline=False)
        else:
            pass
        if wmv10 == 69.420:
            em.add_field(
                name="Tenth Form: Constant Flux",
                value=
                "★★★☆☆ | **DMG :** First Shot : 5, Last Shot: 30 | **Special Buffs:** Deals 4 consecutive hits, DMG increasing each hit",
                inline=False)
        else:
            pass
        if wmv11 == 69.420:
            em.add_field(
                name="Eleventh Form: Dead Calm",
                value=
                "★★★★★ | **DMG : **90 | **Special Buffs:** 100% DMG Reduction for all hits sustained for the next 20 seconds",
                inline=False)
        else:
            pass

        if wmv1 != 69.420 and wmv2 != 69.420 and wmv3 != 69.420 and wmv4 != 69.420 and wmv5 != 69.420 and wmv6 != 69.420 and wmv7 != 69.420 and wmv8 != 69.420 and wmv9 != 69.420 and wmv10 != 69.420 and wmv11 != 69.420:
            em.add_field(name="No Water Breathing Moves Unlocked",
                         value="Collect more moves by opening Loot Crates !")
        em.set_image(
            url=
            "https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/3/32/Water_Breathing_%28Zenshuchuten%29.png/revision/latest/scale-to-width-down/200?cb=20200524143708"
        )
        await message.edit(embed=em)

    elif g.content.lower() == "3":
        em = discord.Embed(title=str(user) + "'s Owned Moves", color=0xb90e9c)
        em.add_field(name="Thunder Breathing - 3.375 ★ Avg Rating",
                     value="Unlocked Thunder Breathing Moves")
        if tmv11 == 69.420:
            em.add_field(
                name=
                "First Form: Thunderclap and Flash - Six Fold / Eight Fold",
                value=
                "★★☆☆☆ | **DMG : **7 - 8 | **Special Buffs:** Deals 6 or 8  consecutive hits on the enemy",
                inline=False)
        else:
            pass
        if tmv12 == 69.420:
            em.add_field(
                name="First Form: Thunderclap and Flash - God Speed",
                value=
                "★★★★☆ | **DMG : **55 | **Special Buffs:** 25% chance to deal 200% DMG",
                inline=False)
        else:
            pass
        if tmv2 == 69.420:
            em.add_field(
                name="Second Form: Rice Spirit ",
                value=
                "★★★☆☆ | **DMG : **8 X5 times | **Special Buffs:** 5% chance to stun enemy for next 15 seconds",
                inline=False)
        else:
            pass
        if tmv3 == 69.420:
            em.add_field(
                name="Third Form: Thunder Swarm",
                value=
                "★★★★☆ | **DMG : **65 | **Special Buffs:**5% chance to instant kill enemy",
                inline=False)
        else:
            pass
        if tmv4 == 69.420:
            em.add_field(
                name="Fourth Form: Distant Thunder",
                value=
                "★★★☆☆ | **DMG : **10 X5 times | **Special Buffs:** 25 % DMG reduction from hits sustained for one turn.",
                inline=False)
        else:
            pass
        if tmv5 == 69.420:
            em.add_field(
                name="Fifth Form: Heat Lightning",
                value="★★☆☆☆ | **DMG : **35 - 40 | **Special Buffs:**None",
                inline=False)
        else:
            pass
        if tmv6 == 69.420:
            em.add_field(
                name="Sixth Form: Rumble and Flash",
                value=
                "★★★★☆ | **DMG : **10 X6 times | **Special Buffs:** 15% chance to deal 250% DMG",
                inline=False)
        else:
            pass
        if tmv7 == 69.420:
            em.add_field(
                name="Seventh Form: Honoikazuchi no Kami",
                value=
                "★★★★★| **DMG : **90 | **Special Buffs:** 45% chance to deal 200% DMG",
                inline=False)
        else:
            pass
        if tmv11 != 69.420 and tmv12 != 69.420 and tmv2 != 69.420 and tmv3 != 69.420 and tmv4 != 69.420 and tmv5 != 69.420 and tmv6 != 69.420 and tmv7 != 69.420:
            em.add_field(name="No Thunder Breathing Moves Unlocked",
                         value="Collect more moves by opening Loot Crates !",
                         inline=False)
        em.set_image(
            url=
            "https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/0/00/Thunder_Breathing_%28Zenshuchuten%29.png/revision/latest/scale-to-width-down/200?cb=20200524144723"
        )
        await message.edit(embed=em)
    elif g.content.lower() == "cancel":
        await message.edit("Unlocked Moves Menu Closed")

    else:
        pass


@client.command(aliases=['mission', 'msn'])
async def missions(ctx, field=None, field2=None):
    users = await get_moves_data()
    use = await get_bank_data()
    user = ctx.author

    res = await levels(user)

    uselvl = res[0]

    if field == None:
        embed = discord.Embed(title="Play missions assigned to you here !",
                              color=0xff0000)
        embed.set_author(name="Slayer Corps Missions")
        embed.add_field(
            name="\u200b",
            value=
            "**Warning :** You can die in missions meaning you'll *lose ~50% of all items in your bag* ! Proceed with caution, following all minimum requirements ! If you fail missions, you will *lose experience orbs and fined*\n",
            inline=False)
        if int(users[str(user.id)]["swordlvl"]) < 1 or int(uselvl) < 3:
            embed.add_field(
                name=":one: **Forest Scares**",
                value=
                "Word has spread that a demon is lurking in the dense forest...If this continues, the people cannot access the forest for their needs.\n\n**Minimum Mission Requirements Satisfied : **:x:",
                inline=False)

        else:
            embed.add_field(
                name=":one: **Forest Scares**",
                value=
                "Word has spread that a demon is lurking in the dense forest...If this continues, the people cannot access the forest for their needs.\n\n**Minimum Mission Requirements Satisfied : **:white_check_mark:",
                inline=False)

        if int(users[str(user.id)]["swordlvl"]) < 3 or int(uselvl) < 7:
            embed.add_field(
                name="\n:two: **Mysterious Disappearances**",
                value=
                "Reported cases of missing people are rising ! Could it be the work of a nasty demon? It's up to you to unravel this mystery !\n\n**Minimum Mission Requirements Satisfied : **:x:",
                inline=False)
        else:
            embed.add_field(
                name="\n:two: **Mysterious Disappearances**",
                value=
                "Reported cases of missing people are rising ! Could it be the work of a nasty demon? It's up to you to unravel this mystery !\n\n**Minimum Mission Requirements Satisfied : **:white_check_mark:",
                inline=False)

        embed.add_field(
            name=
            "\nTo view more about a mission and its minimum player requirements, run :\n`t missions view <mission number>\n` Or to accept a mission, run :\n`Work In Progress Feature`",
            value=
            "**Have a great idea for a new mission? Drop it by on our [support server](https://discord.gg/H6d5kUhue5) !**"
        )
        await ctx.send(embed=embed)
    else:
        pass

    if field == "view":
        if field2 == None:
            await ctx.send(
                "You need to mention a valid mission to view like this: `t missions accept <mission number>` !"
            )
        elif field2 == "1":
            embed = discord.Embed(title="**View Mission Details**",
                                  color=0xfb0e0e)
            if int(users[str(user.id)]["swordlvl"]) < 1 or int(uselvl) < 3:
                embed.add_field(
                    name="**:one: Forest Scares**",
                    value=
                    "Word has spread that a demon is lurking in the dense forest...If this continues, the people cannot access the forest for their needs.\nMinimum Mission Requirements Satisfied : :x:",
                    inline=False)
            else:
                embed.add_field(
                    name="**:one: Forest Scares**",
                    value=
                    "Word has spread that a demon is lurking in the dense forest...If this continues, the people cannot access the forest for their needs.\n\n**Minimum Mission Requirements Satisfied :** :white_check_mark:",
                    inline=False)

            embed.add_field(name="**Minimum Level Restriction :**", value="3")
            embed.add_field(name="**Minimum Slayer Corps Rank :**",
                            value="Mizunoe | Rank IX")

            embed.add_field(name="**Mission Difficulty :**",
                            value="Easy",
                            inline=True)
            embed.add_field(name="Recommended Equipment :",
                            value="Level 1 Nichirin Blade",
                            inline=True)
            embed.add_field(
                name="**Mission Objective :**",
                value=
                " To locate and eliminate the demon terrorizing the region")
            embed.add_field(
                name="**Mission Rewards :**",
                value="8000 :yen:\n5 <:slayersgem:785765850862059520>")
            await ctx.send(embed=embed)

        elif field2 == "2":
            embed = discord.Embed(title="**View Mission Details**",
                                  color=0xfb0e0e)
            embed.add_field(
                name=":two: **Mysterious Disappearances**",
                value=
                "Reported cases of missing people are rising ! Could it be the work of a nasty demon? It's up to you to unravel this mystery !",
                inline=False)
            embed.add_field(name="**Minimum Level Restriction :**", value="7")
            embed.add_field(name="**Minimum Slayer Corps Rank :**",
                            value="Kanoto | Rank VIII")

            embed.add_field(name="**Mission Difficulty :**",
                            value="Medium",
                            inline=True)
            embed.add_field(
                name="Recommended Equipment :",
                value="Level 3 Nichirin Blade\n★★☆☆☆ Unlocked Move",
                inline=True)
            embed.add_field(
                name="**Mission Objective :**",
                value=
                " To investigate the cause of the disappearings and to learn what happened to the missing."
            )
            embed.add_field(
                name="**Mission Rewards :**",
                value="15000 :yen:\n15 <:slayersgem:785765850862059520>")
            await ctx.send(embed=embed)

        else:
            pass

    elif field == "accept":
        if field2 == None:
            await ctx.send(
                "You need to mention a valid mission to accept like this: `t missions view <mission number>` !"
            )

        elif field2 == "1":
            global reqs1
            if int(users[str(user.id)]["swordlvl"]) < 1 or int(uselvl) < 3:
                reqs1 = False
            else:
                if users[str(user.id)]["engaged"] == False:
                    reqs1 = True

                else:
                    reqs1 = "a"

            if reqs1 == True:
                message = await ctx.send(
                    "Accept Mission :one: - **Forest Scares** ?\n**Make sure you've read the mission details at `t missions view 1` before starting. If you haven't, please cancel the prompt and view the details !**\n**WARNING**: You cannot exit the mission or run other commands unless you complete it or die in the process ! If you abandon the mission, you'll be fined an amount !\n**Respond with `accept` or `cancel` in 45 seconds**"
                )

                def check(m1):
                    return m1.author == ctx.author and m1.channel == ctx.channel and \
                    m1.content.lower() in ["accept","cancel"]

                try:
                    m1 = await client.wait_for("message",
                                               check=check,
                                               timeout=45)
                except asyncio.TimeoutError:
                    await ctx.send(
                        "Mission accept prompt closed due to inactivity")

                if m1.content.lower() == "accept":
                    await ctx.send(
                        "**Mission Accepted | :one:  Forest Scares**")
                    await asyncio.sleep(1.5)
                    await ctx.send(
                        "**Current Objective:** Talk with the people and gather information !"
                    )
                    await asyncio.sleep(1.5)
                    await ctx.send(
                        "**Who do you want to talk to?** - `shopkeeper` / `old lady` / `bystander` (Respond with an option in 20 seconds !)\n**WARNING: ** You can only talk to one person ! Each person gives a unique clue varying from not helpful to helpful clues ! Choose carefully !"
                    )
            elif reqs1 == "a":
                await ctx.send("You are currently engaged in another mission !"
                               )
            else:
                await ctx.send(
                    "You do not satisfy the minimum requirements to go on this mission !\nCome back once you are **Level 3** and have a **Level 1 Nichirin Blade**"
                )
        elif field2 == "2":
            global reqs2
            if int(users[str(user.id)]["swordlvl"]) < 3 or int(uselvl) < 7:
                reqs2 = False
            else:
                reqs2 = True
            if reqs2 == True:
                await ctx.send(
                    "Accept Mission :two: - **Mysterious Disappearances** ?\n**Make sure you've read the mission details at `t missions view 2` before starting**\n**WARNING**: You cannot exit the mission unless you complete it or die in the process ! If you abandon the mission, you'll be fined an amount !"
                )

            else:
                await ctx.send(
                    "You do not satisfy the minimum requirements to go on this mission !\nCome back once you are **Level 7** and have a **Level 3 Nichirin Blade**"
                )
        else:
            pass

    elif field == None:
        pass
    else:
        await ctx.send(
            "That attribute of the `missions` command doesn't exist !")


@client.command()
async def challenge(ctx, member: discord.Member):
    global health1
    health1 = 100

    global health2
    health2 = 100
    challenge = ctx.author.mention
    await ctx.send(f"{challenge} has challenged {member.mention} !")
    while health1 > 0 and health2 > 0:
        challenger = ctx.author.mention
        dmg1 = random.randrange(50)
        dmg2 = random.randrange(50)
        message = await ctx.send(
            str(ctx.author.mention) +
            " , what do you want to do? Respond with sword/surrender/end.")

        def check(ga):
            return ga.author == ctx.author and ga.channel == ctx.channel and \
            ga.content.lower() in ["sword", "surrender", "end"]

        try:
            ga = await client.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Challenge discontinued")
            break

        if ga.content == "sword":
            await ctx.send(
                str(ctx.author.mention) +
                " used a nichirin sword and slashed {member.mention}")
            health2 = health2 - dmg1
            await ctx.send(f"{member.mention} HP - " + str(dmg1) + ", " +
                           str(health2) + " remaining !")
            if health2 <= 0:
                await ctx.send(
                    str(ctx.author.mention) +
                    " won the challenge against {member.mention}")
                break
            else:
                pass
        else:
            pass

        messa = await ctx.send(
            f"{member.mention}, what do you want to do? Respond with sword/surrender/end."
        )

        def check(mga69):
            return mga69.author == member and mga69.channel == ctx.channel and \
            mga69.content.lower() in ["sword", "surrender", "end"]

        try:
            mga69 = await client.wait_for("messa", check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You didn't reply in time. Challenge discontinued")

        if mga69.content == "sword":
            await ctx.send(
                f"{member.mention} used a nichirin sword and slashed {challenger}"
            )
            health1 = health1 - dmg2
            if health1 < 0:
                health1 = 0
            else:
                pass
            await ctx.send(f"{challenger} HP - " + str(dmg2) + ", " +
                           str(health1) + " remaining !")
            if health1 <= 0:
                break
                await ctx.send(
                    f"{member.mention} won the challenge against {challenger}")
                break
            else:
                pass
        else:
            pass


@client.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    else:
        pass
    created_at = member.created_at.strftime("%d %B %Y")
    jat = member.joined_at.strftime("%d %B %Y")
    pfp = member.avatar_url
    discid = member.id
    name = member
    global nick
    if member.display_name == member.name:
      nick = "No Nickname Here"
    else:
      nick = member.display_name
    usn = member.name
    disc = member.discriminator
    embed = discord.Embed(title="User Information", color=0x07e3f2)
    embed.set_author(name=name, icon_url=pfp)
    embed.add_field(name="User Name", value=usn)
    embed.add_field(name="User ID", value=discid, inline=True)
    embed.add_field(name="User Discriminator",
                    value="#" + str(disc),
                    inline=True)
    embed.add_field(name="Account Created On", value=created_at, inline=True)

    
    embed.add_field(name="Server Nickname", value=nick)
    embed.add_field(name="Joined Server On", value=f"{jat}", inline=True)
    embed.add_field(name="Top Role On Server",
                    value=f"{member.top_role.mention}",
                    inline=True)
    

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


@client.command(pass_context=True, aliases=["clear"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=limit)
    clearmsg = await ctx.send(
        str(limit) + ' messages cleared by {}'.format(ctx.author.mention))
    await asyncio.sleep(2)
    await clearmsg.delete()


@purge.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to perform this action.\nMissing Permissions: `Manage_Messages`"
        )


@client.command(aliases=["si"])
async def serverinfo(ctx, server: discord.Guild = None):
    if server == None:
        server = ctx.guild
    else:
        pass

    create = server.created_at.strftime("%b %d, %Y")
    logourl = server.icon_url
    logo = server.icon
    owner = server.owner
    sid = server.id
    count = server.member_count
    active = server.max_presences
    chans = server.text_channels
    vc = server.voice_channels
    vcc = len(vc)
    cats = len(server.categories)
    chancount = len(chans)
    member = ctx.guild.member_count
    
    bans = await server.bans()
    emojis = await server.fetch_emojis()
    embed = discord.Embed(title="Server Information", color=0x07e3f2)
    embed.set_author(name=server, icon_url=logourl)
    embed.add_field(name="Server Name", value=server)
    embed.add_field(name="Server Region", value=str(server.region).capitalize())
    embed.add_field(name="Server ID", value=sid, inline=True)
    embed.add_field(name="Server Created", value=create, inline=True)
    embed.add_field(name="Server Icon URL",
                    value="[Click Here]({})".format(logourl),
                    inline=True)
    embed.add_field(name="Server Member Count",
                    value=f"<:members:826433096676671499> {member} Members",
                    inline=True)
    embed.add_field(name="Categories & Channel Count", value=f"<:category:826430086885933057> {cats} Categories\n<:voicechannel:826427969412136980> {vcc} Voice Channels\n<:textchannel:826427185509171220> {chancount} Text Channels", inline=True)

    embed.add_field(name="Server Security",
                    value=f"Verification Level - {str(server.verification_level).capitalize()} \nExplicit Content Filter - {str(server.explicit_content_filter).capitalize()}\n2FA - {str(bool(server.mfa_level)).capitalize()}",
                    inline=True)

    embed.add_field(name="Other Info", value=f":no_entry: {len(bans)}  Banned Members\n:fleur_de_lis: {len(emojis)}  Custom Emojis", inline=False)
    
    
   

    embed.set_thumbnail(url=server.icon_url)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    perm_list = [perm[0] for perm in user.guild_permissions if perm[1]]
    if "administrator" in perm_list:
        await ctx.send(
            "<:xs:818502085326405652> Target is a Moderator/Admin. Cannot kick a target with `Administrator` Permissions !"
        )
    elif str(user.id) == str(767624993507901470):
        await ctx.send("<:xs:818502085326405652> Cannot kick myself. Mention someone else to kick !")

    elif user == ctx.author:
        await ctx.send("<:xs:818502085326405652> You cannot kick yourself !")
    else:

        await user.kick(reason=reason)
        embed = discord.Embed(
            title=
            f":no_entry:  {user.name}#{user.discriminator} was kicked successfully !",
            color=0xff7b00)
        embed.set_author(name="Kicked " + str(user.name) + "#" +
                         str(user.discriminator),
                         icon_url=user.avatar_url)
        embed.add_field(name="Defaulter :", value=user.mention, inline=True)
        embed.add_field(name="Responsible Moderator :",
                        value=ctx.author.mention,
                        inline=True)
        embed.add_field(name="Reason :", value=reason, inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.message.delete()
        await ctx.channel.send(embed=embed)
        await user.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
    if "administrator" in perm_list:
        await ctx.send(
            "<:xs:818502085326405652> Target is a Moderator/Admin . Cannot ban a target with `Administrator` permissions !"
        )
    elif str(member.id) == str(767624993507901470):
        await ctx.send("<:xs:818502085326405652> Cannot ban myself. Mention someone else to ban !")

    elif member == ctx.author:
        await ctx.send("<:xs:818502085326405652> You cannot ban yourself !")

    else:
        try:

          embed = discord.Embed(
            title=
            f":no_entry:  {member.name}#{member.discriminator} was banned  !",
            color=0xec1313)
          embed.set_author(name="Banned " + str(member.name) + "#" +
                          str(member.discriminator),
                          icon_url=member.avatar_url)
          embed.add_field(name="Defaulter :", value=member.mention, inline=True)
          embed.add_field(name="Responsible Moderator :",
                          value=ctx.author.mention,
                          inline=True)
          embed.add_field(name="Reason :", value=reason, inline=True)
          embed.set_thumbnail(url=member.avatar_url)
          await member.send(embed=embed)
          await member.ban(reason=reason)
          
          await ctx.message.delete()
          await ctx.channel.send(embed=embed)
          
          
        except Exception as err:
          print(err)
        


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to perform this action.\nMissing Permissions: `Kick_Members`"
        )


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to perform this action.\nMissing Permissions: `Ban_Members`"
        )


@client.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    else:
        pass
    formats = ["jpg", "png", "jpeg", "webp"]
    webplink = member.avatar_url_as(static_format="webp")
    pnglink = member.avatar_url_as(static_format="png")
    jpglink = member.avatar_url_as(static_format="jpg")
    giflink = member.avatar_url
    embed = discord.Embed(color=0x000000)
    embed.set_author(name=str(member.name) + "#" + str(member.discriminator) +
                     "'s Avatar",
                     icon_url=pnglink)
    if str(member.avatar_url).endswith(".gif?size=1024"):
      embed.add_field(name="Avatar URLs", value=f"[GIF]({giflink})")
    else:

      embed.add_field(name="Avatar URLs", value=f"[JPG]({jpglink})  | [PNG]({pnglink}) | [WEBP]({webplink})")
                    

    embed.set_image(url=pnglink)
    await ctx.send(embed=embed)


@client.command(aliases=["tc"])
async def tradecurrency(ctx, member: discord.Member):

    await open_account(member)
    await open_account(ctx.author)
    users = await get_bank_data()
    c1 = users[str(ctx.author.id)]["wallet"]
    c2 = users[str(member.id)]["wallet"]
    g1 = users[str(ctx.author.id)]["bank"]
    g2 = users[str(member.id)]["bank"]
    embed = discord.Embed(
        title="Cash & Gems :yen:  <:slayersgem:785765850862059520>",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
    )
    embed.set_author(
        name="Currency Trades",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
    )
    embed.add_field(
        name="Player Trade Request :briefcase:",
        value=str(ctx.author.mention) +
        "** would like to trade currencies with " + str(member.mention) +
        " !**\n React with :white_check_mark: to accept or :x: to deny the trade request ! ",
        inline=False)
    req = await ctx.send(embed=embed)

    await req.add_reaction("\u2705")
    await req.add_reaction("\u274C")

    @client.event
    async def on_reaction_add(reaction, user):

        emoji = reaction.emoji
        if user.bot:
            return

        if emoji == "\u2705":

            embe = discord.Embed(
                title="Cash & Gems :yen:  <:slayersgem:785765850862059520>",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
                color=0xedde02)
            embe.set_author(
                name="Currency Trades",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
            )
            embe.add_field(
                name="Accepted Trade Request :briefcase: :white_check_mark:",
                value=str(member.mention) +
                "** has accepted to trade currencies with " +
                str(ctx.author.mention) +
                " !**\n Enter items to be traded in the format `<cash/gems> <quantity>` !",
                inline=False)
            embe.add_field(name=str(ctx.author) + "'s Offer",
                           value="`Not Ready`",
                           inline=True)
            embe.add_field(name=str(member) + "'s Offer",
                           value="`Not Ready`",
                           inline=True)
            embe.add_field(
                name=
                "To lock your offer and be ready, react with :lock:\nTo cancel the trade, react with :x:",
                value="\u200b",
                inline=True)

            newr = await req.edit(embed=embe)

            await req.clear_reaction("\u2705")
            await req.clear_reaction("\u274C")
            await req.add_reaction("\u274C")
            await req.add_reaction("\U0001F512")

            new_msg = await ctx.channel.fetch_message(req.id)
            use = await new_msg.reactions[0].users().flatten()

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                msg.author not in use

            msg = await client.wait_for("message", check=check)
            if msg.content.lower() == "cash":
                await ctx.send(
                    "You offered cash! How much cash are you offerring? Enter a valid number within your balance ("
                    + str(c1) + " :yen:)")
            elif msg.content.lower() == "gems":
                await ctx.send(
                    "You offered slayer's gems! How many gems are you offerring? Enter a valid number within your balance ("
                    + str(g1) + " <:slayersgem:785765850862059520>)")

        elif emoji == "\u274C":
            emb = discord.Embed(
                title="Cash & Gems :yen:  <:slayersgem:785765850862059520>",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
                color=0xf40606)
            emb.set_author(
                name="Currency Trades",
                url=
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
            )
            emb.add_field(name="Rejected Trade Request  :briefcase::x:",
                          value=str(member.mention) +
                          "** has rejected to trade currencies with " +
                          str(ctx.author.mention) + " !**",
                          inline=False)
            await req.edit(embed=emb)
            await req.clear_reaction("\u2705")
            await req.clear_reaction("\u274C")

        else:
            return

@client.command()
async def test(ctx):
  await ctx.send("✯")

@client.command()
async def use(ctx, item=None):
    await open_moves(ctx.author)
    user = ctx.author
    users = await get_moves_data()
    
  

  
    if item == None:

        await ctx.send(
            "You need to mention an item to use!\nCurrently usable items: Move Scrolls (`twostarscroll` , `threestarscroll` , `fourstarscroll`, `fivestarscrolL`)"
        )
    elif item.lower() == "fivestarscroll" or item.lower() == "fivestar":
      res = await invitems(user)
      bagscroll = res[15]
      if bagscroll < 1:
        embed = discord.Embed(description="Item '`★★★★★` Move Scroll' not in bag ", color=0xf00505)
        embed.set_author(name="Cannot Use Item", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
      else:

        fs = ["Ẃ̵̨̢̹̩̩̰́̊ä̷̟̫͎̗̩̱́̆͛̈́͠t̴̹͕͔̟̬̿͝e̶͉̮̦͈̰̓̅͝r̸̭̲̖̠̊͛̄͆̾̈͐̋͜ ̷̘̙̲̳̞̩̩͓͑͛́́̄́͗͗̚͝B̷̺̜̤̯̖͈̻̦̀̈́̅ȓ̷̩͚̽̍̚e̷̢̥̙̬̒͌̿͒̐̀̾̓̚͝ͅǎ̵̭̲͒̍́̀͠ţ̸̧̬̳̯̬͈̥̘͕̋ḩ̸͋̅̈́̑̂̀̔̕i̸̻̜͌̍͊̂͊̈̕͠n̶̨̡̛̛̗̣̭̳̤̣̹̬̓͗͑͘̕g̴̹̻̞̮͈͚̾̋́̂̓ ̵̡̞̘̺̤́̀̉̑̊͘͝Ḙ̶͎̱̏́ļ̷̭̫̥̬͚͚͑̈́̆̍͊̿͛́͝e̸͎̳̐̿v̵͍͎̘͊͆̊̓̔̓͝ë̸̤͇̼̖́̈́̏ṉ̴̫̮̂̇͗́̎͜ẗ̵̠̭͕̰̓̓͗̒̚h̷̬͓̤̫͓̥̺͓̻͉̉͋̐̇͌́̏͘ ̷̠̱͚͔̗̍͌͊̑̈͑̇͠F̷̢̮̹̙̰̖͓̆o̴̧͚͎̪̹͐́̊̇̍̊r̴̩̒m̷͉͇̲̯̪͂͐̂̍̅̃̽͌͜͝͝ ̸̣̥͈́̚͠:̸̗͕̩̫̟͌̆́̑̈́̈́̌͋̄͝ ̵̰͔̭͓̜̤̈D̵̢̙͖̼̝̠̜̆̿͗̾͗̉̏̿̈́͠ȩ̴̛̭̩͕̩͖̬̦̓̉̃̀̔̾̽̅̕ȃ̷̡̔̏̋̓d̷̨̹͕̦̞̪̯͔͐͜ ̶̭̪̝̫̙̖̼̦̈͋̈͑C̴͚̩̖͓̖̼̤̈́̀̉̈́̈́͂͌a̵̤̱̪͐͐́̃̽̈́̂͛̕l̴̖̤̯̔́̈̒͐m̵̧̯̗̩̽͆̋̀̔̃͘͘", "Ṫ̵̢̧͎̟̼̯̩̟̓͊̄ḩ̴̛̖̰̥̭̖̟̝̈́̄ǔ̵̪̞̺̠̤̞͍̩̔̌̏n̸͓̰̫̼̈́̓̈́ḓ̴̨̜͖̯͍͆͆͌̄̒̕͝ͅe̸̢̡̨͉͔̹̻͈̟̲͗̕r̸̛͓̎̈͊̓͌̓̚͝͝ ̵͙̥̙͚̉̋͑͒̐͠B̶̛͖̥̘̙̘͐͋͊͂̌̀̃̾r̸̡͉̮̣͍̊̍́̕e̴̛̬͈͑̉̄͑͒̉̓͠ą̵̥͓̝̙͒̈͛͊͌̔̏͘͜t̵̙́̑̈͗̚h̶͕̘̝̭͔̱̅͜ͅi̶͍̞̐̇̉̉ñ̶͇̖̰̲́͒̒́͊̓͘͠g̷̛͎͎̼͉͓̦͗̌̌̅̓̃̓̕ ̸͔̺͛̅̇̄̾͗̚͜͝S̸̜̆̊̔͆̽̕ě̵̘̄́̒v̵̡̖͕͍̭̹͉͐̀̾͂͂̈͛͝ͅḙ̴̡̮͓̖͊̀̍͗́̇͋̽ṇ̷̨̝͙̈́̓͌t̶̲͎͔̣̥͔̾̾͗̅̆̃h̵̠̲͓͍̄͌̊̐ ̷̡̱̠̫͇͌̐͛͝F̷̤͈̙̲̦͎́ȏ̵͕̻̺̰̄̀̕ͅr̴͓͕͖̓̆̀̚͘̕m̴̡͕̙̼̼̰̉̓̌̔̿̈͝:̶̡̛͔͕̿͆͐͠ ̶̯͐̐̈́̒̃͜Ĥ̶̟̳̫̙̣͍̺̥͙̓͒͑̇͜o̸̜͕̝͙͕̝͖͋̓̓̕͝ṇ̶̭̱̖̝̝͔̣̲̐͂̒͜o̷͙̙͓͙̣̎́̆̑ͅi̸̢̱̜̣̐̃̈̀̕k̷͔̠͖͉̙̠̖̟̋͋́͑̎͠a̶̟̥͙̼͈͝z̴̛̩͙̮̟̞ͅͅu̸̥̲̦͗͗́̎̓̃͂͗̽̚͜c̸̢̫̯̥̲̺͖̋̎̎̄̽̿̀̌͆̈́ͅͅh̵̛̲̏͗̇̈̄́͘͝i̸͉̭̻̦͇̾̓̂́͆̕ ̴̢̗̟̩̯͖̺̣͚͋͒͛͂̍ǹ̷̡̾̂̅͜o̷̢̥̎̿̌̐̾ ̴̡̫͉͊̓̎͐̊̀K̸̺̥̜̭̖̟̼̦̪͐̂͆͛̍̈́̒̊̕a̶͎͇̚m̸̡͖̗͉̗̊͊͒̿̈́̈́̕͝͝į̸̡̞̜̞͙̗͚͎̽̈́͒͒̆͆", ":̶̡͚̺̠͚̞̠́̐͆̎͜|̶̡͗̓̀̒͐̀͠:̵͉̘̫̮̹̘͇̽͘͜͝|̵̞̠̈̀͊́͛̀̔̇̃̀:̷̖̯̈́̑̄̇̆̀͊:̷̣͔̈́͑̆͐̚|̴̮̗̝͔̹͕̯̈̒̾̂̂:̴̛̰̝̒͝|̴̬͔̺͚̩̯͌͗͗̽͂̿͘̚|̵̛̗̼͎̝̗̣̬͔̆̾͊̕͝>̴̫͈̩̖̞̙͈̝̤̒|̷̡͎̮̖̓̋̒̎̃<̷̤̦͂̎̾́̍́́͘͠>̴̨̗͚̞̤̙̺̅̐͋͒͗̽͜≯̛͍̺̱̤̘̽͆͆̓̈́͊̑͝͝ͅ:̵̡̢̡͍͍͛|̷̛̣̮̜̗͔͖̏̅:̸̞̣̜̝̣̥̲̆̋͊͠|̷̨͔̪̞̼̻̦͉͐̈́|̸͍͍̭̎̄̈́͒͛̔̔̔̌>̶̘̗̯̤̖̎͌>̴̦̭̣̜̮̠̪͍̫̿̋̏̀̇̈́̈́̐.̵̛̻͍̱̫̜͉̦̀̽̈́̈́͗́͂̚}̶̭̥̜̥̘̭̣̱̅̓̇͊̽̆̈̕͝͠{̸̡̤͇̭͉̭̼̀͂̇̈͘}̸̠͓̰̑̍͑͆͌̉̑̇͑̀{̸̢̢̜̩̘͓̙̯͙̞́̆͊̀͊̐̓̀̊͛|̷̢͙͎͕͇̄̾͋̒̑͂͂̎͜:̶͇̰̫̜̃̐̃́̔͂̃͐̇͠:̴̧̠̞̞̫̼̭̣̟̾̏͊̄̒͆̈́̒́̅|̷͙̣̜̩́̉̎́̋̕>̴̫̲̳͓͚͔̺͐̍̍̎̿̏̍̕|̵̦͕̾̃͌̕͠:̶̲̬̠̩͇̺̪̺̩̦̒̄̋͑̄̚}̸̧̢͚͈̙͆̓:̶̧̡̡͓͙̝͕̉͜}̴̨̛̲̝̳͈̙̲̠͂̈́ͅ.̶̡̪̈́̔̿̚/̸̜̘̼͍̉͗̒̊͒̋͠\̶̛̯̣̦̱̦̜̒̈́͂͂̚͘͜/̶̯̤̙̩̳͎̐͜'̶̢̤͍̘̘̬̿͜}̴̛̰͙̮̗̘͈̱͕̱̝̔̅͋̒̈́̑̈́̕;̷̧̻̠͔͎̪̥̯̹̔̋̌͜", "|̵̡̨̛̟̝̩̺̪͙͔͗̌̓̾̈́̽̀͆͑|̵͕̃|̶̛͉̖̀͌̒:̷̭̫̻̞̻̞̠̈́̉̃̆̍̎|̴͓̹͖̙̹͉̩͈̙̭̓̓͠:̶͍̳͇̠̙̤̅̄̋̂̽̌>̴͍̤͕̼̝͊͒̌͐͋̂̈̕̕͜<̶̡̍̃̀̒͐͛͝͠|̶̜̤͈̞͓̤͂:̷̝͚̫͈̘͆͆̚.̷̠͐͛̃̈́|̴̨̭̙̪̰̲̹̯̹͍̉̔͆̅͗͗̒̚|̵̡̨̻̭͍͚͇̹̂̿́̉͐̾̈̈́͘͜ͅ:̴̡̢̹̎̓̎̈́́́|̸̡̹̰̠̖̪͋̃̒͌ͅ:̷̧̧̪̰͈̣̤̫͇̀̄̍̊̄}̵̪̈̃̉͗̃͝͝ͅ[̶̛͎͓͙̤̭͕̦̀̑̈́͂̓͋`̶̭͍̼͕̄̍̊̋͝\̸̱͔̲̦͕̼̞̞̓̎̅̽̏͌͗̚ͅ`̶̧̛̂̉͠͠|̵̲͚̊̊̒͂͂̌̔̕͝~̷̡̮͉̺̦̖͔͙̔̐\̷̯͉̌̐̇̋̐̒`̴̭̩̖̠̬̖̦̣͌̐\̴̛̞̪̥̩̀̀͗ͅͅ`̸̭͍̮̪̰̭͛͗͒̇̔͛̑͜ͅ\̸̧̨̝̙̟̤̗͖̼̓͜~̴̺̣̎̋̍͊̂͂̾|̵̬̭͍̩̼̯̹̋̒̋͗̾`̴̧̺͔̩̏̌̔̽̓̿̊̓̓"]

        fmoves = ["Water Breathing Eleventh Form : Dead Calm", "Thunder Breathing Seventh Form : Honoikazuchi no Kami", "Total Concentration Breathing : Constant"]
        
      
        embed=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
        embed.add_field(name="Proceed?", value="React with :white_check_mark:", inline=False)
        pr = await ctx.send(embed=embed)
        await pr.add_reaction("\U00002705")

        @client.event
        async def on_reaction_add(reaction, user):

          emoji = reaction.emoji
          if user.bot:
              return

          if emoji == "\U00002705" and user == ctx.author:
            res1 = await invitems(user)
            bagscroll1 = res1[15]
            await pr.clear_reaction("\U00002705")
            x1 = random.choice(fs)
            embe1=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe1.add_field(name="Deciphering Scroll .", value=f"```{x1}```", inline=False)
            x2 = random.choice(fs)
            embe2=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe2.add_field(name="Deciphering Scroll ..", value=f"```{x2}```", inline=False)
            x3 = random.choice(fs)
            embe3=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe3.add_field(name="Deciphering Scroll ...", value=f"```{x3}```", inline=False)
            x4 = random.choice(fs)
            embe4=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe4.add_field(name="Deciphering Scroll .", value=f"```{x4}```", inline=False)
            x5 = random.choice(fs)
            embe5=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe5.add_field(name="Deciphering Scroll ..", value=f"```{x5}```", inline=False)
            x6 = random.choice(fs)
            embe6=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe6.add_field(name="Deciphering Scroll ...", value=f"```{x6}```", inline=False)
            m5 = random.choice(fmoves)
            embe7=discord.Embed(title="Teachings Of The Scroll :scroll:", description="**You are about to learn a move from a `★★★★★` scroll**", color=0xfc941d)
            embe7.add_field(name="Scroll Deciphered ! You learnt to use :", value=f"```asciidoc\n= {m5} =```", inline=False)
            bagscroll1 -= 1
            await asyncio.sleep(0.5)
            await pr.edit(embed=embe1)
            await asyncio.sleep(0.5)
            await pr.edit(embed=embe2)
            await asyncio.sleep(0.6)
            await pr.edit(embed=embe3)
            await asyncio.sleep(0.7)
            await pr.edit(embed=embe4)
            await asyncio.sleep(0.7)
            await pr.edit(embed=embe5)
            await asyncio.sleep(0.7)
            await pr.edit(embed=embe6)
            await asyncio.sleep(0.7)
            global wmv11
            wmv11 = users[str(user.id)]["Wform11"]
            global tmv7
            tmv7 = users[str(user.id)]["Tform7"]
            global tcmv1
            tcmv1 = users[str(user.id)]["TCform1"]
            if m5 == "Water Breathing Eleventh Form : Dead Calm" and wmv11 == 0:
              wmvll += 69.420
              with open("moves.json", "w") as f:
                          json.dump(users, f)
            else:
              pass
            if m5 == "Total Concentration Breathing : Constant" and tcmv1 == 0:
              tcmv1 += 69.420
              with open("moves.json", "w") as f:
                          json.dump(users, f)
            else:
              pass
            if m5 == "Thunder Breathing Seventh Form : Honoikazuchi no Kami" and tmv7 == 0:
              tmv7 += 69.420
              with open("moves.json", "w") as f:
                          json.dump(users, f)
            else:
              pass
            with open("moves.json", "w") as f:
                          json.dump(users, f)
            
            await pr.edit(embed=embe7)
    elif item.lower() == "rare" or item.lower() == "rare crate" or item.lower() == "rare loot crate":
      await ctx.send("Loot crates have a seperate command to be used !\nTo open them, run `t crate <crate rarity>`\nFor example : `t crate rare` to open a rare loot crate.")
    
    elif item.lower() == "common" or item.lower() == "common crate" or item.lower() == "common loot crate":
      await ctx.send("Loot crates have a seperate command to be used !\nTo open them, run `t crate <crate rarity>`\nFor example : `t crate common` to open a common loot crate.")
          



@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(":lock: Channel " + str(channel.mention) +
                   " has been locked successfully !")

@client.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
  async with ctx.channel.typing():
    for channel in ctx.guild.channels:

      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f":lock: This server is now under lockdown. `{len(ctx.guild.text_channels)}` channels have been locked")

@client.command()
@commands.has_permissions(manage_channels=True)
async def removelockdown(ctx):
  async with ctx.channel.typing():
    for channel in ctx.guild.channels:
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = True
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f":unlock: The server lockdown has now been ended.\n `{len(ctx.guild.text_channels)}` channels have been unlocked")


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(":unlock: Channel " + str(channel.mention) +
                   " has been unlocked successfully !")


@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to lock channels.\nMissing Permissions: `Manage Channels`"
        )


@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to unlock channels.\nMissing Permissions: `Manage Channels`"
        )

@lockdown.error
async def lockdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to lockdown the server.\nMissing Permissions: `Manage Channels`"
        )


@unlock.error
async def removelockdown_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to end lockdowns on this server.\nMissing Permissions: `Manage Channels`"
        )


@client.command()
@commands.has_permissions(manage_channels=True,
                          manage_roles=True,
                          manage_messages=True)
async def mute(ctx,
               member: discord.Member = None,
               *,
               reason="No reason provided"):
    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role == None:
        role = await ctx.guild.create_role(name="Muted",
                                           reason="Atla Bot Mute Role")
    else:
      pass
    
    if role in member.roles:
        await ctx.send(f":mute: {member} is already muted !")
    else:
        await member.add_roles(role)
        embed = discord.Embed(
            color=0xffdd00)
        embed.set_author(name="\U0001f507 Muted " + str(member.name) + "#" +
                        str(member.discriminator),
                        icon_url=member.avatar_url)
        
        embed.add_field(name="Responsible Moderator :",
                        value=ctx.author.mention,
                        inline=True)
        embed.add_field(name="Duration :", value="Indefinite ∞", inline=True)
        embed.add_field(name="Reason :", value=reason, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.message.delete()
        await ctx.channel.send(embed=embed)
        if not member.bot:
          await member.send(embed=embed)

        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)

@client.command()
async def unmute(ctx,
               member: discord.Member = None,
               *,
               reason="No reason provided"):

    role = discord.utils.get(ctx.guild.roles, name="Muted")

    if role == None:
        role = await ctx.guild.create_role(name="Muted",
                                           reason="Atla Bot Mute Role")
    else:
      pass
    
    if role not in member.roles:
        await ctx.send(f"{member} is not muted !")
    else:
      await member.remove_roles(role)
      embe = discord.Embed(
                   color=0x92e000)
      embe.set_author(name="\U0001f50a Unmuted " + str(member.name) + "#" +
                      str(member.discriminator),
                      icon_url=member.avatar_url)
      
      embe.add_field(name="Responsible Moderator :",
                    value=f"{ctx.author.mention}",
                    inline=True)
      embe.add_field(name="Reason :",
                    value=f"{reason}",
                    inline=True)
      embe.set_thumbnail(url=member.avatar_url)

      await ctx.channel.send(embed=embe)
      if not member.bot:
        await member.send(embed=embe)
  

@client.command()
@commands.has_permissions(manage_messages=True,
                          manage_channels=True,
                          manage_roles=True)
async def tempmute(ctx,
                   member: discord.Member,
                   time: int,
                   d,
                   *,
                   reason="No reason provided"):

    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role == None:
        role = await ctx.guild.create_role(name="Muted",
                                           reason="Atla Bot Mute Role")

    await member.add_roles(role)
    embed = discord.Embed(
        title=
        f":mute:  {member.name}#{member.discriminator} was temporarily muted !",
        color=0xffdd00)
    embed.set_author(name="Temporarily Muted " + str(member.name) + "#" +
                     str(member.discriminator),
                     icon_url=member.avatar_url)

    embed.add_field(name="Responsible Moderator :",
                    value=ctx.author.mention,
                    inline=True)
    if d == "s":
        embed.add_field(name="Duration :",
                        value=str(time) + " Second(s)",
                        inline=True)
    elif d == "m":
        embed.add_field(name="Duration :",
                        value=str(time) + " Minute(s)",
                        inline=True)
    elif d == "h":
        embed.add_field(name="Duration :",
                        value=str(time) + " Hour(s)",
                        inline=True)
    embed.add_field(name="Reason :", value=reason)

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.message.delete()
    await member.add_roles(role)
    await ctx.channel.send(embed=embed)
    await member.send(embed=embed)
    if d == "s":
        await asyncio.sleep(time)

    if d == "m":
        await asyncio.sleep(time * 60)

    if d == "h":
        await asyncio.sleep(time * 60 * 60)

    if d == "d":
        await asyncio.sleep(time * 60 * 60 * 24)

    await member.remove_roles(role)
    embe = discord.Embed(
        title=
        f":loud_sound:  {member.name}#{member.discriminator} was unmuted successfully !",
        color=0x92e000)
    embe.set_author(name="Unmuted " + str(member.name) + "#" +
                    str(member.discriminator),
                    icon_url=member.avatar_url)
    embe.add_field(name="Defaulter :", value=member.mention, inline=True)
    embe.add_field(name="Responsible Moderator :",
                   value="Automatic Action Carried Out",
                   inline=True)
    embe.add_field(name="Reason :",
                   value="Temporary Mute Duration Has Ended",
                   inline=True)
    embe.set_thumbnail(url=member.avatar_url)

    await ctx.channel.send(embed=embe)
    await member.send(embed=embe)


@tempmute.error
async def tempmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to mute members.\nMissing Permission(s): `Manage Channels`, `Manage Roles`, `Messages` (One or more of these missing) "
        )


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "<:xs:818502085326405652> You don't have permission to mute members.\nMissing Permission(s): `Manage Channels`, `Manage Roles`, `Manage Messages` (One or more of these missing)"
        )


@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):

    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"Lifted ban on {user.mention} !")


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            ":xs:818502085326405652> You don't have permission to unban members.\nMissing Permission(s): `Ban Members`"
        )


@client.command()
async def vote(ctx):
    one = Button(style=ButtonStyle.URL, label="Click Here To Vote At top.gg", id="embed1", emoji="🗳️", url="https://top.gg/bot/767624993507901470/vote")
    embed = discord.Embed(
        title=":ballot_box:  Vote For Atla",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        timestamp=datetime.datetime.utcnow(),
        color=000000)

    embed.set_thumbnail(
        url=
        "https://images-ext-1.discordapp.net/external/GSPTqQJ_JztWDUSQWXGgDmQPc30q9oTY5Q1PiDOSJf8/https/emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/263/ballot-box-with-ballot_1f5f3.png?width=80&height=80"
    )
  
    embed.add_field(
        name="Vote Rewards",
        value=
        ":gift: 1 Rare Loot Crate\n<:slayersgem:785765850862059520> 10 Slayers Gems\n",
        inline=False)
    embed.set_footer(text="Double top.gg vote rewards on weekends !")
    await ctx.send(embed=embed, components=[one])

@client.command()
async def setpremium(ctx):
  users=await get_cd_data()
  user=ctx.author
  await open_cd(ctx.author)
  pr = users[str(user.id)]["premium"]
  pr += 1
  with open("cd.json", "w") as f:
     json.dump(users, f)

  if pr == 1:
    await ctx.send("1")
  elif pr == 0:
    await ctx.send("0")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def nezukorun(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  channel=ctx.channel
  async with channel.typing():
    nez = Image.open("nez.jpg")
    asset1 = ctx.author.avatar_url_as(size=128)
    asset2 = user.avatar_url_as(size=128)
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((108,105))
    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((106,107))
    nez.paste(pfp1, (109,95))
    nez.paste(pfp2, (491,130))

    nez.save("out1.jpg")

    await ctx.send(file = discord.File("out1.jpg"))
    await asyncio.sleep(2)
    os.remove("out1.jpg")
    print("Removed NezukoRun Output Image From Database")

@client.command(aliases=["owms"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def omaewamoushindeiru(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  channel=ctx.channel
  async with channel.typing():
    owms = Image.open("owms.jpg")
    asset1 = ctx.author.avatar_url_as(size=128)
    asset2 = user.avatar_url_as(size=128)
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((159,157))
    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((269,296))
    owms.paste(pfp1, (153,4))
    owms.paste(pfp2, (139,385))

    owms.save("out.jpg")

    await ctx.send(file = discord.File("out.jpg"))
    await asyncio.sleep(2)
    os.remove("out.jpg")
    print("Removed OWMS Output Image From Database")

@omaewamoushindeiru.error
async def omaewamoushindeiru_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      embed=discord.Embed(description=f"You can run this command only once __every 10 seconds__\nYou can make someoe good as dead again __in {error.retry_after:.2f} seconds__", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, This Command Is Ratelimited !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
      embed=discord.Embed(description=f"The user must be in the same server ! Try mentioning them or use their Discord User ID (available at `t userinfo @user`) !", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, That User Was Not Found !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
        
    else:
        raise error

@client.command(aliases=["rtb"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def raisedthatboy(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  channel=ctx.channel
  async with channel.typing():
    owms = Image.open("ka.jpg")
    asset1 = ctx.author.avatar_url_as(size=128)
    asset2 = user.avatar_url_as(size=128)
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((244,244))
    data2 = BytesIO(await asset2.read())
    pfp2 = Image.open(data2)
    pfp2 = pfp2.resize((420,407))
    owms.paste(pfp1, (472,437))
    owms.paste(pfp2, (1171,3))

    owms.save("out2.jpg")
    

    await ctx.send(file = discord.File("out2.jpg"))
    await asyncio.sleep(2)
    os.remove("out2.jpg")
    print("Removed RTB Output Image From Database")

@raisedthatboy.error
async def raisedthatboy_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      embed=discord.Embed(description=f"You can run this command only once __every 10 seconds__\nYou can gloat about raising someone again __in {error.retry_after:.2f} seconds__", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, This Command Is Ratelimited !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
      embed=discord.Embed(description=f"The user must be in the same server ! Try mentioning them or use their Discord User ID (available at `t userinfo @user`) !", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, That User Was Not Found !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
        
    else:
        raise error


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def drip(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  channel=ctx.channel
  async with channel.typing():
    owms = Image.open("drip.png")
    asset1 = user.avatar_url_as(size=128)
    
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((118,133))
    
    owms.paste(pfp1, (185,55))
    

    owms.save("out3.png")
  
    await ctx.send(file = discord.File("out3.png"))
    await ctx.send("Did you know that Atla can now play music ? Check oit out at `t commandlist` !")
    await asyncio.sleep(2)
    os.remove("out3.png")
    print("Removed Drip Output Image From Database")

@drip.error
async def drip_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      embed=discord.Embed(description=f"You can run this command only once __every 10 seconds__\nYou can make someone drip again __in {error.retry_after:.2f} seconds__", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, This Command Is Ratelimited !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
      embed=discord.Embed(description=f"The user must be in the same server ! Try mentioning them or use their Discord User ID (available at `t userinfo @user`) !", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, That User Was Not Found !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
        
    else:
        raise error


@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def lowquality(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  
  channel=ctx.channel
  async with channel.typing():
    asset1 = user.avatar_url_as(size=512)
    
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    
    pfp1.filter(ImageFilter.BoxBlur(5)).save('out4.png')
    
    
    await ctx.send(file = discord.File("out4.png"))
    await ctx.send("Did you know that Atla can now play music ? Check oit out at `t commandlist` !")
    await asyncio.sleep(2)
    os.remove("out4.png")
    print("Removed LowQuality Output Image From Database")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def wasted(ctx, user: discord.Member = None):
  if user == None:
    user = ctx.author
  channel=ctx.channel
  async with channel.typing():
    owms = Image.open("was.png")
    asset1 = user.avatar_url_as(size=512)
   
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((512,512))
    owms = owms.resize((512, 100))

    pfp1 = pfp1.convert(mode='L')
    pfp1.save("out10.png")

    pfp1.paste(owms.convert(mode="RGB"),(0,220))
    pfp1.save("out10.png")

    
    
    await ctx.send(file = discord.File("out10.png"))
    await ctx.send("Did you know that Atla can now play music ? Check oit out at `t commandlist` !")
    await asyncio.sleep(2)
    os.remove("out10.png")
    print("Removed Wasted Output Image From Database")

@wasted.error
async def wasted_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      embed=discord.Embed(description=f"You can run this command only once __every 10 seconds__\nYou can waste someone again __in {error.retry_after:.2f} seconds__", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, This Command Is Ratelimited !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)

    elif isinstance(error, commands.MemberNotFound):
      embed=discord.Embed(description=f"The user must be in the same server ! Try mentioning them or use their Discord User ID (available at `t userinfo @user`) !", color=0xff7b00)
      embed.set_author(name=f"{ctx.author}, That User Was Not Found !", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
        
    else:
        raise error

#SLASH COMMANDS

@slash.slash(name="ping", description="Pong \U0001f3d3 ! View the response time of the bot to Discord !")
async def _ping(ctx): 
    await ctx.send(f'>>> Pong! Client Latency : `{round(client.latency * 1000)}ms`'
                   )
guildids = [727428534204891166]
@slash.slash(name="userinfo",
             description="View detailed information on a member !",
             options=[
               create_option(
                 name="member",
                 description="Choose a member here, whose information you want to view",
                 option_type=6,
                 required=True)
             ])
async def _userinfo(ctx, member: discord.Member):
    created_at = member.created_at.strftime("%d %B %Y")
    jat = member.joined_at.strftime("%d %B %Y")
    pfp = member.avatar_url
    discid = member.id
    name = member
    global nick
    if member.display_name == member.name:
      nick = "No Nickname Here"
    else:
      nick = member.display_name
    usn = member.name
    disc = member.discriminator
    embed = discord.Embed(title="User Information", color=0x07e3f2)
    embed.set_author(name=name, icon_url=pfp)
    embed.add_field(name="User Name", value=usn)
    embed.add_field(name="User ID", value=discid, inline=True)
    embed.add_field(name="User Discriminator",
                    value="#" + str(disc),
                    inline=True)
    embed.add_field(name="Account Created On", value=created_at, inline=True)

    
    embed.add_field(name="Server Nickname", value=nick)
    embed.add_field(name="Joined Server On", value=f"{jat}", inline=True)
    embed.add_field(name="Top Role On Server",
                    value=f"{member.top_role.mention}",
                    inline=True)
    

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
  
@slash.slash(name="serverinfo", description="View extremely detailed information on your Discord server !")
async def _serverinfo(ctx): 
    server=ctx.guild
    create = server.created_at.strftime("%b %d, %Y")
    logourl = server.icon_url
    logo = server.icon
    owner = server.owner
    sid = server.id
    count = server.member_count
    active = server.max_presences
    chans = server.text_channels
    vc = server.voice_channels
    vcc = len(vc)
    cats = len(server.categories)
    chancount = len(chans)
    member = ctx.guild.member_count
    
    bans = await server.bans()
    emojis = await server.fetch_emojis()
    embed = discord.Embed(title="Server Information", color=0x07e3f2)
    embed.set_author(name=server, icon_url=logourl)
    embed.add_field(name="Server Name", value=server)
    embed.add_field(name="Server Region", value=str(server.region).capitalize())
    embed.add_field(name="Server ID", value=sid, inline=True)
    embed.add_field(name="Server Created", value=create, inline=True)
    embed.add_field(name="Server Icon URL",
                    value="[Click Here]({})".format(logourl),
                    inline=True)
    embed.add_field(name="Server Member Count",
                    value=f"<:members:826433096676671499> {member} Members",
                    inline=True)
    embed.add_field(name="Categories & Channel Count", value=f"<:category:826430086885933057> {cats} Categories\n<:voicechannel:826427969412136980> {vcc} Voice Channels\n<:textchannel:826427185509171220> {chancount} Text Channels", inline=True)

    embed.add_field(name="Server Security",
                    value=f"Verification Level - {str(server.verification_level).capitalize()} \nExplicit Content Filter - {str(server.explicit_content_filter).capitalize()}\n2FA - {str(bool(server.mfa_level)).capitalize()}",
                    inline=True)

    embed.add_field(name="Other Info", value=f":no_entry: {len(bans)}  Banned Members\n:fleur_de_lis: {len(emojis)}  Custom Emojis", inline=False)
    
    
  
    embed.set_thumbnail(url=server.icon_url)
    await ctx.send(embed=embed)


@slash.slash(name="Wasted", description="Waste someone GTA style !",
options=[
               create_option(
                 name="member",
                 description="Choose a member to waste here !",
                 option_type=6,
                 required=True)
             ])
async def _wasted(ctx, user: discord.Member = None):
    owms = Image.open("was.png")
    asset1 = user.avatar_url_as(size=512)
   
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((512,512))
    owms = owms.resize((512, 100))

    pfp1 = pfp1.convert(mode='L')
    pfp1.save("out10.png")

    pfp1.paste(owms.convert(mode="RGB"),(0,220))
    pfp1.save("out10.png")

    
    msg=await ctx.send(f"Wasted {user}")
    await msg.reply(file = discord.File("out10.png"))
    
    await asyncio.sleep(2)
    os.remove("out10.png")
    print("Removed /Wasted Output Image From Database")

@slash.slash(name="Drip", description="Put on a supreme jacket, make someone drip !",
options=[
               create_option(
                 name="member",
                 description="Choose a member to drip-ify here !",
                 option_type=6,
                 required=True)
             ])
async def _drip(ctx, user: discord.Member = None):
    owms = Image.open("drip.png")
    asset1 = user.avatar_url_as(size=128)
    
    data1 = BytesIO(await asset1.read())
    pfp1 = Image.open(data1)
    pfp1 = pfp1.resize((118,133))
    
    owms.paste(pfp1, (185,55))
    

    owms.save("out3.png")

    
    msg=await ctx.send(f"Drip {user}")
    await msg.reply(file = discord.File("out3.png"))
    
    await asyncio.sleep(2)
    os.remove("out3.png")
    print("Removed /Drip Output Image From Database")

@slash.slash(name="Avatar", description="Displays the profile picture of a user and its image URLs",
options=[
               create_option(
                 name="member",
                 description="Choose whose profile picture you want to view here !",
                 option_type=6,
                 required=True)
             ])
async def _avatar(ctx, member: discord.Member = None):
    
    webplink = member.avatar_url_as(static_format="webp")
    pnglink = member.avatar_url_as(static_format="png")
    jpglink = member.avatar_url_as(static_format="jpg")
    giflink = member.avatar_url
    embed = discord.Embed(color=0x000000)
    embed.set_author(name=str(member.name) + "#" + str(member.discriminator) +
                     "'s Avatar",
                     icon_url=pnglink)
    if str(member.avatar_url).endswith(".gif?size=1024"):
      embed.add_field(name="Avatar URLs", value=f"[GIF]({giflink})")
    else:

      embed.add_field(name="Avatar URLs", value=f"[JPG]({jpglink})  | [PNG]({pnglink}) | [WEBP]({webplink})")
                    
    embed.set_image(url=pnglink)
    await ctx.send(embed=embed)



@client.command(aliases=["rank", "lvl"])
async def level(ctx, member: discord.Member=None):
  channel=ctx.channel
  async with channel.typing():
    if member == None:
      member = ctx.author
    await open_account(member)
    await open_moves(member)
    await levels(member)
    users = await get_bank_data()
    res = await levels(member)
    level = res[0]
    x = users[str(member.id)]["xp"]
    global dscrank
    global li
    global li1
    if x in range(0, 499):
        dscrank = "Mizunoto | Rank X"
        li = 500 - x
        li1 = 500
    elif x in range(500, 1899):
        dscrank = "Mizunoe | Rank IX"
        li = 1900 - x
        li1 = 1900
    elif x in range(1900, 2799):
        dscrank = "Kanoto | Rank VIII"
        li = 2800 - x
        li1 = 2800
    elif x in range(2800, 3899):
        dscrank = "Kanoe | Rank VII"
        li = 3900 - x
        li1 = 3900
    elif x in range(3900, 4999):
        dscrank = "Tsuchinoto | Rank VI"
        li = 5000 - x
        li1 = 5000
    elif x in range(5000, 6499):
        dscrank = "Tsuchinoe | Rank V"
        li = 6500 - x
        li1 = 6500
    elif x in range(6500, 7899):
        dscrank = "Hinoto | Rank IV"
        li = 7900 - x
        li1 = 7900
    elif x in range(7900, 9099):
        dscrank = "Hinoe | Rank III"
        li = 9100 - x
        li1 = 9100
    elif x in range(9100, 11499):
        dscrank = "Kinoto | Rank II"
        li = 11500 - x
        li1 = 11500
    elif x in range(11500, 14999):
        dscrank = "Kinoe | Rank I"
        li = 15000 - x
        li1 = 15000
    elif x in range(15000, 999999999):
        dscrank = "Hashira | Rank MAX"
        li1 = "`MAX`"
        li = "`MAX`"

    else:
        dscrank = "Error retrieving data"
        li1 = "Error retrieving data"
        li = "Error retrieving data"
    medium_font = ImageFont.truetype("LemonMilkRegular.otf", 35)
    font = ImageFont.truetype("LemonMilkRegular.otf", 35)
    med1_font = ImageFont.truetype("TheFrontman-j32M.ttf", 16)
    background = Image.open("bg.jpg")
    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    logo = Image.open(data).convert("RGBA").resize((110,110))
    bigsize = (logo.size[0] * 1, logo.size[1] * 1)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, 255)
    nxtlvl = res[1]
    draw.ellipse((140 * 1, 140 * 1, 189 * 1, 189 * 1), 0)
    
    mask = mask.resize(logo.size, Image.ANTIALIAS)
    logo.putalpha(mask)
    
    try:
      draw1 = ImageDraw.Draw(background)
      name = member.name
      sub = "Level And Rank"
      lv69 = "LEVEL"
      level = str(res[0])
      xp = res[3]
      limit = res[2]
      fraction = (xp / limit) * 360
      ranktit = "Slayer Corps Rank"
      rank = dscrank
      text_size = draw1.textsize(str(name), font=medium_font)
      rankfont = ImageFont.truetype("TheFrontman-j32M.ttf", 15)
      if len(name) < 18:
        draw1.text((160, 43), str(name), font=medium_font, fill="#00ffff")
      else:
        draw1.text((150, 43), str(name), font=ImageFont.truetype("LemonMilkRegular.otf", 25), fill="#00ffff")
      draw1.text((160, 91), str(sub), font=med1_font, fill="#99ffff")
      draw1.text((245, 173), str(ranktit), font=ImageFont.truetype("TheFrontman-j32M.ttf", 18), fill="#00ffff")
      draw1.text((245, 205), str(rank), font=rankfont, fill="#99ffff")
      draw1.text((245, 243), "Progress To Rank Up", font=ImageFont.truetype("TheFrontman-j32M.ttf", 18), fill="#00ffff")
      draw1.text((245, 271), str(x)+" / "+str(li1)+" XP", font=ImageFont.truetype("LemonMilkRegular.otf", 23), fill="#99ffff")
      draw1.text((115, 195), str(lv69), font=med1_font, fill="#99ffff")
      draw1.text((119, 225), str(level).zfill(2), font=font, fill="#99ffff")
      draw1.text((102, 330), "Next Level In", font=ImageFont.truetype("TheFrontman-j32M.ttf", 14), fill="#00ffff")
      draw1.text((113, 350), str(nxtlvl).zfill(2)+ " XP", font=ImageFont.truetype("LemonMilkRegular.otf", 23), fill="#99ffff")

      draw1.text((279, 330), "Next Rank In", font=ImageFont.truetype("TheFrontman-j32M.ttf", 14), fill="#00ffff")
     
      draw1.text((290, 350), str(li).zfill(2)+ " XP", font=ImageFont.truetype("LemonMilkRegular.otf", 23), fill="#99ffff")
    except Exception as er:
      await ctx.send(er)
    draw1.arc([82, 172, 205, 298], 0, int(fraction), fill=None, width=6)
    background.paste(logo, (30, 20), mask=logo)
    background.save("final.png")
    embed = discord.Embed(color=000000)
    embed.set_image(url='attachment://final.png')
    
    await ctx.send(file=discord.File('./final.png'), embed=embed)

@client.command()
async def lmao(ctx):
  await ctx.send("This command had a testing name of 'lmao'. It has permanently moved to `t level`. `t lvl` and `t rank` will also display the same")   

@client.command(aliases=["fotd"])
async def funnehoftheday(ctx):
  embed = discord.Embed(color=000000, description="Funneh Of The Day :rofl:")
  embed.add_field(name="Smoking causes ~~cancer~~ thooral. Smoking kills.", value="This command has reached its end of life. If you want new funneh related commands , I'll do it if we reach a 100 votes on june . Vote for ~~jose~~ Atla at `t vote`")
  embed.set_image(url='attachment://funneh.JPG')
  
  await ctx.send(file=discord.File('./funneh.JPG'), embed=embed)
  
  

@client.command()
async def math(ctx, *, exprn="0"):
  if exprn == "0":
    await ctx.send("You need to provide a mathematical expression to calculate !\nYou can mix multiple operations and use sin(), cos() and tan() ! You can also use `**` for exponents.\n\nExamples: `t math 1+2*3-4`, `t math sin(60)+50`, `t math 8**2`")
  else:
    result = eval(exprn)
    embed=discord.Embed(colour=000000)
    embed.set_author(name="Math Calculator")
    embed.add_field(name=f"Input : {exprn}\t|\tResult :  {str(result)}", value=f"You can even use ** for exponents and sin(), cos(), tan()\n*Note*: Trigonometric input angles are measured in radians", inline=True)
      
    await ctx.reply(embed=embed)
 

reddit = praw.Reddit(client_id = "Pf-CJbh23eNpyw", client_secret = "WXEJa2R2C5F2QWaEH8gT7CgaXmoLoA", username="atlabotdiscord", password="p@55vv0rd", user_agent="atla", check_for_async=False)

@client.command()
async def meme(ctx, sub="memes"):
    channel = ctx.channel
  
    subreddit = reddit.subreddit(sub)
    alls = []
    top = subreddit.hot(limit=50)

    i=0
    while i<1:
      for submission in top:
        alls.append(submission)
        i+=1
    
    ran= random.choice(alls)
    alls.remove(ran)
    name = ran.title
    url = ran.url
    ups = ran.ups
    cc = len(ran.comments)
    
    em = discord.Embed(title=f"{name}\t", url=url)
    em.add_field(name=f"{ups} <:upvote:781762766339309568>", value=f"**{cc} :speech_balloon:**")
    em.set_image(url=url)
    await ctx.send(embed = em)

@client.command()
async def trigger(ctx, user: discord.Member):
  if not user:
    user = ctx.author
  else:
    pass

  url = "https://some-random-api.ml/canvas/triggered/?avatar=user.avatar_url"
  async with request("GET", url, headers={}) as response:
    if response.status == 200:
        data = await response.json()
        await ctx.send(data)

    
  
@client.command()
async def buttontest(ctx):
  one = Button(style=ButtonStyle.blue, label="blue button", id="embed1", emoji="📜")
  two = Button(style=ButtonStyle.red, label="red button lol", id="embed2")
  three = Button(style=ButtonStyle.green, label="green button lol", id="embed3")
  four = Button(style=ButtonStyle.grey, label="grey button lol", id="embed4")

  embed = discord.Embed(
        title="Button testing",
        url=
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
        color=0x0cc0ed)
  embed.add_field(
        name="click any button",
        value=
        "each button can only be clicked once",
        inline=False)
    
      
  embed1 = discord.Embed(
          title="Blue button embed",
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
          color=discord.Colour.blurple())
  embed1.add_field(
        name="You are seein this because you clicked the blue button",
        value=
        "testing",
        inline=False)
    
  embed2 = discord.Embed(
          title="red button embed",
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
          color=discord.Colour.red())
  embed2.add_field(
        name="You are seein this because you clicked the red button",
        value=
        "testing",
        inline=False)
    
  embed3 = discord.Embed(
          title="green button embed",
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92",
          color=discord.Colour.green())
  embed3.add_field(
        name="You are seein this because you clicked the green button",
        value=
        "testing",
        inline=False)

  embed4 = discord.Embed(
          title="grey button embed",
          url=
          "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PL45I7czocaVJmE4FQrV4r6R5SL47hIs-O&index=92"
          )
  embed4.add_field(
        name="You are seein this because you clicked the grey button",
        value=
        "testing",
        inline=False)
    
  buttons = {"embed1":embed1, "embed2":embed2,"embed3":embed3,"embed4":embed4}

  mes = await ctx.send(embed=embed,
  components=[[one,two,three,four]])
  
  res1 = await client.wait_for("button_click")
  if res1.channel==ctx.channel:
    await mes.edit(embed=embed1)
    response = buttons.get(res1.component.id)
    if response is None:
      await ctx.send("clicked blue")
    

  res2 = await client.wait_for("button_click")
  if res2.channel==ctx.channel:
    await mes.edit(embed=embed2)

  res3 = await client.wait_for("button_click")
  if res3.channel==ctx.channel:
    await mes.edit(embed=embed3)
    
  res4 = await client.wait_for("button_click")
  if res4.channel==ctx.channel:
    await mes.edit(embed=embed4)

    

client.sniped_messages = {}
client.edited_messages = {}
@client.event
async def on_message_delete(message):
  try:
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at, message.attachments[0])
  except IndexError:
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at, None)

@client.event
async def on_message_edit(before, after):
    client.edited_messages[before.guild.id] = (before.content, before.author, before.channel.name, before.created_at, after.content)


@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time1, attachs = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=f"{contents}", color=000000, timestamp=time1)
    embed.set_author(name=f"{author.name}#{author.discriminator} said", icon_url=author.avatar_url)
    if attachs != None:
      embed.set_image(url=attachs.url)
  
    embed.set_footer(text=f"Deleted in  #{channel_name}")

    await ctx.channel.send(embed=embed)

@client.command(aliases=["esnipe","es"])
async def editsnipe(ctx):
    try:
        contents, author, channel_name, time1, mid = client.edited_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find an edited message to snipe!")
        return

    embed = discord.Embed(description=f"**Before**\n{contents}\n**After**\n{mid}", color=000000, timestamp=time1)
    embed.set_author(name=f"{author.name}#{author.discriminator} edited their message", icon_url=author.avatar_url)
    
  
    embed.set_footer(text=f"Edited in  #{channel_name}")

    await ctx.channel.send(embed=embed)
@client.command()
async def pp(ctx, user:discord.Member):
  profile = await user.profile()
  accounts = profile.user
  await ctx.send(accounts)
keep_alive.keep_alive()
client.run(os.getenv('TOKE'))
