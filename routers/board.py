from fastapi import APIRouter, HTTPException
from database import mysql_create_session
from schemas.board import postWrite_Model, PostDelete_Model  
from datetime import datetime
from dotenv import load_dotenv
import jwt
import os

router = APIRouter(
  prefix="/board",
  tags=["board"]
)

# 환경변수 이용을 위한 전역변수
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 루트 경로에 .env파일로 값 설정
load_dotenv(os.path.join(BASE_DIR, ".env"))
# jwt에 필요한 전역변수
SECRET_KEY = os.environ["SECRET_KEY"]
# 알고리즘
ALGORITHM = "HS256"

# 게시판 글 작성
@router.post("/postWrite")
async def write(postWrite_data : postWrite_Model):
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 유저 정보 - 토큰 디코딩 후 - 아이디, 닉네임 가져오기
  user_nickname = jwt.decode(postWrite_data.access_token, SECRET_KEY, argorithms = [ALGORITHM])
  
  # 게시판 정보 - 제목, 내용, 작성 시간
  community_title = postWrite_data.community_title
  community_content = postWrite_data.community_content
  
  # 작성 시간을 년, 달, 일 순으로 가져오기
  now = datetime.now()
  community_createat = now.strftime("%Y-%m-%d")
  
  try:
    # 입력 받은 값을 가져오기
    sql = "INSERT INTO `USER`.`Community` (`community_title`, `user_nickname`, `community_content`, `community_createat`) VALUES (%s, %s, %s, %s);"
    cur.execute(sql,(community_title,user_nickname,community_content,community_createat))
    conn.commit()
  except Exception as e:
    conn.rollback()
    # 에러 발생시 예외 메세지 (detail)를 전달 
    raise HTTPException(status_code=400, detail=str(e))
  finally:
    conn.close()
    
  return {"status_code" : 400, "message" : "업로드 성공"}

# 게시판 글 불러오기
@router.posr("/postUpload")
async def Upload(postUpload_data : PostUpload_Model):
  
  return  {"불러오기 성공"}

# 게시판 글 삭제
@router.post("/postRemove")
async def remove(postDelete_data : PostDelete_Model):
  
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 유저 정보 - 토큰 디코딩 후 - 아이디, 닉네임 가져오기
  user_nickname = jwt.decode(postDelete_data.access_token, SECRET_KEY, argorithms = [ALGORITHM])
  
  community_id = postDelete_data.community_id

  conn, cur = mysql_create_session()
  sql = 'SELECT writer FROM main_board WHERE community_id=%s;'

  cur.execute(sql,(community_id))
  writer = cur.fetchone()
  
  if (writer["writer"] == postDelete_data["user_nickname"]) :
    try:
      sql = 'DELETE FROM main_board WHERE community_id=%s;'
      cur.execute(sql,(community_id))
      conn.commit()
    except Exception as e:
      conn.rollback()
    finally:
      conn.close()
    return {"status" : 201, "message" : "삭제완료"}
  
  return {"status" : 401, "message" : "삭제불가"}


# 게시판 글 수정
@router.post("/post")
async def update():
  return {"수정 성공"}

