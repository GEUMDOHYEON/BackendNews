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

# 유저 개인정보 수정 DTO
class Change_User(BaseModel):
  status:int
  data:str

# keyword 추가 DTO
class Keyword_Add(BaseModel):
  keyword:str

# keyword 삭제 DTO
class Keyword_Delete(BaseModel):
  keyword:str

#회원가입 반환 DTO
class Response_Register(BaseModel):
  status:int
  message:str


#로그인 반환 DTO
class Response_Login(BaseModel):
  status:int
  message:str
  data:dict

#개인정보 변경 반환 DTO
class Response_changeinfo(BaseModel):
  status:int
  message:str

#자동로그인 토큰 반환 DTO
class Response_autologinToken(BaseModel):
  status:int
  message:str
  data:str

#Keyword 추가 반환 DTO
class Response_Keyword_Add(BaseModel):
  status:int
  message:str

#Keyword 반환 DTO
class Response_Keyword(BaseModel):
  status:int
  message:str
  data:list


#Keyword 삭제 반환 DTO
class Response_Keyword_Delete(BaseModel):
  status:int
  message:str