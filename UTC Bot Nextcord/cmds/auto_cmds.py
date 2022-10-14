import pandas as pd
from datetime import datetime
import nextcord, os

from constants import *

def init_auto_cmds(bot):
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=nextcord.Activity(type=5, name="a UTC competition"))
        print(f"Online: {datetime.now()}"[:27].replace("-", "/"))

    @bot.event
    async def on_guild_join(guild):
        df, df2 = pd.DataFrame(settings_dict), pd.DataFrame(competition_results_dict)
        os.makedirs(f"server_settings/{guild.id}")
        df.to_csv(f"server_settings/{guild.id}/channel_config.csv", index=False)
        df2.to_csv(f"server_settings/{guild.id}/competition_results.csv", index=False)