from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .models import Tweet

from fastapi import FastAPI, Depends, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable templates (HTML rendering)
templates = Jinja2Templates(directory="app/templates")

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
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")

    new_tweet = Tweet(
        tweet_data=tweet.tweet_data,
        tweet_media_ids=",".join(map(str, tweet.tweet_media_ids))
    )
    db.add(new_tweet)
    db.commit()
    db.refresh(new_tweet)

    return {"result": True, "tweet_id": new_tweet.id}

