from fastapi import FastAPI
from routers import users, news,board
# 백그라운드 스케줄러
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import get_news_from_api
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  scheduler = BackgroundScheduler()
  scheduler.add_job(get_news_from_api, 'interval', hours=10)
  scheduler.start()

  get_news_from_api()

  yield

  scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


app.include_router(users.router)
app.include_router(news.router)
app.include_router(board.router)

@app.get("/")
def helloWorld():
  return {"HELLO WORLD"}