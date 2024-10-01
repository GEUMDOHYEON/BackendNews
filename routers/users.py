from fastapi import APIRouter
import os
from dotenv import load_dotenv
from fastapi import HTTPException
import bcrypt
import jwt
from database import mysql_create_session
from tokens import create_token
from schemas.user import *
from schemas.token import *

#jwt에 필요한 전역변수
SECRET_KEY = os.environ["SECRET_KEY"]
#jwt 알고리즘
ALGORITHM = os.environ["ALGORITHM"]
#access_token 만료(분)
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]


router = APIRouter()

# /user에 접속후 api
router = APIRouter(	
    prefix="/users",
    tags=["users"]
)

# 환경변수 이용을 위한 전역변수
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
# 루트 경로에 .env파일로 값 설정
load_dotenv(os.path.join(BASE_DIR, ".env"))


#access_token 만료(분)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
#refresh_token 만료(분)
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"])

@router.get("/")
def tmp_user():
  return "HELLO WORLD"


#회원가입 API
#response_model_exclude_unset=True : 디폴트값은 제외
@router.post("/register", response_model=Response_Register, response_model_exclude_unset=True)
def register(user:Register_User):
  conn,cur = mysql_create_session()
  user_dict = user.model_dump()
  user_email,user_password,user_name,user_number,user_nickname,user_age = user_dict.values()

  #패스워드 해싱
  hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

  try:
    sql = 'INSERT INTO Users(user_email, user_name, user_password,user_number,user_nickname,user_age) VALUES (%s, %s, %s, %s, %s, %s)'
    cur.execute(sql,(user_email,user_name,hashed_password,user_number,user_nickname,user_age))
    conn.commit()
    return Response_Register(status=201, message="회원가입 성공")
  except Exception as e:
    conn.rollback()
    return Response_Register(status=400, message="회원가입 실패")
  finally:
    conn.close()
    cur.close()



#로그인 API
@router.post("/login", response_model=Response_Login)
def login(user:Login_User):
  """
  로그인시 정보를 확인해 토큰을 반환합니다.
  """
  conn,cur = mysql_create_session()
  user_dict = user.model_dump()
  user_id, password = user_dict.values()

  try:
    sql = 'SELECT * FROM Users WHERE user_email = %s'
    cur.execute(sql,(user_id))
    #쿼리 결과의 첫번째 행
    row = cur.fetchone()

    #결과가 없을 경우
    if not row:
      #아이디 없는 로그 띄우지 않음(보안정책)
      return Response_Login(status=400, message="로그인 실패", data={})
    
    #비밀번호 해싱후 체크
    if bcrypt.checkpw(password.encode('utf-8'), row['user_password'].encode('utf-8')):
      access_token = create_token(data={"sub":row['user_email'],"nick":row['user_nickname'],"type":"access_token"},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
      refresh_token = create_token(data={"sub":row["user_email"],"type":"refresh_token"},expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES)


      #리턴 값 data안에 일단 닉네임 넣음
      return Response_Login(status=201, message="로그인 성공",data={"access_token":access_token,"refresh_token":refresh_token,"nickname":row['user_nickname']})
    else:
      return Response_Login(status=400,message="로그인 실패",data={})
  finally:
    conn.close()
    cur.close()


# 리프레쉬 토큰 만료 확인 및 엑세스 토큰 재발급 API
@router.get("/reissue", response_model=Response_Reissue, response_model_exclude_unset=True)
def login(refresh:Refresh_Token):
  """
  리프레쉬 토큰 만료를 확인하고 엑세스 토큰을 재발급합니다
  """

  try:
    #refresh_token 만료 확인
    payload = jwt.decode(refresh['refresh_token'], SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get('sub')

    try:
      conn, cur = mysql_create_session()
      sql = "SELECT * FROM Users WHERE user_email = %s"
      cur.execute(sql,(user_id))
      row = cur.fetchone()

      if not row:
        raise HTTPException(status_code=401,detail="id확인불가")
      
      # 새로운 access토큰 발급
      new_access_token = create_token(data={"sub":row['user_email'],"nick":row['user_nickname'],"type":"access_token"},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

      return Response_Reissue(status=200,message="엑세스토큰 발급",access_token=new_access_token)
    
    except:
      raise HTTPException(status_code=401,detail="id확인불가")
    
    finally:
      conn.close()
      cur.close()

  except:
    raise HTTPException(status_code=401,detail="access_token만료")




# 개인정보 변경 API
@router.post("/changeinfo", response_model=Response_Login)
def changeinfo(user:Change_User):
  """
  유저 정보를 변경합니다.
  닉네임 : 100
  전화번호 : 200
  비밀번호 : 300
  """
  conn,cur = mysql_create_session()
  user_dict = user.model_dump()
  status, data = user_dict.values()
  
  # 변경중...


