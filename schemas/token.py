from pydantic import BaseModel

# access_토큰 DTO
class Access_Token(BaseModel):
    access_token:str

# refresh_토큰 DTO
class Refresh_Token(BaseModel):
    refresh_token:str

# access_토큰 재발급 DTO
class Response_Reissue(BaseModel):
    status:int
    message:str
    access_token:str

