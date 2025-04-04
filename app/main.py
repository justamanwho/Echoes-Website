from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import Tweet
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request



app = FastAPI()
import os
load_dotenv()
SECRET_API_KEY = os.getenv('SECRET_API_KEY')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # one level up from 'app/'

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)
# Enable templates (HTML rendering)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int] = []  # Optional

@app.post("/api/tweets")
def create_tweet(
    tweet: TweetCreate,
    api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    new_tweet = Tweet(
        tweet_data=tweet.tweet_data,
        tweet_media_ids=",".join(map(str, tweet.tweet_media_ids))
    )
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)

    return {"result": True, "tweet_id": new_tweet.id}

# @app.post("/api/media")
# def load_media(
#     tweet: TweetCreate,
#     api_key: str = Header(None),
#     db: Session = Depends(get_db)
# ):
#