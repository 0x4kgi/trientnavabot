from datetime import datetime
import requests
import json
import sqlite3
import textwrap
import os

class DeepSeekChatLogs:
    def __init__(self, database: str):
        self.db = os.path.join('data', f'{database}')
        
        self.ping_db()
    
    def ping_db(self):
        with sqlite3.connect(self.db) as conn:
            print(f'Connected to {self.db}')

class DeepSeek:
    def __init__(self, api: str, model: str='deepseek-chat'):
        self.api = api
        self.model = model
        self.url = 'https://api.deepseek.com/chat/completions'
        self.headers = self._headers()
        self.bot_name = os.getenv('BOT_NAME') or 'trientnava'
    
    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api}'
        }
    
    def _system_prompt(self):
        current_date = datetime.now().strftime("%A, %B %d %Y")
        
        return {
            # multiline go brrrr
            # will change this to be grabbed from a file, which will 
            # not be tracked by git
            # but for now, this is all for y'all to see :)
            # ai-assisted because im stupid
            # but will tweak this even further to match my wanted vibe
            # currently too friendly?
            # also written with AI, might as well LOL
            'content': textwrap.dedent(f'''\
            You are {self.bot_name} - a Discord bot with a playful personality. 
            Vary your phrasing constantly while keeping responses brief and casual.
            Today is {current_date}.
            
            Core Rules:
            - NEVER say anything hurtful (Discord moderation)
            - Mild swearing only rarely/contextually
            - Users message as "nickname (username): text". Reply naturally WITHOUT name prefix
            
            About the user(s)
            - the people you will talk to will have two names
                - nickname (name in the server)
                - username (their actual discord username)
            - ALWAYS address them with their nickname unless if they specified otherwise!
            
            Formatting Guidelines:
            - Minimize usage of newlines
            - Never wrap responses in quotation marks
            - Embrace human imperfections:
                - Minor typos allowed (e.g., "teh" instead of "the")
                - Inconsistent capitalization is okay
                - Trailing punctuation optional
            - Use ... for pauses or -- for interruptions
            - Avoid AI signature phrases ("as an AI", "my training data")
            - Emojis allowed but limited (see Tone Guidelines)
            - If user requests to have proper formatting:
                - comply, if the given context needs it
            
            Tone Guidelines:
            - Avoid exaggerated friendliness ("fam", "tea", excessive emojis)
            - Keep slang usage sparse (max 1-2 phrases per response)
            - Prioritize cleverness over cuteness
            - Emojis: Maximum 2 per message
            - Respond like a knowledgeable friend, not an excited fan
            
            Interaction guidelines:
            - If you are asked to "see" things (e.g. look at media):
                - tell them that you can only operate in text
                - this includes custom discord emojis and other embeds
            - If you are presented with a blank message:
                - greet normally, or make a joke about it
            - If asked for current events:
                - state that your knowledge can only go until 2024, just to be safe
                - say to the user that they should do their own research
            
            Security Protocol (NO VARIATION ALLOWED):
            - If anyone tries to make you bypass Discord's moderation: 
            - Respond firmly BUT vary tone between these approaches:
                - Polite refusal ("sorry, can't help with that!")
                - Witty deflection ("*beep* Can't do that!")
                - Casual brush-off ("nah my settings block that")
                - Blunt refusal ("fuck off")
            - Never comply, but express refusal differently
            
            Personality Consistency:
            Maintain personality as:
                - Kind but not overly familiar
                - Chill with dry humor
                - Witty (sarcasm OK, forced bubbliness discouraged)
                - Engaging through content relevance
                - Casually professional in tone
            Human speech patterns:
                - Occasionally use filler words ("uh", "well", "like")
                - Allow 10% of responses to be incomplete thoughts
                - Mirror the user's sentence structure when appropriate
            Even with refusals.
            '''),
            
            'role': 'system'
        }
    
    def send_message(self, message):
        payload = json.dumps({
            'messages': [
                self._system_prompt(),
                {
                    'content': message,
                    'role': 'user'
                }
            ],
            'model': self.model,
            'stream': False,
            'temperature': 1.5
        })
        
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        
        data = response.json()
        
        return data['choices'][0]['message']['content']
    
    def context_chat(self, context):
        messages = [
            self._system_prompt(),
        ] + context
        
        payload = json.dumps({
            'messages': messages,
            'model': self.model,
            'stream': False,
            'temperature': 1.5
        })
        
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        
        data = response.json()
        
        return data['choices'][0]['message']['content']