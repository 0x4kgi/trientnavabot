import discord
from discord.ext import commands
from ossapi import User
from osu.user.fetch import user_fetch, user_top_plays
from osu.util.embed import osu_profile_card_embed

class Osu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
        
    async def send_profile_card_embed(
            self, ctx: commands.Context, username: str, 
            mode: str, mini: bool=False):
        await ctx.trigger_typing()
        
        player = user_fetch(username, mode)
        player_best = user_top_plays(id=player.id, mode=mode)
        
        if player is None:
            await ctx.send(f'Player {username} not found')
            return
        
        player_embed = osu_profile_card_embed(
            player=player, player_best=player_best, mode=mode, mini_embed=mini)
        await ctx.send(embed=player_embed)
    
    
    @commands.command()
    async def osu(self, ctx: commands.Context, username: str):
        await self.send_profile_card_embed(ctx, username, 'osu')
    
    
    @commands.command()
    async def taiko(self, ctx: commands.Context, username: str):
        await self.send_profile_card_embed(ctx, username, 'taiko')
    
    
    @commands.command()
    async def catch(self, ctx: commands.Context, username: str):
        await self.send_profile_card_embed(ctx, username, 'fruits')
    
    
    @commands.command()
    async def mania(self, ctx: commands.Context, username: str):
        await self.send_profile_card_embed(ctx, username, 'mania')
    
    
    @commands.command()
    async def osuall(self, ctx: commands.Context, username: str):
        # TODO: remake embed for this one
        for mode in ['osu', 'taiko', 'fruits', 'mania']:
            await self.send_profile_card_embed(ctx, username, mode, True)
    

def setup(bot):
    bot.add_cog(Osu(bot))