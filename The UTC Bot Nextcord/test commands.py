from codecs import latin_1_decode
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import pandas as pd
import os

intents = nextcord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
  await bot.change_presence(activity=nextcord.Activity(type=5, name="a UTC competition"))
  print("Online")

@bot.slash_command(name="ping")
async def ping(ctx):
  await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

bot.run("TOEKN") 
