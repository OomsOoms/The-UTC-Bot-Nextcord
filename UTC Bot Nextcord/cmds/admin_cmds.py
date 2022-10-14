import nextcord
import pandas as pd
import asyncio
from nextcord import SelectOption, SlashOption
from nextcord.ui import Button, Select, View


def init_admin_cmds(bot):
    
    @bot.slash_command(name="assign-log-channel", description="Sets the current channel to the bots log channel")
    async def assign_log_channel(ctx): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You are not authorized to run this command.", ephemeral=True)
        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list") # Reading CSV file
            df["log_channel"] = [ctx.channel.id]  # Changing log channel ID
            df = pd.DataFrame(df)
            df.to_csv(f"server_settings/{ctx.guild.id}/channel_config.csv", index=False)
            await bot.get_channel(int(df["log_channel"][0])).send(f"<#{ctx.channel.id}> set to log channel")
    
    @bot.slash_command(name="assign-event-channel", description="Sets current channel to an entries channel")
    async def assign_event_channel(ctx, event_name): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You are not authorized to run this command.", ephemeral=True)
        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
            in_use = False
            for x in df:
                try: # If there is an error it means no log channel is set
                    if str(df[x][0]) == str(ctx.channel.id):
                        await ctx.send("Channel has already been asigened", ephemeral=True)
                        in_use = True
                except: await ctx.send("No assigned log channel, it is required for this command to work", ephemeral=True)
                
                if not in_use:
                    response = {f"{event_name}_{len(df)}": [ctx.channel.id]}
                    df.update(response)  # type: ignore
                    new_data = pd.DataFrame(df)
                    new_data.to_csv(f"server_settings/{ctx.guild.id}/channel_config.csv", index=False)
                    # try except for error if log channel is unassigned
                    try: await bot.get_channel(int(df["log_channel"][0])).send("")
                    except: pass
                    await ctx.send(f"**Submit {event_name} results here! use the `/submit-solves` command**")

    @bot.slash_command(name="reset-assigned-channel", description="Resets the current assigned channel or all, excluding the log channel")
    async def clear_event_channels(ctx, channels: int = SlashOption(choices={"All": True, "Current": False})): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You are not authorized to run this command.", ephemeral=True)
        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
            if channels:
                df = {"log_channel": [df["log_channel"][0]]}
                msg = "All event channels reset, log channel unchanged"
            else:
                for key in df:
                    if df[key][0] == ctx.channel.id:
                        if key == "log_channel":
                            df = {"log_channel": []}
                            msg = f"<#{ctx.channel.id}> removed from assigned channel, event channels require this therefore all assigned channels reset"
                        else:
                            df.pop(key)
                            msg = f"<#{ctx.channel.id}> removed assigned channel"
                        break
            df = pd.DataFrame(df)
            df.to_csv(f"server_settings/{ctx.guild.id}/channel_config.csv", index=False)

            await ctx.send(msg, ephemeral=True) # type: ignore
            # try except for error if log channel is unassigned
            try: await bot.get_channel(int(df["log_channel"][0])).send(msg) # type: ignore
            except: pass

    @bot.slash_command()
    async def assign_leaderboard_channel(ctx, main_event):
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You are not authorized to run this command.", ephemeral=True) # type: ignore
        else:
            competition_results_path = f"server_settings/{ctx.guild.id}/competition_results.csv"
            channel_config_path = f"server_settings/{ctx.guild.id}/channel_config.csv"
            config_dict =  pd.read_csv(channel_config_path).to_dict("list")

            def update_lb(bttn_label):
                comp_data_df = pd.read_csv(competition_results_path)
                sorted_data = comp_data_df.sort_values(by="average", ascending=False).to_dict("list")

                leaderboard = "⠀"
                placement = 1
                for x in range(len(sorted_data['event_name'])):
                    if sorted_data['event_name'][x] == bttn_label[:len(bttn_label)-2]:
                        leaderboard = f"{leaderboard}\n{placement}. **<@{sorted_data['discord_id'][x]}>** {sorted_data['average'][x]} Ao5"
                        placement += 1

                embed = nextcord.Embed(title=f"Live {bttn_label[:len(bttn_label)-2]} results")
                embed.add_field(name="⠀", value=leaderboard)
                return embed
            
            class EventButtons:
                def __init__(self, bttn_label):
                    async def button_callback(ctx):
                        await ctx.send(embed=update_lb(bttn_label), ephemeral=True)

                    self.button = Button(label=bttn_label[:len(bttn_label)-2])
                    if not bttn_label == "log_channel" or bttn_label == main_event: view.add_item(self.button)
                    self.button.callback = button_callback  # type: ignore

            view=View(timeout=604800)
            for key in config_dict:
                EventButtons(key)

            
            msg = await ctx.send(embed=update_lb(f"{main_event}__"), view=view)
            
            while True:
                await msg.edit(embed=update_lb(f"{main_event}__"))
                await asyncio.sleep(60)
