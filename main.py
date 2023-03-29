import nextcord
from nextcord.ext import commands

from cmds import init_cmds

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)

init_cmds(bot)

bot.run("OTgyNjEzMTY1MTk4MTU1ODg2.GVuFIq.aE2KvUMdbNOwltnOoTXPovOU9a0_evhPsoWog4") 
