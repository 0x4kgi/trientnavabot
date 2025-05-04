from ossapi import Ossapi, User
from dotenv import load_dotenv
import os

from ossapi.models import UserStatistics

load_dotenv()
api = Ossapi(
    client_id=os.getenv('OSU_CLIENT_ID'),
    client_secret=os.getenv('OSU_CLIENT_SECRET')
)


def user_fetch(username: str, mode: str='osu'):
    try:
        user = api.user(user=username, mode=mode)
        return user
    except Exception as e:
        print(e)
        return None