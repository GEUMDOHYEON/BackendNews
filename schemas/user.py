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

# ID 찾기 DTO
class Find_ID(BaseModel):
  user_name:str
  user_number:str

# 비밀번호 재설정 DTO
class Reset_Password(BaseModel):
  user_email:str
  user_name:str
  user_number:str
  new_password:str

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

# 아이디 찾기 반환 DTO
class Response_findID(BaseModel):
  status:int
  message:str
  email:str

# 비밀번호 재설정 반환 DTO
class Response_resetPassword(BaseModel):
  status:int
  message:str

# 이미지 조회 반환 DTO
class Response_profileImage(BaseModel):
  status:int
  message:str
  data:str

# 이미지 수정 반환 DTO
class Response_profileImageChange(BaseModel):
  status:int
  message:str


# 회원탈퇴 DTO
class Response_Secession(BaseModel):
  status:int
  message:str