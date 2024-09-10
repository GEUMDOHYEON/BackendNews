import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def mysql_create_session():
  mysql_ip = os.environ['MYSQL_IP']
  mysql_port = int(os.environ['MYSQL_PORT'])
  mysql_user = os.environ['MYSQL_USER']
  mysql_pw = os.environ['MYSQL_PW']
  mysql_db = os.environ['MYSQL_DB']
  # MYSQL에 생성한 DB와 연결
  conn = pymysql.connect(host=mysql_ip,port=mysql_port, user=mysql_user, password=mysql_pw ,db=mysql_db, charset='utf8', cursorclass=pymysql.cursors.DictCursor)

  #cursor: 하나의 DB connection에 대하여 독립적으로 SQL 문을 실행할 수 있는 작업환경을 제공하는 객체
  cur = conn.cursor()

  return conn,cur
