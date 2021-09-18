import discord
from discord_slash import SlashCommand
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType
import datetime
import random
import time
import pytz
import json
import os
import asyncio
import dotenv
import dbl
import logging
from aiohttp import request
from PIL import Image, ImageFilter
from io import BytesIO
from dotenv import load_dotenv
from datetime import date
from discord import Status
from discord.ext import commands, tasks
from discord.utils import get
import keep_alive

@client.event
async def on_member_join(member):
  with open('user.json', 'r') as f:
    users=json.load(f)

  await update_data(users, member)

  with open('users.json', 'w') as f:
    json.dump(users, f)

@client.event
async def on_command(command):
  with open('users.json', 'r') as f:
    users=json.load(f)

  await update_data(users, command.author)
  await add_experience(users, command.author, 5)
  await level_up(users, command.author, command.channel)


  with open('users.json', 'w') as f:
    json.dump(users, f)

async def update_data(users, user):
  if not user.id in users:
    users[user.id]={}
    users[user.id]['experience']=0
    users[user.id]['level']=1
    return True

async def add_experience(users, user, exp):
  users[user.id]['experience']+=exp

async def level_up(users, user, channel):
  experience = users[user.id]['experience']
  lvl_start=users[user.id]['level']
  lvl_end=int(experience ** (1/4))

  if lvl_start < lvl_end:
    await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
    users[user.id]['level']=lvl_end