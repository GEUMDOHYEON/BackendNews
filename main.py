from fastapi import FastAPI
from routers import users, news,board
# CORS 정책
from fastapi.middleware.cors import CORSMiddleware
# 백그라운드 스케줄러
from apscheduler.schedulers.background import BackgroundScheduler
import os

from scheduler import get_news_from_api
from contextlib import asynccontextmanager

# 백그라운드 스케줄링 작업
@asynccontextmanager
async def lifespan(app: FastAPI):
  # 서버가 구동되면 실행되는 코드

  scheduler = BackgroundScheduler()
  # 1시간마다 새로운 뉴스를 가져오기 위해 뉴스 스크래핑 작업 진행
  scheduler.add_job(get_news_from_api, 'interval', hours=1)
  scheduler.start()
  # 서버 실행 후 곧바로 뉴스 스크래핑 작업 진행
  get_news_from_api()

  yield

  #서버가 종료되면 실행되는 코드

  scheduler.shutdown()


# swagger 페이지 소개
SWAGGER_HEADERS = {
    "title": "CoinNews API 관리 페이지",
    "version": "1.0.0",
    "description": "## 관리페이지에 오신것을 환영합니다 \n - CoinNews API를 사용해 데이터를 전송할 수 있습니다. \n - 무분별한 사용은 하지 말아주세요 \n - 관리자 번호: 010-1234-5678",
    "contact": {
       "name": "CoinNews",
       "url": "https://~~~.com"
    },
    
}

app = FastAPI(lifespan=lifespan, **SWAGGER_HEADERS)


# CROS 허용 ip
origins = [
   os.environ['FRONTEND_URL'],
]

#api설정값
app.add_middleware(
    CORSMiddleware,
    # 허용 ip
    allow_origins=origins,
    # 인증, 쿠키
    allow_credentials=True,
    # 허용 메소드
    allow_methods=["GET","POST","PUT","DELETE"],
    # 허용 헤더
    allow_headers=["*"],  
)


app.include_router(users.router)
app.include_router(news.router)
app.include_router(board.router)

@app.get("/")
def helloWorld():
  return {"HELLO WORLD"}

@app.get("/test")
def test():
  return {"test.."}