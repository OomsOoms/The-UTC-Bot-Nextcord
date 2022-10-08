import nextcord
from nextcord.ext import commands

from cmds import init_cmds

intents = nextcord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!")

init_cmds(bot)

bot.run("MTAyODA2ODkzODQ3NjY5NTU5Mw.GxZIiH.B6-5rSHHhm_Uy6pLXazUtMz_eE69GDg7F2DwoE") 