from pydantic import BaseModel
from datetime import datetime
from typing import List

class News_card(BaseModel):
  article_id:int
  article_title:str
  article_url:str
  article_content:str
  article_image:str

class News_contents(BaseModel):
  article_id:int
  article_title:str
  article_content:str
  article_url:str
  article_views:int
  article_createat:datetime
  article_like:int
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
  data: List[News_contents]

class Response_NewsTitle(BaseModel):
  status:int
  message:str
  data: List[News_title]

class My_News(BaseModel):
  access_token:str
  refresh_token:str
  article_id:int

class Response_Like_Scrap(BaseModel):
  status:int
  message:str
  data: int

class My_News_Lists(BaseModel):
  access_token:str
  refresh_token:str
