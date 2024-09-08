from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def tmp_user():
  return "HELLO WORLD"