from datetime import datetime
import requests
import json
import sqlite3
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
        self.system_prompt_path = 'default.md'
    
    def _headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api}'
        }
    
    def _prompt_from_file(self, path: str):
        with open(f'llm/prompts/{path}') as file:
            return file.read()
    
    def _prompt_config(self, prompt: str, replacements: list[dict[str, str]]):
        for string, replacement in replacements:
            prompt = prompt.replace(string, replacement)
        return prompt
    
    def _system_prompt(self):
        current_date = datetime.now().strftime("%A, %B %d %Y")
        
        prompt = self._prompt_from_file(self.system_prompt_path)
        prompt = self._prompt_config(prompt, [
            ('{{bot_name}}', self.bot_name),
            ('{{current_date}}', current_date),
        ])
        
        return {
            'content': prompt,
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