from fastapi import FastAPI
from routers import users, news,board
# 백그라운드 스케줄러
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import get_news_from_api
from contextlib import asynccontextmanager

# 백그라운드 스케줄링 작업
@asynccontextmanager
async def lifespan(app: FastAPI):
  scheduler = BackgroundScheduler()
  # 1시간마다 새로운 뉴스를 가져오기 위해 뉴스 스크래핑 작업 진행
  scheduler.add_job(get_news_from_api, 'interval', hours=1)
  scheduler.start()
  # 서버 실행 후 곧바로 뉴스 스크래핑 작업 진행
  # get_news_from_api()

  yield

  scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


app.include_router(users.router)
app.include_router(news.router)
app.include_router(board.router)

@app.get("/")
def helloWorld():
  return {"HELLO WORLD"}
