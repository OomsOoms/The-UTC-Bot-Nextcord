from datetime import datetime
from nextcord import SlashOption
import nextcord
import pandas as pd
import os

from constants import *

def init_user_cmds(bot):
    @bot.slash_command(name="ping", description="Play PingPong with the bots latency")
    async def ping(ctx):
        await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
        
    @bot.event
    async def on_ready():
        await bot.change_presence(activity=nextcord.Activity(type=5, name="a UTC competition"))
        print(f"Online: {datetime.now()}")

    @bot.event
    async def on_guild_join(guild):
        df, df2 = pd.DataFrame(settings_dict), pd.DataFrame(competition_results_dict)
        os.makedirs(f"server_settings/{guild.id}")
        df.to_csv(f"server_settings/{guild.id}/channel_config.csv", index=False)
        df2.to_csv(f"server_settings/{guild.id}/competition_results.csv", index=False)

    @bot.slash_command(name="download-data", description="Download current competition results")
    async def set_channel(ctx): 
        path = f"server_settings/{ctx.guild.id}/competition_results.csv"
        await ctx.send(file=nextcord.File(path))

    @bot.slash_command(name="help")#, guild_ids=[1008051439957966989])
    async def help(ctx, command_name: int =  SlashOption(required=False, choices={"Download-data": 1, "Submit-solves": 2})):
        embed = nextcord.Embed()
        embed.set_author(name="UTC Commnad help 2", icon_url="https://cdn.discordapp.com/attachments/1022903963772780584/1027694855884902440/UTC_Logo.png")  
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1022903963772780584/1027694855884902440/UTC_Logo.png")
        embed.set_footer(text=f"⠀\nUse /help [command-name] for more info and help on syntax. Feel free to mention staff for help")

        if command_name == 1:
            embed.add_field(name="Download data", value="Sends a csv file all the stored\n data from the current competition. This could\n be used for data analysis if you really\n wanted to go through that pain. But it is intresting.", inline=True)

        elif command_name == 2:
            embed.add_field(name="Submit solves", value="Use in the correct channel for it\n to work. these channels will have a message\n at the start with the event name.\n\n**syntax**:\n mm:ss.ms\n mm:ss.ms+2\nDNF", inline=True)

        else:
            embed.add_field(name="Submit solves", value="Use in the correct channel for it\n to work.", inline=True)
            embed.set_author(name="UTC Commnad help, 2", icon_url="https://cdn.discordapp.com/attachments/1022903963772780584/1027694855884902440/UTC_Logo.png")
            embed.add_field(name="Download data", value="Downloads all the results for the\n current competition as a csv file.", inline=True)
        await ctx.send(embed=embed)
"""
    @bot.user_command(name="View results")
    async def view_resuts(ctx: nextcord.Interaction, member: nextcord.member):
        competition_results = pd.read_csv(f"server_settings/{ctx.guild.id}/competition_results.csv").to_dict("list")
        
        if not competition_results["discord_id"] == []:
            for x in competition_results["discord_id"]:
            
            if str(x) == str(member.id):
                # Making the embed
                embed_message = ast.literal_eval(competition_results["embed_message"][0])
                embed = nextcord.Embed(title=embed_message[0], color=ctx.user.colour)
                embed.add_field(name=embed_message[1], value=embed_message[2], inline=True)

                await ctx.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(f"<@{member.id}> has not competed yet!", ephemeral=True)
        else:
            await ctx.send(f"<@{member.id}> has not competed yet!", ephemeral=True)
"""