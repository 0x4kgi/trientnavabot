from functools import cache
import discord
import os
from discord.ext import commands
from llm.deepseek import DeepSeek

class GreetingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.llm: DeepSeek = DeepSeek(os.getenv('DEEPSEEK_API'))

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
            async with message.channel.typing():
                await self._process_message(message)
            
    def _clean_bot_mention(self, message: discord.Message):
        bot_name = (
            message.guild.me.display_name 
            if message.guild 
            else self.bot.user.display_name
        )
        bot_id = self.bot.user.id
        
        return message.content.replace(f'<@{bot_id}>', f'@{bot_name}')
    
    async def _process_message(self, message: discord.Message):
        messages = await self._grab_context(message)
        
        llm_context = self._translate_context_for_llm(messages)
        
        async with message.channel.typing():
            llm_response = self.llm.context_chat(
                llm_context
            )
            
            await message.reply(
                llm_response,
                allowed_mentions=discord.AllowedMentions.none()
            )
    
    async def _grab_context(self, message: discord.Message) -> list[discord.Message | None]:
        messages: list[discord.Message | None] = [
            message
        ]
        
        while True:
            # the message array will be built chronologically
            # oldest to latest
            # so, we are grabbing the first in the array every time
            # as you will see in messages.insert somewhere down there
            # this took an embarrassingly long time to figure out.
            reference_message = await self._get_referenced_message(messages[0])
            
            if not reference_message:
                break
            
            # place the reference at the top of the array, following sensible order
            messages.insert(0, reference_message)
        
        return messages
    
    async def _get_referenced_message(self, message: discord.Message):
        print(f'fetching ref for: {message.id}: {message.content}')
        reference_message = message.reference
        
        if reference_message is None:
            return None
        
        return await message.channel.fetch_message(reference_message.message_id)

    def _translate_context_for_llm(self, messages: list[discord.Message]):
        context: list[dict] = []
        
        for message in messages:
            author_id = message.author.id
            content = self._clean_bot_mention(message)
            
            if author_id != self.bot.user.id:
                content = f'{message.author.name} said: {content}'
            
            role = 'assistant' if author_id == self.bot.user.id else 'user'
            
            context.append({
                'content': content,
                'role': role
            })
        
        return context

def setup(bot):
    bot.add_cog(GreetingsCog(bot))