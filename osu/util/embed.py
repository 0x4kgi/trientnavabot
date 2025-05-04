import statistics
import discord
from ossapi import Ossapi, User

def osu_profile_card_embed(player: User) -> discord.Embed:

    pp = player.statistics.pp or -1
    global_rank = player.statistics.global_rank or -1
    country_rank = player.statistics.country_rank or -1
    country_code = player.country.code
    
    play_time = player.statistics.play_time / 60 / 60
    
    description = f"""Performance: {pp:,.2f}pp ({player.statistics.hit_accuracy:,.2f}%)
    Level: {player.statistics.level.current:,}
    Play count: {player.statistics.play_count:,} ({play_time:,.2f} hours)
    Ranked score: {player.statistics.ranked_score:,}
    Total score: {player.statistics.total_score:,}
    """
    
    embed = discord.Embed(
        title=player.username,
        color=player.profile_hue,
        description=description,
    )
    
    embed.set_author(
        name=f'{player.username} (#{global_rank}, {country_code}#{country_rank})',
        url=f'https://osu.ppy.sh/users/{player.id}',
        icon_url=f'https://osu.ppy.sh/images/flags/{player.country.code}.png',
    )
    
    embed.set_thumbnail(url=player.avatar_url)
    embed.set_image(url=player.cover_url)
    
    return embed

def color_int(color_hex: str) -> int:
    if color_hex is None:
        return None
    
    color_hex = color_hex.lstrip('#')
    return int(color_hex, 16)