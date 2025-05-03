import discord
from discord.ext import commands

class Cogger(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cogging(self, ctx: commands.Context):
        await ctx.send('ye cogging rn bruh')

    @commands.command()
    async def hey_ron(self, ctx: commands.Context):
        await ctx.send('hey, billy')

def setup(bot):
    bot.add_cog(Cogger(bot))