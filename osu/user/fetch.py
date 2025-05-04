from ossapi import Ossapi, ScoreType, User
from dotenv import load_dotenv
import os

from ossapi.models import Score

load_dotenv()
api = Ossapi(
    client_id=os.getenv('OSU_CLIENT_ID'),
    client_secret=os.getenv('OSU_CLIENT_SECRET')
)


def user_fetch(username: str, mode: str='osu') -> User | None:
    try:
        user = api.user(user=username, mode=mode)
        return user
    except Exception as e:
        print(e)
        return None


def user_top_plays(
        *, 
        id: int=None, 
        username: str=None, 
        mode: str='osu', 
        limit: int=100) -> list[Score] | None:
    try:
        user_id = id or api.user(user=username, mode=mode).id
        
        user_best = api.user_scores(
            user_id=user_id, 
            type=ScoreType.BEST,
            mode=mode,
            limit=limit
        )

        return user_best
    except Exception as e:
        print(e)
        return None


def user_recent(username: str, mode: str, limit: int=5):
    pass