import discord
import os
import dbl
import logging
import json
from discord.ext import commands, tasks


async def get_bank_data():
  with open("mainbank.json","r") as f:
    users = json.load(f)
  return users



async def vote_open_account(user):
  users = await get_bank_data()

  if str(user) in users:
    return False
  else:
    users[str(user)] = {}
    users[str(user)]["xp"] = 0
    users[str(user)]["twostar"] = 0
    users[str(user)]["threestar"] = 0
    users[str(user)]["fourstar"] = 0
    users[str(user)]["fivestar"] = 0
    users[str(user)]["wallet"] = 0
    users[str(user)]["bank"] = 0
    users[str(user)]["coal"] = 0
    users[str(user)]["ore"] = 0
    users[str(user)]["fragment"] = 0
    users[str(user)]["chunk"] = 0
    users[str(user)]["dust"] = 0
    users[str(user)]["sand"] = 0
    users[str(user)]["nichirin"] = 0
    users[str(user)]["common"] = 0
    users[str(user)]["rare"] = 0
    users[str(user)]["epic"] = 0
    users[str(user)]["legendary"] = 0
    users[str(user)]["mystical"] = 0
    users[str(user)]["crystal"] = 0
    users[str(user)]["shard"] = 0
    users[str(user)]["blade"] = 0

  with open("mainbank.json","w") as f:
    json.dump(users,f)
  return True