import discord
from discord.ext import commands

class Template(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(
        name='hello',
        aliases=['hi', 'hey'],
        help='detailed help desc',
        description='short help desc',
        hidden=True, # hide from help
        usage=';hello',
        enabled=True,
    )
    async def hello(self, ctx: commands.Context):
        await ctx.send('hey! :wave:')

    @discord.slash_command(
        # same attribs also
    )
    async def hello(self, ctx: discord.ApplicationContext):
        await ctx.respond('yo!!')

def setup(bot):
    bot.add_cog(Template(bot))