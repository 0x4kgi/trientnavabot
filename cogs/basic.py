import discord
import random
from discord.ext import commands

class Basic(commands.Cog):
    
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        latency = self.bot.latency * 1000
        await ctx.send(f'the bot pongs back within {latency:,.2f}ms')

    @commands.command()
    async def echo(self, ctx: commands.Context, *, message):
        await ctx.send(message)

    @commands.command()
    async def dice(self, ctx: commands.Context, min=1, max=6):
        num = random.randint(min, max)
        await ctx.send(f'I rolled a {num}')

    @discord.slash_command()
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond('yo!!')

def setup(bot):
    bot.add_cog(Basic(bot))