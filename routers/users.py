from fastapi import APIRouter

router = APIRouter(	
    prefix="/users",
    tags=["users"]
)

@router.get("/info")
def tmp_user():
  return "HELLO WORLD"