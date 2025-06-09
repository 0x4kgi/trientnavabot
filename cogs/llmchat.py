import discord
import os
from discord.ext import commands
from llm.deepseek import DeepSeek

class GreetingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if 'hello bot' in message.content.lower():
            # Just a debug.
            await message.reply(f'hello {message.author.display_name}!')
            # await message.channel.send(f'hello {message.author.display_name}!')
            return
        
        if self.bot.user in message.mentions:
            bot_name = (
                message.guild.me.display_name 
                if message.guild 
                else self.bot.user.display_name
            )
            bot_id = self.bot.user.id
            
            # old code that is not yet committed so im keeping
            # if message.reference:
            #     async with message.channel.typing():
            #         reference_message_id = message.reference.message_id
            #         reference_message = await message.channel.fetch_message(reference_message_id)
            #         content = reference_message.content
            #         await message.reply(
            #             f'You replied to: "{content}"~!'
            #         )
            #     return
            
            # await message.reply(
            #     f'You pinged {bot_name}? What\'s up?',
            #     allowed_mentions=discord.AllowedMentions.none()
            # )
            
            user_message = message.content.replace(f'<@{bot_id}>', f'@{bot_name}')
            #print(user_message, bot_id)
            
            llm = DeepSeek(os.getenv('DEEPSEEK_API'))
            
            async with message.channel.typing():
                llm_response = llm.send_message(
                    f'{message.author.display_name} said: {user_message}'
                )
                
                await message.reply(
                    llm_response,
                    allowed_mentions=discord.AllowedMentions.none()
                )
                return

def setup(bot):
    bot.add_cog(GreetingsCog(bot))