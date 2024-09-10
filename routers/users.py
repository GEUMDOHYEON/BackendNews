from fastapi import APIRouter
from database import mysql_create_session
from schemas.user import Register_User 

router = APIRouter(	
    prefix="/users",
    tags=["users"]
)

router = APIRouter()

@router.get("/")
def tmp_user():
  return "HELLO WORLD"

@router.post("/register")
def register(user:Register_User):
  conn,cur = mysql_create_session()
  user_dict = user.model_dump()
  email,user_name,password,user_number,nickname,user_age = user_dict.values()

  try:
    sql = 'INSERT INTO users(email, user_name, password,user_number,nickname,user_age) VALUES (%s, %s, %s, %s, %s, %s)'
    cur.execute(sql,(email,user_name,password,user_number,nickname,user_age))
    conn.commit()
    return "성공"
  finally:
    conn.close()
    cur.close()
