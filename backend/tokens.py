from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
import jwt
import os
from schemas.token import *
from database import mysql_create_session

#jwt에 필요한 전역변수
SECRET_KEY = os.environ["SECRET_KEY"]
#jwt 알고리즘
ALGORITHM = os.environ["ALGORITHM"]
#access_token 만료(분)
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]



# 토큰생성 함수
def create_token(data:dict, expires_delta: int | None = None):
    #전달된 data 복사본
    to_encode = data.copy()
    #만료시간 제공되면 현재시간에 더함
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        #현재시간에 15분 더함
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    # to_encode에 만료시간과 발행시간 추가
    to_encode.update({"exp":expire,"iat": datetime.now(timezone.utc)})
    #jwt 인코딩하여 생성
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

# 엑세스 토큰 만료 확인
def access_expirecheck(data:Access_Token):
    try:
        #access_token 만료 확인
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        nickname = payload.get('nick')
        return {"email":email,"nickname":nickname}
    except:
        raise HTTPException(status_code=401,detail="access_token만료")