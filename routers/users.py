from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, Request
import bcrypt
import jwt
from database import mysql_create_session
from tokens import *
from schemas.user import *
from schemas.token import *
from routers.news import findUserID

#jwt에 필요한 전역변수
SECRET_KEY = os.environ["SECRET_KEY"]
#jwt 알고리즘
ALGORITHM = os.environ["ALGORITHM"]
#access_token 만료(분)
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
# 헤더에 토큰 값 가져오기 위한 객체
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
  """
  이메일, 이름, 패스워드, 핸드폰번호, 닉네임, 나이를 입력받아 회원가입을 받습니다.
  """
  conn,cur = mysql_create_session()
  user_dict = user.model_dump()
  user_email,user_password,user_name,user_number,user_nickname,user_age = user_dict.values()


  try:
    # 이메일 중복 여부 확인
    sql1 = 'SELECT EXISTS(SELECT 1 FROM Users WHERE user_email="{}")'.format(user_email)
    cur.execute(sql1)
    dupli = cur.fetchone()
    exists = list(dupli.values())[0]
    if exists != 0:
      return Response_Register(status=418, message="아이디 중복")
    
    # 닉네임 중복 여부 확인
    sql2 = 'SELECT EXISTS(SELECT 1 FROM Users WHERE user_nickname="{}")'.format(user_nickname)
    cur.execute(sql2)
    dupli = cur.fetchone()
    exists = list(dupli.values())[0]
    if exists != 0:
      return Response_Register(status=419, message="닉네임 중복")
  except:
    conn.rollback()
    conn.close()
    cur.close()
    raise HTTPException(status_code=404,detail="회원가입 실패")

    

  #패스워드 해싱
  hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

  try:
    sql3 = 'INSERT INTO Users(user_email, user_name, user_password,user_number,user_nickname,user_age) VALUES (%s, %s, %s, %s, %s, %s)'
    cur.execute(sql3,(user_email,user_name,hashed_password,user_number,user_nickname,user_age))
    conn.commit()
    return Response_Register(status=201, message="회원가입 성공")
  except Exception as e:
    conn.rollback()
    raise HTTPException(status_code=404, detail="회원가입 실패")
  finally:
    conn.close()
    cur.close()



#로그인/자동로그인 API
@router.post("/login", response_model=Response_Login)
def login(user:Login_User, request: Request):
  """
  로그인시 정보를 확인해 토큰을 반환합니다.
  auto_token을 보낼 시 자동로그인 됩니다.
  auto_token을 보낸 경우에도 email,password(공백) 데이터를 전송해야 합니다.
  """

  # 자동로그인 확인
  auto_login = False

  # request 헤더에서 토큰 추출
  auth_header = request.headers.get("Authorization")
  # Beaer 토큰 추출 후 유저 검사
  if auth_header:
    token_type, auto_token = auth_header.split()  # Bearer 토큰 분리
    if auto_token:
      try:
        #auto_token 확인
        payload = jwt.decode(auto_token, SECRET_KEY, algorithms=[ALGORITHM])
        # 이메일
        user_email = payload.get('sub')
        # auto_login 활성화
        auto_login = True
        # 공백 패스워드
        password = ""
      except:
        raise HTTPException(status_code=401,detail="auto_token만료")
      
  else:
    user_dict = user.model_dump()
    user_email, password = user_dict.values()

  conn,cur = mysql_create_session()
  
  try:
    sql = 'SELECT * FROM Users WHERE user_email = %s'
    cur.execute(sql,(user_email))
    #쿼리 결과의 첫번째 행
    row = cur.fetchone()

    #결과가 없을 경우
    if not row:
      #아이디 없는 로그 띄우지 않음(보안정책)
      raise HTTPException(status_code=404, detail="로그인 실패")
    
    #비밀번호 해싱후 체크 or auto_login == True
    if auto_login or bcrypt.checkpw(password.encode('utf-8'), row['user_password'].encode('utf-8')):
      access_token = create_token(data={"sub":row['user_email'],"nick":row['user_nickname'],"type":"access_token"},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
      refresh_token = create_token(data={"sub":row["user_email"],"type":"refresh_token"},expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES)


      #리턴 값 data안에 닉네임, 이메일, 폰번호 전달
      return Response_Login(status=201, message="로그인 성공",data={"access_token":access_token,"refresh_token":refresh_token,"nickname":row['user_nickname'],"email":user_email,"number":row['user_number']})
    else:
      conn.rollback()
      raise HTTPException(status_code=404, detail="로그인 실패")
  finally:
    conn.close()
    cur.close()


# 리프레쉬 토큰 만료 확인 및 엑세스 토큰 재발급 API
@router.post("/reissue", response_model=Response_Reissue, response_model_exclude_unset=True)
def reissue(refresh:Refresh_Token):
  """
  리프레쉬 토큰 만료를 확인하고 엑세스 토큰을 재발급합니다.
  """

  try:
    #refresh_token 만료 확인
    payload = jwt.decode(refresh['refresh_token'], SECRET_KEY, algorithms=[ALGORITHM])
    user_email = payload.get('sub')

    try:
      conn, cur = mysql_create_session()
      sql = "SELECT * FROM Users WHERE user_email = %s"
      cur.execute(sql,(user_email))
      row = cur.fetchone()

      if not row:
        raise HTTPException(status_code=401,detail="id확인불가")
      
      # 새로운 access토큰 발급
      new_access_token = create_token(data={"sub":row['user_email'],"nick":row['user_nickname'],"type":"access_token"},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

      return Response_Reissue(status=200,message="엑세스토큰 발급",access_token=new_access_token)
    
    except:
      conn.rollback()
      raise HTTPException(status_code=401,detail="id확인불가")
    
    finally:
      conn.close()
      cur.close()

  except:
    raise HTTPException(status_code=401,detail="access_token만료")




# 개인정보 변경 API
@router.put("/changeinfo", response_model=Response_changeinfo)
def changeinfo(user:Change_User, access_token: str = Depends(oauth2_scheme)):
  """
  유저 정보를 변경합니다.
  닉네임 : 100
  전화번호 : 200
  비밀번호 : 300
  """

  # 사용자 검증
  payload = access_expirecheck(access_token)
  email = payload['email']
  user_id = findUserID(email)

  changedata = user.data
  status = user.status
  
  conn,cur = mysql_create_session()

  # 닉네임
  if status == 100:
    sql = 'UPDATE Users SET user_name = %s WHERE user_id=%s'
  # 전화번호
  elif status == 200:
    sql = 'UPDATE Users SET user_number = %s WHERE user_id=%s'
  # 비밀번호
  elif status == 300:
    hashed_password = bcrypt.hashpw(changedata.encode('utf-8'), bcrypt.gensalt())
    changedata = hashed_password
    sql = 'UPDATE Users SET user_name = %s WHERE user_id=%s'

  try:     
    cur.execute(sql,(changedata,user_id))
    conn.commit()
    
    return Response_changeinfo(status=200, message="개인정보 변경 성공")
  except:
    conn.rollback()
    raise HTTPException(status_code=404, detail="개인정보 변경 실패")
  finally:
    cur.close()
    conn.close()

  
# 자동로그인 토큰 발급 API
@router.post("/autologinToken", response_model=Response_autologinToken)
def autologinToken(access_token: str = Depends(oauth2_scheme)):
  """
  자동로그인 토큰을 발급합니다.
  """

  # 사용자 검증
  payload = access_expirecheck(access_token)
  email = payload['email']
  
  auto_token = create_token(data={"sub":email,"type":"auto_token"},expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES)

  return Response_autologinToken(status=201, message="auto_token 발급 성공",data=auto_token)


# 개인 키워드 추가 API
@router.post("/keywordAdd",response_model=Response_Keyword_Add)
def keywordAdd(data:Keyword_Add, access_token: str = Depends(oauth2_scheme)):
  """
  개인 키워드를 추가합니다.
  """

  # 사용자 검증
  payload = access_expirecheck(access_token)
  email = payload['email']
  user_id = findUserID(email)

  keyword = data.keyword

  conn, cur = mysql_create_session()
  try:
    # 키워드 있는지 확인
    sql1 = 'SELECT keyword_id FROM Keywords WHERE keyword=%s'
    cur.execute(sql1,(keyword))
    keyword_id = cur.fetchone()

    if keyword_id is None:
      # 키워드 추가
      sql2 = 'INSERT INTO Keywords (keyword) VALUES(%s)'
      cur.execute(sql2,(keyword))
      keyword_id = cur.lastrowid
    else:
      keyword_id = keyword_id['keyword_id']

    # 유저가 키워드 연결
    sql3 = 'INSERT INTO User_keyword (keyword_id, user_id) VALUES(%s,%s)'
    cur.execute(sql3,(keyword_id,user_id))
    
    conn.commit()
    return Response_Keyword_Add(status=201, message="키워드 추가 성공")
  except:
    conn.rollback()
    raise HTTPException(status_code=403, detail="키워드 추가 실패")
  finally:
    cur.close()
    conn.close()


# 개인 키워드 조회 API
@router.get("/keyword",response_model=Response_Keyword)
def keywordAdd(access_token: str = Depends(oauth2_scheme)):
  """
  개인 키워드를 조회합니다.
  """

  # 사용자 검증
  payload = access_expirecheck(access_token)
  email = payload['email']
  user_id = findUserID(email)

  conn, cur = mysql_create_session()
  try:
    sql1 = 'SELECT keyword_id FROM User_keyword WHERE user_id=%s'
    cur.execute(sql1,(user_id,))
    result = cur.fetchall()
    
    keyword_ids = [row['keyword_id'] for row in result]

    # keyword_id가 존재할 경우
    if keyword_ids:  
        sql2 = 'SELECT keyword FROM Keywords WHERE keyword_id IN %s'
        cur.execute(sql2, (tuple(keyword_ids),))
        keyword = cur.fetchall()
        keyword_results = [row['keyword'] for row in keyword]
    else:
        # 없으면 공백
        keyword_results = []
    
    conn.commit()
    
    return Response_Keyword(status=200,message="키워드 조회 성공",data=keyword_results)


  except:
    conn.rollback()
    raise HTTPException(status_code=404, detail="키워드 조회 실패")
  finally:
    cur.close()
    conn.close()


# 개인 키워드 삭제 API
@router.delete("/keywordDelete",response_model=Response_Keyword_Delete)
def keywordDelete(data:Keyword_Delete, access_token: str = Depends(oauth2_scheme)):
  """
  개인 키워드를 삭제합니다.
  """

  # 사용자 검증
  payload = access_expirecheck(access_token)
  email = payload['email']
  user_id = findUserID(email)

  keyword = data.keyword

  conn, cur = mysql_create_session()
  try:
    # 키워드 조회
    sql1 = 'SELECT keyword_id FROM Keywords WHERE keyword=%s'
    cur.execute(sql1,(keyword))
    keyword_id = cur.fetchone()['keyword_id']

    # 유저-키워드 삭제
    sql2 = 'DELETE FROM User_keyword WHERE keyword_id=%s and user_id=%s'
    cur.execute(sql2,(keyword_id,user_id))
    
    conn.commit()
    return Response_Keyword_Delete(status=200, message="키워드 삭제 성공")
  except:
    conn.rollback()
    raise HTTPException(status_code=403, detail="키워드 삭제 실패")
  finally:
    cur.close()
    conn.close()


# 아이디 찾기 API
@router.post("/findID",response_model=Response_findID)
def keywordDelete(data:Find_ID):
  """
  아이디를 찾습니다.
  """

  name = data.user_name
  number = data.user_number

  conn, cur = mysql_create_session()
  try:
    sql = 'SELECT user_email FROM Users WHERE user_name=%s and user_number=%s'
    cur.execute(sql,(name,number))
    user_email = cur.fetchone()['user_email']

    conn.commit()
    return Response_findID(status=201, message="아이디 찾기 완료", email=user_email)
  
  except:
    conn.rollback()
    raise HTTPException(status_code=403, detail="아이디 찾기 실패")
  finally:
    cur.close()
    conn.close()


# 비밀번호 재설정 API
@router.post("/resetPassword",response_model=Response_resetPassword)
def keywordDelete(data:Reset_Password):
  """
  비밀번호를 재설정합니다.
  """

  email = data.user_email
  name = data.user_name
  number = data.user_number
  new_password = data.new_password

  conn, cur = mysql_create_session()
  try:
    # 대상이 있는지 확인
    sql1 = 'SELECT user_id FROM Users WHERE user_email=%s and user_name = %s and user_number=%s'
    cur.execute(sql1,(email,name,number))
    result = cur.fetchone()

    conn.commit()

    # 일치하지 않을 시
    if result is None:
      return Response_resetPassword(status=418,message="대상 정보가 없습니다")
    
    user_id = list(result.values())[0]

    #패스워드 해싱
    new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    sql2 = "UPDATE Users SET user_password = %s WHERE user_id = %s"
    cur.execute(sql2,(new_hashed_password,user_id))
    conn.commit()

    return Response_findID(status=201, message="비밀번호 변경 완료")
  
  except:
    conn.rollback()
    raise HTTPException(status_code=403, detail="비밀번호 변경 실패")
  finally:
    cur.close()
    conn.close()