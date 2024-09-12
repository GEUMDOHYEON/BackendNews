from fastapi import APIRouter, Response
from database import mysql_create_session
from schemas.board import PostUpload_Model
from datetime import datetime

router = APIRouter(
  prefix="/board",
  tags=["board"]
)

# 게시판 글 작성
@router.post("/postUpload")
async def upload(response:Response, postUpload_data : PostUpload_Model):
  # mysql 과 상호작용하기 위해 연결해주는 cur 객체
  conn, cur = mysql_create_session()
  
  # 토큰 디코딩
  
  # 유저 정보 - 토큰 디코딩 후 - 아이디, 닉네임 가져오기
  # nickname = 
  
  # 게시판 정보 - 제목, 내용, 작성 시간
  title = postUpload_data.community_title
  content = postUpload_data.community_content
  
  now = datetime.now()
  createat = now.strftime("%Y-%m-%d")
  
  
  
  return {"업로드 성공"}

# 게시판 글 삭제
@router.post("/postRemove")
async def remove():
  return {"삭제 성공"}


# 게시판 글 수정
@router.post("/post")
async def update():
  return {"수정 성공"}