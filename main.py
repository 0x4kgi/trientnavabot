from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=os.getenv('BOT_PREFIX'),
    intents=intents,
)

cog_list = [
    'basic',
    'osu',
    'llmchat',
]

for cog in cog_list:
    print(f'Loading cog: {cog}')
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


@bot.command(
    aliases=['rcog'],
    hidden=True,
)
@commands.is_owner()
async def reloadcog(ctx: commands.Context, cog: str):
    try:
        bot.reload_extension(f'cogs.{cog}')
        await ctx.send(f':white_check_mark: Reloaded {cog}')
    except Exception as e:
        await ctx.send(f':x: Failed to reload {cog} ({e})')


@bot.command(
    aliases=['lcog'],
    hidden=True,
)
@commands.is_owner()
async def loadcog(ctx: commands.Context, cog: str):
    try:
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f':white_check_mark: Loaded {cog}')
    except Exception as e:
        await ctx.send(f':x: Failed to load {cog} ({e})')


if __name__ == '__main__':
    bot.run(os.getenv("TOKEN"))
