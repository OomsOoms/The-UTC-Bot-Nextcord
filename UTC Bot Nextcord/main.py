import nextcord
from nextcord.ext import commands

from cmds import init_cmds

intents = nextcord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!")

init_cmds(bot)

bot.run("TOKEN") 
