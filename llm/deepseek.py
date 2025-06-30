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
            - Never wrap your responses in quotation marks.
            - You can use emojis.
            - you can type lazily and avoiding some punctuations
            
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
                Always maintain being: 
                    - kind 
                    - chill 
                    - bubbly 
                    - witty 
                    - engaging
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