from datetime import datetime, timezone, timedelta
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

# 토큰 만료 확인 및 재갱신 함수
def expirecheck(data:Tokens):
    try:
        #access_token 만료 확인
        payload = jwt.decode(data['access_token'], SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        return Response_Tokens(status=201, message="이상없음", data=email)
    
    except:
        try:
            #refresh_token 만료 확인
            jwt.decode(data['refresh_token'], SECRET_KEY, algorithms=[ALGORITHM])

            new_access_token = access_token_reissue(data['refresh_token'])

            # 재발급중 오류생기면
            if new_access_token['status']==401:
                return Response_Tokens(status=400, message="발급오류", data='')
            
            access_token = new_access_token['data']

            # data를 json말고 str로 보내도 되는지
            return Response_Tokens(status=100, message="access_token재발급", data=access_token)
        
        except:
            return Response_Tokens(status=401, message="모든 토큰 만료", data='')


#access_token 재발급 함수
def access_token_reissue(refresh_token):
    # 토큰 디코딩
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get('sub')

    conn, cur = mysql_create_session()

    try:
        sql = "SELECT * FROM users WHERE user_email = %s"
        cur.execute(sql,(user_id))
        row = cur.fetchone()

        if not row:
            return Response_Tokens(status=401, message="id확인안됨", data='')
        
        # 새로운 access토큰 발급
        new_access_token = create_token(data={"sub":row['user_email'],"nick":row['user_nickname'],"type":"access_token"},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

        return Response_Access_Token(status=200, message="access토큰 재발급", data=new_access_token)
    except:
        return Response_Access_Token(status=401, message="aceess토큰 오류", data='')

    finally:
        conn.close()
        cur.close()
        