from functools import cache
import discord
import os
from discord.ext import commands
from llm.deepseek import DeepSeek

class ThreadChat(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.llm: DeepSeek = DeepSeek(os.getenv('DEEPSEEK_API'))
        self.processing_threads = set()
    
    def _clean_bot_mention(self, message: discord.Message):
        bot_name = (
            message.guild.me.display_name 
            if message.guild 
            else self.bot.user.display_name
        )
        bot_id = self.bot.user.id
        
        return message.content.replace(f'<@{bot_id}>', f'@{bot_name}')
    
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
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        # Create thread on ping and answer user's goofy query
        # Will this get fucked up when multiple people message?
        # No one will know LMAOoooooooooooooo
        if self.bot.user in message.mentions and not isinstance(message.channel, discord.Thread):
            try:
                thread = await message.create_thread(name='New thread!')
                thinking_message = await thread.send('*Thinking...*')
                
                # TODO: find a way to "lock" the bot when sending a first message
                clean_message = self._clean_bot_mention(message)
                single_response = self.llm.send_message(clean_message)
                await thinking_message.edit(single_response)
                
                thread_title_llm = self.llm.send_message(
                    f'Summarize the following in less than 5 (five) words: "{clean_message}"'
                )
                await thread.edit(name=thread_title_llm)
            except Exception as e:
                print(f'Cannot create thread: {e}')
            return

        # Ignore messages not in threads
        if not isinstance(message.channel, discord.Thread):
            return
        
        thread_id = message.channel.id
        if thread_id in self.processing_threads:
            return
        self.processing_threads.add(thread_id)
        
        try:
            thinking_message = await message.channel.send('*Thinking...*')
            
            # thanks chatgipity
            thread_messages = [msg async for msg in message.channel.history(limit=25)]
            thread_messages.reverse()
            
            llm_thread_context = self._translate_context_for_llm(thread_messages)
            llm_response = self.llm.context_chat(llm_thread_context)
            
            await thinking_message.edit(content=llm_response)
        except Exception as e:
            await thinking_message.edit(content='something wrong happened. :sob: (code error, check console)')
            print(f'Error in thread {thread_id}: {e}')
        finally:
            self.processing_threads.remove(thread_id)

def setup(bot):
    bot.add_cog(ThreadChat(bot))