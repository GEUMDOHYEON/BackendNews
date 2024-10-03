from pydantic import BaseModel
from datetime import datetime
from typing import List

class News_card(BaseModel):
  article_id:int
  article_title:str
  article_url:str
  article_content:str
  article_image:str

class News_title(BaseModel):
  article_id:int
  article_title:str


class Response_NewsList(BaseModel):
  status:int
  message:str
  data: List[News_card]

class Response_News(BaseModel):
  status:int
  message:str
  data: dict

class Response_NewsTitle(BaseModel):
  status:int
  message:str
  data: List[News_title]

class My_News(BaseModel):
  article_id:int

class Response_Like_Scrap(BaseModel):
  status:int
  message:str
  data: int

class Create_Comment(BaseModel):
  article_id:int
  comment_content:str

class Response_Comment(BaseModel):
  status:int
  message:str

class Chagnge_Comment(BaseModel):
  comment_id: int
  comment_content:str

class Delete_Comment(BaseModel):
  comment_id: int