from fastapi import APIRouter
from database import mysql_create_session

router = APIRouter(
  prefix="/board",
  tags=["board"]
)

@router.get("/")
def tmp_board():
  return "HELLO WORLD"
