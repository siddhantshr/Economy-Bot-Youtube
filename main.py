import discord
from discord.ext import commands
from data.secrets import secret

economy = commands.Bot(
    command_prefix="!"
)
economy.remove_command('help')

@economy.event
async def on_ready():
    print(f'Logged in as {economy.user}')

cogs = ['cogs.economy']

if __name__ == '__main__':
    for cog in cogs:
        economy.load_extension(cog)
        print(f"Booted up {cog[5:]}")

@economy.command(name="load")
async def load(ctx, cog):
    if ctx.author.id == 711444754080071714:
        if cog not in cogs:
            return await ctx.send(
                f"{cog} is not a valid cog!"
            )
        
        economy.load_extension(cog)
    else:
        await ctx.send("You are not the developer!")

@economy.command(name="unload")
async def unload(ctx, cog):
    if ctx.author.id != 711444754080071714:
        return await ctx.send(
            "You are not the developer!"
        )
    if cog not in cogs:
        return await ctx.send(
            f"{cog} is not a valid cog!"
        )
    
    economy.unload_extension(cog)

economy.run(secret['token'])