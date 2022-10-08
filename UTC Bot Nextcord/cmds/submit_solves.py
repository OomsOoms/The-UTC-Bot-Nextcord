import pandas as pd
from datetime import datetime
import nextcord

from convert_time import *
from constants import *

def init_submit_solves_cmd(bot):
    @bot.slash_command(name="submit-solves")#, guild_ids=[ID])
    async def submit_solves(ctx, solve1, solve2, solve3, solve4, solve5): 
      competition_results_path = f"server_settings/{ctx.guild.id}/competition_results.csv"
      channel_config_path = f"server_settings/{ctx.guild.id}/channel_config.csv"

      for i, key in enumerate(pd.read_csv(channel_config_path).to_dict("list")):
        if not ctx.channel.id == pd.read_csv(channel_config_path).to_dict("list")[key][0]:
          if i == len(pd.read_csv(channel_config_path).to_dict("list"))-1:
            await ctx.send("Invalid submission channel", ephemeral=True)
        else:
          try:
            submitted_once = True
            for i, x in enumerate(pd.read_csv(competition_results_path).to_dict("list")["discord_id"]):
              if ctx.user.id == x:
                if ctx.channel.id == pd.read_csv(competition_results_path).to_dict("list")["channel_id"][i]:
                  await ctx.send("You can only submit once", ephemeral=True)
                  submitted_once = False

            if submitted_once:
              times_list = [solve1, solve2, solve3, solve4, solve5]
              constant_times_list = times_list.copy()

              for i, x in enumerate(times_list):
                if "DNF" in x.upper(): times_list[i] = x.upper().replace("DNF", "-1.0")
                if "+" in x: times_list[i] = convert_time_float(x.split("+")[0])+2
            
              for i in range(len(times_list)): times_list[i] = convert_time_float(times_list[i])
                
              average = convert_time_str(mean(times_list))

              if times_list.count(-1.0) >= 3: average = "DNF"

              min_index, max_index = times_list.index(min(times_list)), times_list.index(max(times_list))

              for i in range(len(times_list)): times_list[i] = convert_time_str(times_list[i])

              for i, x in enumerate(constant_times_list):
                if "+" in x: times_list[i] = f"{times_list[i]}+"

              for i, x in enumerate(times_list):
                if x == -1.0: times_list[i] = "DNF"
                

              times_list[min_index] = f"({times_list[min_index]})"
              times_list[max_index] = f"({times_list[max_index]})"

              new_results = {
                "time_submitted": [datetime.now()],
                "discord_user": [ctx.user],
                "discord_id": [ctx.user.id],
                "event_name": [key[:len(key)-2]],  # type: ignore
                "channel_id": [ctx.channel.id],
                "solve_1": [times_list[0]],
                "solve_2": [times_list[1]],
                "solve_3": [times_list[2]],
                "solve_4": [times_list[3]],
                "solve_5": [times_list[4]],
                "average": [average],
                "embed_message": [[f"{ctx.user.name} Results!", f"Average⠀⠀⠀⠀⠀⠀⠀Solves", f"⠀{average}⠀⠀{times_list[0]} {times_list[1]} {times_list[2]} {times_list[3]} {times_list[4]}"]]
              }

              new_results = pd.DataFrame(new_results)   
              new_results.to_csv(competition_results_path, mode='a', index=False, header=False)

              embed = nextcord.Embed(title=f"{ctx.user.name} Results!", color=ctx.user.colour)
              embed.add_field(name=f"Average⠀⠀⠀⠀⠀⠀⠀Solves", value=f"⠀{average}⠀⠀{times_list[0]} {times_list[1]} {times_list[2]} {times_list[3]} {times_list[4]}", inline=True)
              embed.set_thumbnail(url=ctx.user.avatar.url)

              await ctx.send(embed=embed)
              
              try: await bot.get_channel(int(pd.read_csv(channel_config_path).to_dict("list")["log_channel"][0])).send(f"<@{ctx.user.id}> Submited **{key[:len(key)-2]}** results")  # type: ignore
              except: pass
          except: await ctx.send("Invaild syntax, mention staff if you need help", ephemeral=True)
          break