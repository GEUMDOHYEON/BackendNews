from pydantic import BaseModel

#회원가입 DTO
class Register_User(BaseModel):
  user_email:str
  user_password:str
  user_name:str
  user_number:str
  user_nickname:str
  user_age:int


#로그인 DTO
class Login_User(BaseModel):
  email:str
  password:str

# 유저 개인정보 수정
class Change_User(BaseModel):
  status:int
  data:str

#회원가입 반환 DTO
class Response_Register(BaseModel):
  status:int
  message:str


#로그인 반환 DTO
class Response_Login(BaseModel):
  status:int
  message:str
  data:dict