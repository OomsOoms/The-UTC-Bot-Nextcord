from datetime import datetime
from nextcord import SlashOption
import nextcord 
import pandas as pd

from convert_time import *
from constants import *

def init_submit_cmd(bot):

  #bot.slash_command(name="submit-video")
  #sync def submit_video(ctx, link, private: int =  SlashOption(choices={"True": True, "False": False})):
  # if private:
  #   await bot.get_channel(int(pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")["log_channel"][0])).send(f"<@{ctx.user.id}> Submited **EVENT NAME** Video {link}")
  # else:
  #   await ctx.send(f"<@** Video {link}")

  @bot.slash_command(name="submit-solves")
  async def submit_solves(ctx, solve1, solve2, solve3, solve4, solve5): 
    competition_results_path = f"server_settings/{ctx.guild.id}/competition_results.csv"
    channel_config_path = f"server_settings/{ctx.guild.id}/channel_config.csv"
    
    comp_data_dict = pd.read_csv(competition_results_path).to_dict("list")
    config_dict =  pd.read_csv(channel_config_path).to_dict("list")

    for i, key in enumerate(config_dict): # Compares channel ID to all saved IDs
      if not ctx.channel.id == config_dict[key][0]: 
        if i == len(config_dict)-1: # Only send messgae on last loop
          await ctx.send("Invalid submission channel", ephemeral=True)
      else:
        submitted_once = True
        for i, user_id in enumerate(comp_data_dict["discord_id"]): # Compares uers id to all saves IDs to see if they have an entry
          if ctx.user.id == user_id:
            if ctx.channel.id == comp_data_dict["channel_id"][i]: # If there is an entry with the same channel it means its the secnds entry for that event
              await ctx.send("You can only submit once", ephemeral=True)
              submitted_once = False
        try:
          if submitted_once:
            times_list = [solve1, solve2, solve3, solve4, solve5]
            constant_times_list = times_list.copy()
            
            for i, time in enumerate(times_list):
              if "DNF" in time.upper(): times_list[i] = "9078563412" # Sets DNF to biggest number in average 
              if "+" in time: times_list[i] = convert_time_float(time.split("+")[0])+2
          
            for i in range(len(times_list)): times_list[i] = convert_time_float(times_list[i]) # Converts all times to real numbers
            average = convert_time_str(mean(times_list))
            if times_list.count(9078563412) >= 2: average = "DNF"
            min_index, max_index = times_list.index(min(times_list)), times_list.index(max(times_list))

            for i in range(len(times_list)): times_list[i] = convert_time_str(times_list[i]) # Converts all times back to strings
            for i, time in enumerate(constant_times_list):
              if "+" in time: times_list[i] = f"{times_list[i]}+"
            for i, time in enumerate(times_list):
              if time == "151309390:12.00": times_list[i] = "DNF" 
              
            times_list[min_index] = f"({times_list[min_index]})" # Formatting for embed
            times_list[max_index] = f"({times_list[max_index]})" # Formatting for embed

            new_results = {
              "time_submitted": [str(datetime.now())[:19].replace("-", "/")],
              "discord_user": [ctx.user],
              "discord_id": [ctx.user.id],
              "channel_id": [ctx.channel.id],
              "event_name": [key[:len(key)-2]],
              "times_list": [times_list],
              "average": [average]
            }

            new_results = pd.DataFrame(new_results) # Writing new results to CSV file
            new_results.to_csv(competition_results_path, mode='a', index=False, header=False)

            embed = nextcord.Embed(title=f"{ctx.user.name} Results!", color=ctx.user.colour) # Making embed
            embed.add_field(name="Average", value=f"⠀{average}", inline=False)
            embed.add_field(name="Solves", value=f"⠀⠀{times_list[0]} {times_list[1]} {times_list[2]} {times_list[3]} {times_list[4]}", inline=False)
            embed.set_thumbnail(url=ctx.user.avatar.url)
            await ctx.send(embed=embed)

            try: await bot.get_channel(int(config_dict["log_channel"][0])).send(f"<@{ctx.user.id}> Submited **{key[:len(key)-2]}** results")  # type: ignore
            except: pass
        except: await ctx.send("Invaild syntax, mention staff if you need help", ephemeral=True)
        break