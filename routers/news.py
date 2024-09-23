import os
import sys
from fastapi import APIRouter
from database import mysql_create_session
from dotenv import load_dotenv
from schemas.news import *
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

router = APIRouter(
  prefix="/news",
  tags=["news"]
)

# 뉴스 썸네일 가져오는 API(keyword별 itemCount 만큼 조회)
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
    sql = 'SELECT article_id, article_title FROM Article WHERE article_createat = %s ORDER BY article_views DESC, article_id DESC limit 10'
    cur.execute(sql, (today))
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

# 뉴스 좋아요 API
@router.post("/like")
def likeNews():
  conn, cur = mysql_create_session()
  