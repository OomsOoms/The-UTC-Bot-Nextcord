import nextcord
from nextcord.ext import commands

from cmds import init_cmds

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)

init_cmds(bot)

bot.run("TOKEN") 
