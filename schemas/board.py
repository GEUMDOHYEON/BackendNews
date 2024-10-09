from pydantic import BaseModel

class PostWrite_Model (BaseModel):
    community_title : str
    community_content : str

class PostEdit_Model (BaseModel):
    community_title : str
    community_content : str
    community_id : str

class PostRead_Model (BaseModel):
    community_id : str

class PostRemove_Model (BaseModel):
    community_id : str

class CommentWrite_Model (BaseModel):
    comment_id : str
    comment_content : str
    comment_create : str
    access_token : str
    
class CommentUpload_Model (BaseModel):
    comment_id : str
    access_token : str

class Response_PostWrite_Model (BaseModel):
    status : int
    message : str
    
class Response_PostEdit_Model (BaseModel):
    status : int
    message : str
    
class Response_PostUpload_Model (BaseModel):
    status : int
    message : str
    data : list
    
class Response_PostRead_Model (BaseModel):
    status : int
    message : str
    data : list
    
class Response_PostRemove_Model (BaseModel):
    status : int
    message : str