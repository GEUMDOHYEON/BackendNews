import os
import sys
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from database import mysql_create_session
from dotenv import load_dotenv
from schemas.news import *
from datetime import date
from tokens import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

router = APIRouter(
  prefix="/news",
  tags=["news"]
)

# 헤더에 토큰 값 가져오기 위한 객체
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 뉴스 목록 가져오는 API(keyword별 itemCount 만큼 조회)
@router.get("/getNewsList/{keyword}/{itemCount}", response_model=Response_NewsList)
def getNewsList(keyword: str, itemCount: int):
  conn,cur = mysql_create_session()
  try:
    if keyword == 'normal':
      # 키워드가 normal이면 키워드를 통합하여 뉴스를 조회
      sql = 'SELECT article_id, article_title, article_url, article_content, article_image FROM Article ORDER BY article_id DESC LIMIT %s'
      cur.execute(sql,(itemCount))
      result = cur.fetchall()
      return Response_NewsList(status=200, message="뉴스 조회 성공",data=result)
    else:
      # 입력한 키워드를 기준으로 뉴스 조회
      sql = 'SELECT a.article_id, a.article_title, a.article_url, a.article_content, a.article_image FROM Keywords k JOIN Article_Keyword ak ON k.keyword_id = ak.keyword_id JOIN Article a ON ak.article_id = a.article_id WHERE k.keyword = %s ORDER BY a.article_id DESC LIMIT %s'
      cur.execute(sql,(keyword,itemCount))
      result = cur.fetchall()
      return Response_NewsList(status=200, message="뉴스 조회 성공",data=result)
  except Exception as e:
    return Response_NewsList(status=404, message="뉴스 조회 실패",data=[])
  finally:
    cur.close()
    conn.close()

# 뉴스 세부정보 가져오는 API
@router.get("/getNews/{news_id}", response_model=Response_News)
def getNews(news_id:int):
  conn,cur = mysql_create_session()
  try:
    # article_views 검색
    article_id = news_id
    sql1 = 'SELECT article_views FROM Article WHERE article_id = %s'
    cur.execute(sql1, (article_id,))

    # 검색 후 조회수 1 증가
    article_views = cur.fetchone()['article_views'] + 1
    sql2 = 'UPDATE Article SET article_views = %s WHERE article_id = %s'
    cur.execute(sql2, (article_views, article_id,))
    conn.commit()

    # 뉴스 고유의 아이디를 기준으로 해당 뉴스 검색
    sql3 = 'SELECT * FROM Article WHERE article_id = %s'
    cur.execute(sql3, (article_id,))
    result = cur.fetchall()
    if not result:
      return Response_News(status=404, message="뉴스 조회 실패", data=[])
    return Response_News(status=200, message="뉴스 조회 성공", data=result)
  except Exception as e:
    return Response_News(status=404, message="뉴스 조회 실패", data=[])
  finally:
    cur.close()
    conn.close()

# 조회수 별 뉴스 조회 API
@router.get("/highestViews", response_model=Response_NewsTitle)
def highestViews():
  conn, cur = mysql_create_session()
  today = date.today()
  try:
    # 오늘 기준 조회수 높은 순으로 10개씩 조회
    count = 10
    sql = 'SELECT article_id, article_title FROM Article WHERE article_createat = %s ORDER BY article_views DESC, article_id DESC limit %s'
    cur.execute(sql, (today, count))
    result = cur.fetchall()
    if(len(result) == 10):
      return Response_NewsTitle(status=200, message="조회수 별 뉴스 조회 성공", data=result)
    else:
      return Response_NewsTitle(status=404, message="오늘의 뉴스가 존재하지 않습니다.",data=[])
  except Exception as e:
    return Response_NewsTitle(status=401, message="조회수 별 뉴스 조회 실패", data=[])
  finally:
    cur.close()
    conn.close()

# 뉴스 좋아요 API (토글처럼 좋아요, 좋아요 취소)
@router.post("/like", response_model=Response_Like_Scrap)
def likeNews(data: My_News, access_token: str = Depends(oauth2_scheme)):
  token = {"access_token": access_token, "refresh_token": data.refresh_token}
  # 뉴스 id
  article_id = data.article_id
  payload = expirecheck(token)

  # 회원 email
  email = payload.data
  conn, cur = mysql_create_session()
  try:
    # 유저 id 검색
    sql1 = 'SELECT user_id FROM Users WHERE user_email = %s'
    cur.execute(sql1,(email))
    user_id = cur.fetchone()['user_id']

    # User_Article 테이블에 해당 기사에 대한 회원이 좋아요 했는지 확인 (안했으면 좋아요 했으면 좋아요 취소)
    sql2 = 'SELECT * FROM User_Article WHERE article_id = %s AND user_id = %s'
    cur.execute(sql2, (article_id,user_id))
    article_result = cur.fetchone()
    
    # Article 테이블에서 좋아요 수 검색
    sql3 = 'SELECT article_like FROM Article WHERE article_id = %s'
    cur.execute(sql3,(article_id,))
    article_like = cur.fetchone()['article_like']
    # 스크랩과 좋아요가 같은 테이블에서 다루기 때문에 if문으로 검증
    if article_result == None:
      # 기사의 좋아요 수 1 증가
      article_like += 1
      sql4 = 'UPDATE Article SET article_like = %s WHERE article_id = %s'
      cur.execute(sql4,(article_like, article_id))
      conn.commit()
      # User_Article 테이블에 기사와 회원 id 추가 + 좋아요 1로 수정
      sql5 = 'INSERT INTO User_Article (article_id, user_id, user_article_like) VALUES (%s,%s,1)' 
      cur.execute(sql5,(article_id,user_id))
      conn.commit()
      # 결과값 전송
      return Response_Like_Scrap(status=201,message="좋아요 성공", data=article_like)
    else: # 스크랩이 존재하거나 좋아요 상태일때
      # 좋아요 상태이면 좋아요 취소하기
      if article_result['user_article_like'] == 1:
        # 기사의 좋아요 수 1 감소
          article_like -= 1
          sql6 = 'UPDATE Article SET article_like = %s WHERE article_id = %s'
          cur.execute(sql6,(article_like, article_id))
          conn.commit()

        # User_Article 테이블에 해당 행 수정
          sql7 = 'UPDATE User_Article SET user_article_like = 0 WHERE article_id = %s AND user_id = %s'
          cur.execute(sql7,(article_id,user_id))
          conn.commit()

        # 결과값 전송
          return Response_Like_Scrap(status=201,message="좋아요 취소 성공", data=article_like)
      else:
        # 기사의 좋아요 수 1 증가
        article_like += 1
        sql6 = 'UPDATE Article SET article_like = %s WHERE article_id = %s'
        cur.execute(sql6,(article_like, article_id))
        conn.commit()

        # User_Article 테이블에 해당 행 수정
        sql7 = 'UPDATE User_Article SET user_article_like = 1 WHERE article_id = %s AND user_id = %s'
        cur.execute(sql7,(article_id,user_id))
        conn.commit()
        return Response_Like_Scrap(status=201,message="좋아요 성공", data=article_like)
  except Exception as e:
    print(e)
    return Response_Like_Scrap(status=404,message="좋아요 실패", data=0)
  finally:
    cur.close()
    conn.close()

# 좋아요한 뉴스 보여주는 API
@router.get("/likeNewsLists")
def likeNewsLists(data: My_News_Lists, access_token: str = Depends(oauth2_scheme)):
  token = {"access_token": access_token, "refresh_token": data.refresh_token}

  payload = expirecheck(token)
  # 이메일
  email = payload.data
  conn, cur = mysql_create_session()
  try:
    # 유저 정보 검색
    sql1 = 'SELECT user_id FROM Users WHERE user_email = %s'
    cur.execute(sql1,(email,))
    user_id = cur.fetchone()['user_id']

    # 좋아요한 뉴스 검색
    sql2 = 'SELECT * FROM Article a JOIN User_Article ua ON ua.article_id = a.article_id WHERE ua.user_id = %s AND ua.user_article_like = 1'
    cur.execute(sql2, (user_id,))
    result = cur.fetchall()
    return Response_NewsList(status=200, message="뉴스 조회 성공",data=result)
  except Exception as e:
    print(e)
    return Response_NewsList(status=404, message="뉴스 조회 실패", data=[])
  finally:
    cur.close()
    conn.close()

# 뉴스 스크랩 API (토글처럼 스크랩, 스크랩 취소)
@router.post("/scrap", response_model=Response_Like_Scrap)
def scrapNews(data: My_News, access_token: str = Depends(oauth2_scheme)):
  token = {"access_token": access_token, "refresh_token": data.refresh_token}
  # 뉴스 id
  article_id = data.article_id
  payload = expirecheck(token)

  # 회원 email
  email = payload.data
  conn, cur = mysql_create_session()
  try:
    # 유저 id 검색
    sql1 = 'SELECT user_id FROM Users WHERE user_email = %s'
    cur.execute(sql1,(email))
    user_id = cur.fetchone()['user_id']

    # User_Article 테이블에 해당 기사에 대한 회원이 스크랩 했는지 확인 (안했으면 스크랩 했으면 스크랩 취소)
    sql2 = 'SELECT * FROM User_Article WHERE article_id = %s AND user_id = %s'
    cur.execute(sql2, (article_id,user_id))
    article_result = cur.fetchone()

    # Article 테이블에서 스크랩 수 검색
    sql3 = 'SELECT article_scrap FROM Article WHERE article_id = %s'
    cur.execute(sql3,(article_id,))
    article_scrap = cur.fetchone()['article_scrap']
    # 스크랩과 좋아요가 같은 테이블에서 다루기 때문에 if문으로 검증
    if article_result == None:
      # 기사의 스크랩 수 1 증가
      article_scrap += 1
      sql4 = 'UPDATE Article SET article_scrap = %s WHERE article_id = %s'
      cur.execute(sql4,(article_scrap, article_id))
      conn.commit()
      # User_Article 테이블에 기사와 회원 id 추가 + 스크랩 1로 수정
      sql5 = 'INSERT INTO User_Article (article_id, user_id, user_article_scrap) VALUES (%s,%s,1)' 
      cur.execute(sql5,(article_id,user_id))
      conn.commit()
      # 결과값 전송
      return Response_Like_Scrap(status=201,message="스크랩 성공", data=article_scrap)
    else: # 스크랩이 존재하거나 스크랩 상태일때
      # 스크랩 상태이면 스크랩 취소하기
      if article_result['user_article_scrap'] == 1:
        # 기사의 스크랩 수 1 감소
          article_scrap -= 1
          sql6 = 'UPDATE Article SET article_like = %s WHERE article_id = %s'
          cur.execute(sql6,(article_scrap, article_id))
          conn.commit()

        # User_Article 테이블에 해당 행 수정
          sql7 = 'UPDATE User_Article SET user_article_scrap = 0 WHERE article_id = %s AND user_id = %s'
          cur.execute(sql7,(article_id,user_id))
          conn.commit()

        # 결과값 전송
          return Response_Like_Scrap(status=201,message="스크랩 취소 성공", data=article_scrap)
      else:
        # 기사의 스크랩 수 1 증가
        article_scrap += 1
        sql6 = 'UPDATE Article SET article_scrap = %s WHERE article_id = %s'
        cur.execute(sql6,(article_scrap, article_id))
        conn.commit()

        # User_Article 테이블에 해당 행 수정
        sql7 = 'UPDATE User_Article SET user_article_scrap = 1 WHERE article_id = %s AND user_id = %s'
        cur.execute(sql7,(article_id,user_id))
        conn.commit()
        return Response_Like_Scrap(status=201,message="스크랩 성공", data=article_scrap)
  except Exception as e:
    print(e)
    return Response_Like_Scrap(status=404,message="스크랩 실패", data=0)
  finally:
    cur.close()
    conn.close()

# 스크랩한 뉴스 보여주는 API
@router.get("/scrapNewsLists")
def scrapNewsLists(data: My_News_Lists, access_token: str = Depends(oauth2_scheme)):
  token = {"access_token": access_token, "refresh_token": data.refresh_token}

  payload = expirecheck(token)
  # 이메일
  email = payload.data
  conn, cur = mysql_create_session()
  try:
    # 유저 정보 검색
    sql1 = 'SELECT user_id FROM Users WHERE user_email = %s'
    cur.execute(sql1,(email,))
    user_id = cur.fetchone()['user_id']

    # 스크랩한 뉴스 검색
    sql2 = 'SELECT * FROM Article a JOIN User_Article ua ON ua.article_id = a.article_id WHERE ua.user_id = %s AND ua.user_article_scrap = 1'
    cur.execute(sql2, (user_id,))
    result = cur.fetchall()
    return Response_NewsList(status=200, message="뉴스 조회 성공",data=result)
  except Exception as e:
    print(e)
    return Response_NewsList(status=404, message="뉴스 조회 실패", data=[])
  finally:
    cur.close()
    conn.close()