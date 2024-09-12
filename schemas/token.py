from pydantic import BaseModel

# 토큰들 DTO
class Tokens(BaseModel):
    access_token:str
    refresh_token:str


# 토큰반환 DTO
class Response_Tokens(BaseModel):
    status:int
    message:str
    data:str


# access토큰반환 DTO
class Response_Access_Token(BaseModel):
    status:int
    message:str
    data:str