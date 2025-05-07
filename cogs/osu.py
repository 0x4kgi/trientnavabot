import discord
from discord.ext import commands
from ossapi import User
from osu.user.fetch import user_fetch, user_top_plays
from osu.util.embed import osu_all_profile_embed, osu_profile_card_embed

class Osu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        
        
    async def send_profile_card_embed(
            self, ctx: commands.Context, username: str, 
            mode: str, mini: bool=False):
        await ctx.trigger_typing()
        
        player = user_fetch(username, mode)
        if player is None:
            await ctx.send(f'Player `{username}` not found')
            return
        
        player_best = user_top_plays(id=player.id, mode=mode)
        
        player_embed = osu_profile_card_embed(
            player=player, player_best=player_best, mode=mode, mini_embed=mini)
        await ctx.send(embed=player_embed)
    
    
    async def send_all_mode_card(self, ctx: commands.Context, username: str):
        await ctx.trigger_typing()
        
        player = user_fetch(username, 'osu')
        if player is None:
            await ctx.send(f'Player `{username}` not found')
            return
        
        taiko_statistic = user_fetch(username, 'taiko')
        catch_statistic = user_fetch(username, 'fruits')
        mania_statistic = user_fetch(username, 'mania')
        
        statistics = {
            'osu': player,
            'taiko': taiko_statistic,
            'catch': catch_statistic,
            'mania': mania_statistic,
        }
        
        top_plays = {
            'osu': user_top_plays(id=player.id, mode='osu'),
            'taiko': user_top_plays(id=player.id, mode='taiko'),
            'catch': user_top_plays(id=player.id, mode='fruits'),
            'mania': user_top_plays(id=player.id, mode='mania'),
        }
        
        player_embed = osu_all_profile_embed(player, statistics, top_plays)
        
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
        await self.send_all_mode_card(ctx, username)
    

def setup(bot):
    bot.add_cog(Osu(bot))