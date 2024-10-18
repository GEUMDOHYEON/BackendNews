from fastapi import FastAPI, Request, BackgroundTasks
from routers import users, news,board
# CORS 정책
from fastapi.middleware.cors import CORSMiddleware
# 백그라운드 스케줄러
from apscheduler.schedulers.background import BackgroundScheduler
import os
# 로깅
import logging
from datetime import datetime

from scheduler import get_news_from_api, Deleted_Withdrawal_Member
from contextlib import asynccontextmanager

# 백그라운드 스케줄링 작업
@asynccontextmanager
async def lifespan(app: FastAPI):
  # 서버가 구동되면 실행되는 코드

  scheduler = BackgroundScheduler()
  # 1시간마다 새로운 뉴스를 가져오기 위해 뉴스 스크래핑 작업 진행
  scheduler.add_job(get_news_from_api, 'interval', hours=1)
  # 24시간마다 30일 지난 탈퇴계정 삭제
  scheduler.add_job(Deleted_Withdrawal_Member, 'interval', days=1)
  scheduler.start()

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
       "url": "https://coin-news-site.web.app/"
    },
    
}

app = FastAPI(lifespan=lifespan, **SWAGGER_HEADERS)


# 로깅 설정
logging.basicConfig(filename='info.log', level=logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)


# 백그라운드 작업으로 처리할 로깅 함수
def log_request_info(req_method: str, req_url: str):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{current_time}] Request: {req_method} {req_url}")


# CROS 허용 ip
origins = [
   os.environ['FRONTEND_URL'],
]

#api설정값
app.add_middleware(
    CORSMiddleware,
    # 허용 ip
    #allow_origins=origins,
    #일단 열어둠
    allow_origins=["*"],
    # 인증, 쿠키
    #allow_credentials=True,
    # 허용 메소드
    allow_methods=["GET","POST","PUT","DELETE"],
    # 허용 헤더
    allow_headers=["*"],  
)


app.include_router(users.router)
app.include_router(news.router)
app.include_router(board.router)


# Request 로깅 미들웨어
@app.middleware("http")
async def log_request(request: Request, call_next):

    # 요청 메서드와 URL 로깅
    req_method = request.method
    req_url = str(request.url)

    # 요청 처리 후 바로 응답 반환
    response = await call_next(request)

    # 요청 정보를 백그라운드 로깅
    Background_Tasks = BackgroundTasks()
    Background_Tasks.add_task(log_request_info(req_method, req_url))

    return response

@app.get("/")
def helloWorld():
  return {"HELLO WORLD"}


