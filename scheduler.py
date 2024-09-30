import os
import sys
import urllib.request
import json
import pymysql
import requests
import ssl
from bs4 import BeautifulSoup
from fastapi import APIRouter
from database import mysql_create_session
from dotenv import load_dotenv
from datetime import datetime
# 스포츠 뉴스를 위한 웹크롤링 모듈
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 네이버 뉴스 api 이용하기 위해서 ssl 무시
ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 네이버 뉴스 api 키
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

#크롬 드라이버 위치
EXCUTABLE_PATH = os.environ['EXCUTABLE_PATH']

# 크롬 옵션 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

# linux 환경에서 필요한 option
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 뉴스 키워드 
KEYWORDS = ["정치", "과학", "스포츠", "사회", "시사", "경제", "생활"]

def get_news_from_api():
  conn,cur = mysql_create_session()
  try:
    for keyword in KEYWORDS:
        encText = urllib.parse.quote(keyword)
        # 네이버 뉴스 api 이용
        url = "https://openapi.naver.com/v1/search/news?query=" + encText 
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",CLIENT_ID)
        request.add_header("X-Naver-Client-Secret",CLIENT_SECRET)

        try:
            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if rescode == 200:
                response_body = response.read()
                response_dict = json.loads(response_body.decode('utf-8'))
                items = response_dict['items']
                print(keyword)
                # 네이버 뉴스API를 통해 가져온 결과값(링크, 제목, 생성일)
                for item in items:
                    print(item['title'])
                    if 'naver.com' in item['link']:
                        try:
                            # 날짜 문자열을 파싱하고 MySQL 형식으로 변환
                            pub_date = datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
                            mysql_date = pub_date.strftime('%Y-%m-%d %H:%M:%S')

                            sql1 = 'INSERT INTO Article (article_title, article_url, article_createat) VALUES (%s,%s,%s)'
                            cur.execute(sql1, (item['title'], item['link'], mysql_date))

                            new_article_id = cur.lastrowid

                            cur.execute('SELECT keyword_id FROM Keywords WHERE keyword = %s', (keyword,))
                            keyword_id = cur.fetchone()['keyword_id']

                            sql2 = 'INSERT INTO Article_Keyword (keyword_id, article_id) VALUES (%s, %s)'
                            cur.execute(sql2, (keyword_id, new_article_id))

                            conn.commit()
                            
                            # 기사 본문을 크롤링하기 위함(스포츠와 연예 뉴스는 동적 페이지라 셀리니움 크롤링 이용)
                            if 'sports.naver' in item['link'] or 'entertain.naver' in item['link']:
                                article_content, article_image = crawl_dynamic_article(item['link'])
                            else:
                                article_content, article_image = crawl_article(item['link'])
                            sql3 = 'UPDATE Article SET article_content = %s, article_image = %s WHERE article_id = %s'
                            cur.execute(sql3, (article_content, article_image, new_article_id))

                            conn.commit()

                        except pymysql.Error as e:
                            print(f"sql 에러: {e}")
                            conn.rollback()
                        except ValueError as e:
                            print(f"날짜 파싱 에러: {e}")
                            conn.rollback()

                        else:
                            conn.commit()

                
            else:
                return {"error": f"API 에러: {rescode}"}

        except Exception as e:
            return {"error": f"에러 발생: {str(e)}"}

  finally:
    cur.close()
    conn.close()

# 일반 뉴스 기사 크롤링
def crawl_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 본문
        content = soup.select_one('article.go_trans._article_content')
        # 뉴스 사진
        try:
            image = soup.select_one('meta[property="og:image"]')['content'] if soup.select_one('meta[property="og:image"]') else None
        except:
            # 뉴스 이미지가 없으면 NULL
            image = None
        return content.text.strip(), image
    except Exception as e:
        print(f"크롤링 에러 : {e}")

# 동적 페이지 크롤링
def crawl_dynamic_article(url):
    # excutable_path는 chromdriver가 위치한 경로를 적어주면 된다.
    driver = webdriver.Chrome(excutable_path =EXCUTABLE_PATH,chrome_options=chrome_options)

    driver.get(url)

    try:
        # WebDriverWait를 사용하여 특정 요소가 나타날 때까지 최대 10초 동안 기다림
        # 뉴스 본문
        content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_article_content'))
        )
        # 뉴스 이미지
        try:
            image = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '._article_content img'))
            )
            image_url = image.get_attribute('src')
        except:
            # 뉴스에 이미지가 없으면 NULL
            image_url = None

        return content.text, image_url

    finally:
        driver.quit()

