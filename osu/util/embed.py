from typing import Literal
import discord
from ossapi import Ossapi, Score, User

def osu_profile_card_embed(player: User, player_best: list[Score], mode: str, mini_embed: bool=False) -> discord.Embed:
    pp = player.statistics.pp or -1
    
    global_rank = player.statistics.global_rank or -1
    country_rank = player.statistics.country_rank or -1
    country_code = player.country.code
    
    play_time = player.statistics.play_time / 60 / 60
    
    grade_x = player.statistics.grade_counts.ss + player.statistics.grade_counts.ssh
    grade_s = player.statistics.grade_counts.s + player.statistics.grade_counts.sh
    grade_a = player.statistics.grade_counts.a
    
    gamemode = proper_mode(mode)
    
    best_range = top_play_stats(player_best)
    top_score = best_range[0]
    top_100 = best_range[1]
    best_spread = top_score - top_100
    
    description = f"""Performance: {pp:,.2f}pp ({player.statistics.hit_accuracy:,.2f}%)
    SS / S / A: {grade_x:,} / {grade_s:,} / {grade_a:,}
    Top 1 / 100: {top_score:,.2f}pp / {top_100:,.2f}pp ({best_spread:,.2f}pp diff)
    Level: {player.statistics.level.current:,}
    Play count: {player.statistics.play_count:,} ({play_time:,.2f} hours)
    Ranked score: {player.statistics.ranked_score:,}
    Total score: {player.statistics.total_score:,}
    """
    
    embed = discord.Embed(
        title=f'{player.username}\'s statistics for {gamemode}',
        color=player.profile_hue,
        description=description,
    )
    
    embed.set_author(
        name=f'{player.username} (#{global_rank}, {country_code}#{country_rank})',
        url=f'https://osu.ppy.sh/users/{player.id}',
        icon_url=f'https://osu.ppy.sh/images/flags/{player.country.code}.png',
    )
    
    if not mini_embed:
        embed.set_thumbnail(url=player.avatar_url)
        embed.set_image(url=player.cover_url)
    
    return embed


def top_play_stats(player_best: list[Score]):
    count = len(player_best)
    
    top_pp = player_best[0].pp
    top_end = player_best[count - 1].pp
    
    return (top_pp, top_end)


def proper_mode(mode: str|int) -> str:
    match mode:
        case 'osu' | 0 | 'o':
            return 'osu!'
        case 'taiko' | 1 | 't' | 'taco':
            return 'osu!taiko'
        case 'fruits' | 2 | 'fruit' | 'catch' | 'ctb' | 'c' | 'minigame':
            return 'osu!catch'
        case 'mania' | 3 | 'm' | '4k' | '7k':
            return 'osu!mania'


def color_int(color_hex: str) -> int:
    if color_hex is None:
        return None
    
    color_hex = color_hex.lstrip('#')
    return int(color_hex, 16)