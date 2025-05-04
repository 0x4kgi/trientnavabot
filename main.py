from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=';',
    intents=intents,
)

cog_list = [
        'basic',
        'osu',
    ]

for cog in cog_list:
    print(f'Loading cog: {cog}')
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')


@bot.command()
@commands.is_owner()
async def reload(ctx: commands.Context, cog: str):
    try:
        bot.reload_extension(f'cogs.{cog}')
        await ctx.send(f':white_check_mark: Loaded {cog}')
    except Exception as e:
        await ctx.send(f':x: Failed to load {cog} ({e})')


if __name__ == '__main__':
    load_dotenv()

    bot.run(os.getenv("TOKEN"))
