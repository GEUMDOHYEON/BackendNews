from fastapi import APIRouter, HTTPException
from database import mysql_create_session
from schemas.board import postWrite_Model, PostDelete_Model, CommentWrite_Model, CommentUpload_Modal
from tokens import expirecheck
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
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

# 토큰 유효한지 확인
# 유저 아이디로 제어


# 게시판 글 작성 / 수정
@router.post("/postWrite")
async def write(postWrite_data : postWrite_Model):
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 토큰 유효한지 확인 
  # expirecheck(postWrite_data.access_token)
  
  # 유저 정보 - 토큰 디코딩 후 - 닉네임 가져오기
  payload = jwt.decode(postWrite_data.access_token, SECRET_KEY, argorithms = [ALGORITHM])
  
  user_nickname = payload.get("nickname")
  user_email = payload.get("email")
  
  # 게시판 정보 - 제목, 내용, 작성 시간
  community_title = postWrite_data.community_title
  community_content = postWrite_data.community_content
  
  # 작성 시간을 년, 달, 일 순으로 가져오기
  now = datetime.now()
  community_createat = now.strftime("%Y-%m-%d")
  
  # 사용자 이메일이 유효하지 않을 시 토큰 인증 실패
  if user_email is None:
    raise HTTPException(status_code = 400, detail = "토큰 인증 실패")
  
  # 새로운 글인지 확인
  if(postWrite_data.isNewWrite):
    try:
      # 글 생성 
      # 입력 받은 값을 가져오기
      sql = "INSERT INTO `NEWS`.`Community` (`community_title`, `user_nickname`, `community_content`, `community_createat`) VALUES (%s, %s, %s, %s);"
      cur.execute(sql,(community_title,user_nickname,community_content,community_createat))
      conn.commit()
    except Exception as e:
      conn.rollback()
      # 에러 발생시 예외 메세지 (detail)를 전달 
      raise HTTPException(status_code=401, detail=str(e))
    finally:
      conn.close()
  else:
    # 글 수정 
    try:
      community_id = postWrite_data.community_id
      sql = 'UPDATE Community SET community_content = %s WHERE community_id = %s;'
      cur.execute(sql,(community_content,community_id))
      conn.commit()
    except Exception as e:
      conn.rollback()
      raise HTTPException(status_code=401, detail=str(e))
    finally:
      conn.close()
  
  return {"status_code" : 201, "message" : "업로드 성공"}

# 게시판 목록 불러오기
@router.post("/postUpload")
async def upload():
  conn, cur = mysql_create_session()

  # 커뮤니티 테이블의 총 레코드 수 계산 
  sql = 'SELECT COUNT(*) FROM Community;'
    
  cur.execute(sql)
  rowcount = cur.fetchone()
  # 총 게시물 개수
  rowcount = rowcount["COUNT(*)"]
  data = []

  # 게시물 데이터를 10개 단위로 나눠서 배열에 저장
  for i in range(0,rowcount,10):
    sql = 'SELECT community_id,community_title,user_nickname,community_createat FROM Community ORDER BY community_id DESC limit %s;'
    cur.execute(sql,(i))
    tend = cur.fetchall()
    data.append(tend)
#   print(data)

  conn.close()
  return {"status_code" : 201, "message" : "불러오기 성공"}

# 게시판 글 로딩
@router.post("/postLoad")
async def load():
  
  return {"status_code" : 201, "message" : "불러오기 성공"}


# 게시판 글 삭제
@router.delete("/postRemove")
async def remove(postDelete_data : PostDelete_Model):
  
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 유저 정보 - 토큰 디코딩 후 - 아이디, 닉네임 가져오기
  user_nickname = jwt.decode(postDelete_data.access_token, SECRET_KEY, argorithms = [ALGORITHM])
  
  community_id = postDelete_data.community_id

  conn, cur = mysql_create_session()
  sql = 'SELECT user_nickname FROM Community WHERE community_id=%s;'

  cur.execute(sql,(community_id))
  user_nickname = cur.fetchone()
  
  if (user_nickname["user_nickname"] == postDelete_data["user_nickname"]) :
    try:
      sql = 'DELETE FROM Community WHERE community_id=%s;'
      cur.execute(sql,(community_id))
      conn.commit()
    except Exception as e:
      conn.rollback()
    finally:
      conn.close()
    return {"status" : 204, "message" : "삭제완료"}
  
  return {"status" : 401, "message" : "삭제불가"}

@router.post("/commentWrite")
async def remove(commentWrite_data : CommentWrite_Model):
  comment_content = commentWrite_data.comment_content
  comment_id = commentWrite_data.comment_id
  
  payload = jwt.decode(commentWrite_data.access_token, SECRET_KEY, argorithms = [ALGORITHM])
  
  user_nickname = payload.get("nickname")
  user_email = payload.get("email")
  
  conn, cur = mysql_create_session()
  try:
    sql = "INSERT INTO comment (postnum, nick, data) VALUES ({}, '{}', '{}');".format(comment_id,user_nickname,comment_content)
    #print(sql)
    cur.execute(sql)
    #print("완료")
    conn.commit()
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=400, detail=str(e))
  finally:
    conn.close()

    return {"status":201,"message":"등록완료"}
  
@router.get("/CommentUpload/{num}")
async def commentUpload (commentUpload : CommentUpload_Modal):
  comment_id = commentUpload.comment_id
  
  conn, cur = mysql_create_session()
    
  payload = jwt.decode(commentUpload.access_token, SECRET_KEY, argorithms = [ALGORITHM])
  
  user_nickname = payload.get("nickname")
  user_email = payload.get("email")

  sql = "SELECT user_nickname,comment_content FROM Community_Comments WHERE comment_id={} ORDER BY comment_id DESC;".format(comment_id)
  cur.execute(sql)
  data = cur.fetchall()
  conn.close()

  return {"status":201,"message":"댓글 전송 성공"}
