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
async def on_guild_join(guild):
    path = "server_settings/" + str(guild.id)
    channel_dict = {"log_channel": [""]}
    results = {
    "discord_id": [],
    "solve_1": [],
    "solve_2": [],
    "solve_3": [],
    "solve_4": [],
    "solve_5": [],
    }
    df = pd.DataFrame(channel_dict)
    df2 = pd.DataFrame(results)
    try:
      os.makedirs(path)
      df.to_csv(path + "/channel_config.csv", index=False)
      df2.to_csv(path + "/competition_results.csv", index=False)
      print("Making dir:" + path)
    #if the dir exist:
    except FileExistsError:
        print("Dir exist " + path)

@bot.event
async def on_ready():
  await bot.change_presence(activity=nextcord.Activity(type=5, name="a UTC competition"))
  print("Online")

@bot.slash_command(name="ping")#, guild_ids=[788453633963458650])
async def ping(ctx):
  await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.slash_command(name="help")#, guild_ids=[788453633963458650])
async def help(ctx):
  await ctx.send(f"I have run out of time to make this command, sorry, if you need help @Ooms")


# Admin commands below
# event editing comandas:
# /clear-event-channels /view-event-channels 
@bot.slash_command(name="view-config-channels")
async def view_event_channels(ctx): 
  if not ctx.user.guild_permissions.administrator:
    await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
  else:
    path = f"server_settings\{ctx.guild.id}\channel_config.csv"

    df = pd.read_csv(path).to_dict("list")

    await ctx.send(df, ephemeral=True)

@bot.slash_command(name="clear-config-channels")
async def clear_event_channels(ctx): 
  if not ctx.user.guild_permissions.administrator:
    await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
  else:
    path = f"server_settings\{ctx.guild.id}\channel_config.csv"

    df = pd.read_csv(path).to_dict("list")

    df = {"log_channel": [df["log_channel"][0]]}
    
    await bot.get_channel(int(df["log_channel"][0])).send("All event channels reset, log channel unchanged")

    df = pd.DataFrame(df)
    
    df.to_csv(path, index=False)

    await ctx.send("All event channels reset, log channel unchanged", ephemeral=True)


# set channel command for event and log channels:
# /set-channel (log_channel, event_name)
@bot.slash_command(name="set-channel")
async def set_channel(ctx, log_channel="", event_name=""): 
  if not ctx.user.guild_permissions.administrator:
    await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
  else:
    path = f"server_settings\{ctx.guild.id}\channel_config.csv"

    df = pd.read_csv(path).to_dict("list")

    if not log_channel == "": 
      df["log_channel"] = [log_channel.replace("<#", "").replace(">", "")]
      try:
        await ctx.send("Channels updated", ephemeral=True)
        await bot.get_channel(int(df["log_channel"][0])).send("**Channels updated**\n\n" + str(df))
      except:
        await ctx.send("Invalid Channel!", ephemeral=True)

      df = pd.DataFrame(df)

      df.to_csv(path, index=False)
    
    if not event_name == "":
      in_use = False
      for x in df:
        if str(df[x][0]) == str(ctx.channel.id):
          await ctx.send("Channel is already in use", ephemeral=True)
          in_use = True

      if not in_use:
        response = {f"{event_name}_{len(df)}": [ctx.channel.id]}
        
        df.update(response)

        await ctx.send(f"**Submit {event_name} results here! use the /submit-solves command**")
        await ctx.send("Channels updated", ephemeral=True)
        await bot.get_channel(int(df["log_channel"][0])).send("**Channels updated**\n\n" + str(df))

        new_data = pd.DataFrame(df)

        new_data.to_csv(path, index=False)


# Not admin commands bellow
@bot.slash_command(name="download-data")
async def set_channel(ctx): 
  path = f"server_settings\{ctx.guild.id}\competition_results.csv"

  await ctx.send(file=nextcord.File(path))

@bot.slash_command(name="submit-solves")#, guild_ids=[ID])
async def submit_solves(ctx, solve1, solve2, solve3, solve4, solve5): 
  try:
    times = [solve1, solve2, solve3, solve4, solve5]

    for x in range(5):
      if ":" in times[x]:
        mins, temp = times[x].split(":")
        sec, ms = temp.split(".")
        times[x] = str(int(mins)*60 + int(sec) + int(ms)/100)
      
    i = 0
    n = []
    for x in range(5):
      if "+" in times[x]:
        time, temp = str(times[x]).split("+")
        time = float(time) + 2
        times[x] = str(time)
        n.append(x)

    for x in times:
      if x.upper() == "DNF":
        times[i] = -1
      i += 1
    
    i = 0
    for x in range (5):
      if times[x] == -1:
        i += 1
    
    if i >= 2:
      average = "DNF"

      for x in range(5):
        if str(times[x]) == "-1":
          times[x] = "DNF"
      
    else:
      average = times.copy()
      average = [ float(x) for x in average ]

      average.remove(min(average))
      average.remove(max(average))
      average = round(sum(average)/3, 2)

      
      sec, ms = str(average).split(".")

      if len(ms) < 2:
        ms = str(ms) + "0"

      if len(ms) > 2:
        ms = ms[:2]

      average = f"{sec}.{ms}"

      times = [ float(x) for x in times ]

      min_time = int(times.index(min(times)))
      max_time = int(times.index(max(times)))

      for x in range(5):
        if times[x] > 59.9999999:
          sec, ms = str(times[x]).split(".")
          times[x] = str(int(sec)//60)+":"+str((int(sec)%60+int(ms)/100))

      for x in range(5):
        sec, ms = str(times[x]).split(".")

        if len(ms) < 2:
          ms = str(ms) + "0"

        if len(ms) > 2:
          ms = ms[:2]

        times[x] = f"{sec}.{ms}"

      for x in range(len(n)):
        times[n[int(x)]] = str(times[n[x]]) + "+"

      times[min_time] = f"({times[min_time]})"
      times[max_time] = f"({times[max_time]})"

      
        
      for x in range(5):
        if str(times[x]) == "(-1.00)":
          times[x] = "(DNF)"

    solves_len = round(len(f"{times[0]} {times[1]} {times[2]} {times[3]} {times[4]}")/2)
    space = " "
    empty = "⠀"

    embed = nextcord.Embed(title=f"⠀ {int(solves_len/2-5)*empty}{int(solves_len/2)*space}{ctx.user} Results!", color=ctx.user.colour)
    embed.add_field(name=f"⠀ {int(solves_len/2-6)*empty}{int(solves_len/2)*space}Average", value=f"⠀ {int(solves_len/2-3)*empty}{int(solves_len/2)*space}{average}", inline=True)
    embed.add_field(name=f"⠀ {int(solves_len/2-3)*empty}{int(solves_len/2)*space}Solves", value=f"{times[0]} {times[1]} {times[2]} {times[3]} {times[4]}", inline=True)
    
    path = f"server_settings\{ctx.guild.id}\competition_results.csv"
    df2 = pd.read_csv(f"server_settings\{ctx.guild.id}\channel_config.csv")

    df = {
    "discord_id": [ctx.user],
    "solve_1": [times[0]],
    "solve_2": [times[1]],
    "solve_3": [times[2]],
    "solve_4": [times[3]],
    "solve_5": [times[4]],
    }

    df = pd.DataFrame(df)
    
    submitted_once = True
    print(pd.read_csv(path).to_dict("list"))
    for x in pd.read_csv(path).to_dict("list")["discord_id"]:
      if str(x) == str(ctx.user):
        await ctx.send("You can only submit once", ephemeral=True)
        submitted_once = False

    if submitted_once:   
      df.to_csv(path, mode='a', index=False, header=False)

      #embed.set_footer(text=ctx.user, icon_url = ctx.user.avatar_url)
      await ctx.send(embed=embed)
      await bot.get_channel(str(int(df2["log_channel"][0])).send(str(ctx.user)) + " Submited results")

  except KeyboardInterrupt:
    await ctx.send("Invaild syntax, mention staff if you need help", ephemeral=True)

bot.run("OTgyNjEzMTY1MTk4MTU1ODg2.GR_sZu.y8puBj2FdQh91tW2RbfvZiGLnf7cUyC7C2LkEE") 