import pandas as pd
import nextcord

def init_admin_cmds(bot):
    
    @bot.slash_command(name="view-channel-config", description="Show the ID of the log channel and event submission channels")
    async def view_channel_config(ctx): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
            await ctx.send(df, ephemeral=True)

    @bot.slash_command(name="clear-event-channels", description="Resets the event submission channels, doesn't effect the log channel")
    async def clear_event_channels(ctx): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
            df = {"log_channel": [df["log_channel"][0]]}
            df = pd.DataFrame(df)
            df.to_csv(f"server_settings/{ctx.guild.id}/channel_config.csv", index=False)

            await ctx.send("All event channels reset, log channel unchanged", ephemeral=True)
            try:
                await bot.get_channel(int(df["log_channel"][0])).send("All event channels reset, log channel unchanged")
            except:
                pass

    @bot.slash_command(name="set-log-channel", description="Sets the used channel to the log channel")
    async def set_log_channel(ctx): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)

        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
            df["log_channel"] = [ctx.channel.id]
            df = pd.DataFrame(df)
        
            try:
                await bot.get_channel(int(df["log_channel"][0])).send("**Channels updated**\n\n" + str(df))
                df.to_csv(f"server_settings/{ctx.guild.id}/channel_config.csv", index=False)
                await ctx.send("Channels updated", ephemeral=True)
            except:
                await ctx.send("Invalid channel", ephemeral=True)

    @bot.slash_command(name="set-event-channel", description="Use event_name in the desired channel, specify which channel with the log channel")
    async def set_event_channel(ctx, event_name): 
        if not ctx.user.guild_permissions.administrator:
            await ctx.response.send_message("You are not authorized to run this command.", ephemeral=True)
        else:
            df = pd.read_csv(f"server_settings/{ctx.guild.id}/channel_config.csv").to_dict("list")
            in_use = False
            for x in df:
                if str(df[x][0]) == str(ctx.channel.id):
                    in_use = True
                    await ctx.send("Channel is already in use", ephemeral=True)

                if not in_use:
                    response = {f"{event_name}_{len(df)}": [ctx.channel.id]}
                    df.update(response)  # type: ignore
                    new_data = pd.DataFrame(df)
                    new_data.to_csv(f"server_settings/{ctx.guild.id}/channel_config.csv", index=False)

                    await ctx.send(f"**Submit {event_name} results here! use the /submit-solves command**")
                    await ctx.send("Channels updated", ephemeral=True)
                    await bot.get_channel(int(df["log_channel"][0])).send("**Channels updated**\n\n" + str(df))