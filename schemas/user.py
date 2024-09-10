from pydantic import BaseModel

class Register_User(BaseModel):
  email:str
  user_name:str
  password:str
  user_number:str
  nickname:str
  user_age:int