import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

test_user = {
    "user_email": "test@naver.com",
    "user_password": "1234",
    "user_name": "테스트",
    "user_number": "010-1234-1234",
    "user_nickname": "test",
    "user_age": 1
}

def test():
  response = client.get("/")
  print(response)
  assert response.status_code == 200

# 회원가입 테스트
def test_register():
    response = client.post("/users/register", json={
        "user_email": test_user["user_email"],
        "user_password": test_user["user_password"],
        "user_name": test_user['user_name'],
        "user_number": test_user['user_number'],
        "user_nickname": test_user['user_nickname'],
        "user_age": test_user['user_age']
    })
    print(response.json())  # 유효성 검사 오류 확인
    assert response.status_code == 200

# # 로그인 테스트
# def test_login():
#     response = client.post("/users/login", json={"user_email": test_user["user_email"], "user_password": test_user["user_password"]})
#     assert response.status_code == 201
#     assert response.json()["message"] == "로그인 성공"
#     assert "access_token" in response.json()["data"]
#     assert "refresh_token" in response.json()["data"]
