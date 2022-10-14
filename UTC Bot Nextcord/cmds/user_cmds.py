from nextcord import SlashOption, SelectOption
from nextcord.ui import View, Select
import pandas as pd
import nextcord

from constants import *

def init_user_cmds(bot):

    @bot.slash_command(name="ping", description="Play PingPong with the bots latency")
    async def ping(ctx):
        await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

    @bot.slash_command(name="download-data", description="Download current competition results")
    async def set_channel(ctx): 
        path = f"server_settings/{ctx.guild.id}/competition_results.csv"
        await ctx.send(file=nextcord.File(path))

    @bot.slash_command(name="help", description="Help on command and how to compete")#, guild_ids=[1008051439957966989])
    async def help(ctx, command_name: int =  SlashOption(required=False, choices={"submit-solves": 1})):
        def commands(command_name):
            if command_name == 1:
                embed = nextcord.Embed(title="Submit solves", description="Submit your average for your chosen event", url="https://www.youtube.com/watch?v=yX7HBSg1yeM&ab_channel=Ooms")
                embed.set_author(name="UTC Bot commands help", icon_url="https://cdn.discordapp.com/attachments/1028792329827524688/1029515922463019029/UTC_Logo.png")  
                embed.set_footer(text=f"⠀\nUse /help [command-name] for more info and help on syntax. Feel free to mention staff for help")

                embed.add_field(name="How to use", value="Go to the corresponding channel for your event and use this command.\nTo see assigned channels use `/view-assigned-channels`", inline=True)
                embed.add_field(name="Syntax", value="mm:ss.ms: example - 1:14.12, 16.23\nPenalties: [YOUR TIME]+2, DNF", inline=True)

            else:
                embed = nextcord.Embed()
                embed.set_author(name="UTC Bot commands help", icon_url="https://cdn.discordapp.com/attachments/1028792329827524688/1029515922463019029/UTC_Logo.png")  
                embed.set_footer(text=f"⠀\nUse /help [command-name] for more info and help on syntax. Feel free to mention staff for help")

                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1028792329827524688/1029515922463019029/UTC_Logo.png")
                embed.add_field(name="**Submit solves**", value="`/help submit-solves`.", inline=True)

            return embed

        async def dropdown_callback(ctx):
            for value in dropdown.values: await msg.edit(embed=commands(int(value)), view=View()) 
    
        option1 = SelectOption(label="Submit solves", value="1", description="How to submit your average")
        dropdown = Select(placeholder="Pick a command", options=[option1])
        dropdown.callback = dropdown_callback  # type: ignore
        view = View(timeout=180)
        view.add_item(dropdown)

        if type(command_name) is int: view = View()
        
        msg = await ctx.send(embed=commands(command_name), view=view)

    @bot.slash_command(name="view-assigned-channels", description="Shows the channels that have been assigned a use")
    async def view_channel_config(ctx): 
        df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
        message = "**Assigned channels:**"
        for x in df:
            try: message = f"{message}\n**{x}**: <#{df[x][0]}>"
            except: message = f"{message}\n**{x}**: <#{df[x]}>"
        await ctx.send(message, ephemeral=True)

        
        





"""

        async def button_callback(ctx):
            await ctx.send("Button pressed")
        button = Button(label="button")
        view = View()
        view.add_item(button)
        button.callback = button_callback

        embed = nextcord.Embed()
        embed.add_field(name="Download", value="intresting", inline=True)
        msg = await ctx.send(embed=embed)
        
        embed = nextcord.Embed()
        embed.add_field(name="Dowad", value="intrng.", inline=True)
        await msg.edit(embed=embed, view=view) 

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