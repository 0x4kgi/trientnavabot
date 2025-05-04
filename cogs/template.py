import discord
from discord.ext import commands

class Template(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command(
        name='hello',
        aliases=['t_hi', 't_hey'],
        help='detailed help desc',
        description='short help desc',
        hidden=True, # hide from help
        usage=';template_prefix_hello',
        enabled=True,
    )
    async def template_prefix_hello(self, ctx: commands.Context):
        await ctx.send('hey! :wave:')

    @discord.slash_command(
        # same attribs also
    )
    async def template_slash_hello(self, ctx: discord.ApplicationContext):
        await ctx.respond('yo!!')

def setup(bot):
    bot.add_cog(Template(bot))