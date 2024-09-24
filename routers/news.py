import os
import sys
from fastapi import APIRouter
from database import mysql_create_session
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

router = APIRouter(
  prefix="/news",
  tags=["news"]
)

@router.get("/")
def tmp_new():
  return "HELLO WORLD!"

