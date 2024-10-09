from fastapi import APIRouter, HTTPException, Depends
from database import mysql_create_session
from schemas.board import *
from fastapi.security import OAuth2PasswordBearer
from tokens import access_expirecheck
from datetime import datetime
from dotenv import load_dotenv
from routers.news import findUserID
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

# 헤더에 토큰 값 가져오기 위한 객체
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 게시판 글 작성
@router.post("/postWrite", response_model = Response_PostWrite_Model)
def write(postWrite_data : PostWrite_Model, access_token: str = Depends(oauth2_scheme)):
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 토큰 유효한지 확인 
  payload = access_expirecheck(access_token)
  
  # 유저 정보 - 토큰 디코딩 후
  user_email = payload['email']
  
  user_id = findUserID(user_email)
  
  # print(user_email)
  # print(user_nickname)
  # print(user_id)
  
  # 게시판 정보 - 제목, 내용, 작성 시간
  community_title = postWrite_data.community_title
  community_content = postWrite_data.community_content
  
  # print(community_content)
  # print(community_title)
  
  # 작성 시간을 년, 달, 일 순으로 가져오기
  now = datetime.now()
  community_createat = now.strftime("%Y-%m-%d")
  
  # print(community_createat)
  
  try:
    # 글 생성 
    # 입력 받은 값을 가져오기
    sql = "INSERT INTO Community (user_id, community_title, community_content, community_createat) VALUES (%s, %s, %s, %s)"
    cur.execute(sql,(user_id, community_title,community_content,community_createat))
    conn.commit()
    return Response_PostWrite_Model(status=201, message="업로드 성공")
  except Exception as e:
    conn.rollback()
    # 에러 발생시 예외 메세지 (detail)를 전달 
    raise HTTPException(status_code=401, detail=str(e))
  finally:
    conn.close()
    cur.close()
  

# 게시판 글 수정 
@router.put("/postEdit", response_model = Response_PostEdit_Model)
def edit(postEdit_data : PostEdit_Model, access_token: str = Depends(oauth2_scheme)):
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 토큰 유효한지 확인 
  payload = access_expirecheck(access_token)
  
  # 유저 정보 - 토큰 디코딩 후 - 닉네임 가져오기
  user_nickname = payload["nickname"]
  user_email = payload['email']
  
  user_id = findUserID(user_email)
  
  # print(user_email)
  # print(user_nickname)
  # print(user_id)
  
  # 게시판 정보 - 제목, 내용, 작성 시간
  new_community_title = postEdit_data.community_title
  new_community_content = postEdit_data.community_content
  new_community_id = postEdit_data.community_id
  
  # print(new_community_content)
  # print(new_community_title)
  
  # 작성 시간을 년, 달, 일 순으로 가져오기
  now = datetime.now()
  community_createat = now.strftime("%Y-%m-%d")
  
  # print(community_createat)
  
  
  try:
    # 글 생성 
    # 입력 받은 값을 가져오기
    sql = " UPDATE Community SET community_title = %s, community_content = %s, community_createat = %s WHERE community_id = %s AND user_id = %s "
    cur.execute(sql,( new_community_title,new_community_content,community_createat, new_community_id, user_id))
    conn.commit()
    return Response_PostEdit_Model(status=201, message="수정 성공")
  except Exception as e:
    conn.rollback()
    # 에러 발생시 예외 메세지 (detail)를 전달 
    raise HTTPException(status_code=401, detail=str(e))
  finally:
    conn.close()
    cur.close()


# 게시판 목록 불러오기
@router.post("/postUpload", response_model=Response_PostUpload_Model)
def upload(postUpload_data : PostUpload_Model):
  conn, cur = mysql_create_session()

  end = postUpload_data.page * postUpload_data.itemCount
  start = end - postUpload_data.itemCount

  try:
    sql = 'SELECT count(*) FROM Community'
    cur.execute(sql)
    total = cur.fetchone()['count(*)']
    
    sql = 'SELECT community_id,community_title,community_createat FROM Community ORDER BY community_id DESC limit %s, %s;'
    cur.execute(sql,(start, postUpload_data.itemCount))
    result = cur.fetchall()
    return Response_PostUpload_Model(status=200, message="게시판 목록 불러오기 성공",data=result)
  except Exception as e:
    conn.rollback()
    # 에러 발생시 예외 메세지 (detail)를 전달 
    raise HTTPException(status_code=401, detail=str(e))
  finally:
    cur.close()
    conn.close()  


# 게시판 세부정보 불러오기 API
@router.post("/postRead", response_model=Response_PostRead_Model)
def read(postRead_data : PostRead_Model):
  conn, cur = mysql_create_session()
  
  community_id = postRead_data.community_id
  print(community_id)

  
  # 조회수
  sql1 = 'SELECT community_search FROM Community WHERE community_id = %s'
  cur.execute(sql1, (community_id,))

  # 검색 후 조회수 1 증가
  community_search = cur.fetchone()['community_search'] + 1
  sql2 = 'UPDATE Community SET community_search = %s WHERE community_id = %s'
  cur.execute(sql2, (community_search, community_id,))
  conn.commit()
  
  sql = 'SELECT community_id,community_title,community_createat,user_id,community_search FROM Community WHERE community_id = %s;'
  cur.execute(sql,(community_id))
  data = cur.fetchall()
  
  cur.close()
  conn.close()
  return Response_PostRead_Model(status=201, message="게시물 가져오기 성공", data=data)

# 게시글 삭제 API
@router.delete("/postRemove", response_model=Response_PostRemove_Model)
def remove(postRemove_data: PostRemove_Model, access_token: str = Depends(oauth2_scheme)):
  # MySQL과 상호작용하기 위해 연결하는 cur 객체
  conn, cur = mysql_create_session()

  # 토큰 유효성 확인
  payload = access_expirecheck(access_token)

  # 유저 정보 - 이메일로 user_id 조회
  user_email = payload['email']
  access_user_id = findUserID(user_email)
  # print(access_user_id)

  # 삭제할 게시글 ID
  community_id = postRemove_data.community_id
  # print(community_id)

  try:
    # 게시글 작성자(user_id) 확인
    sql = 'SELECT user_id FROM Community WHERE community_id = %s'
    cur.execute(sql, (community_id,))
    result = cur.fetchone()
    # print(result)

    if not result:
      raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        
    # DB에서 가져온 user_id는 튜플이므로 [0]으로 값 추출
    original_user_id = result['user_id']
    # print(original_user_id)

    # 현재 로그인한 유저가 게시글 작성자인지 확인
    if access_user_id != original_user_id:
      raise HTTPException(status_code=403, detail="게시글을 삭제할 권한이 없습니다.")

    # 게시글 삭제
    sql = 'DELETE FROM Community WHERE community_id = %s;'
    cur.execute(sql, (community_id,))
    conn.commit()

  except Exception as e:
      conn.rollback()
      raise HTTPException(status_code=400, detail=f"DB 에러 발생: {str(e)}")
  finally:
    conn.close()
    cur.close()
      
  return Response_PostRemove_Model(status=201, message="게시물 삭제 완료")
