from pydantic import BaseModel

class PostWrite_Model (BaseModel):
    community_title : str
    community_content : str
    
class PostUpload_Model (BaseModel):
    page: int
    itemCount: int

class PostEdit_Model (BaseModel):
    community_title : str
    community_content : str
    community_id : str

class PostRead_Model (BaseModel):
    community_id : str

class PostRemove_Model (BaseModel):
    community_id : str

class CommentWrite_Model (BaseModel):
    community_id : str
    comment_content : str
    
class CommentRead_Model (BaseModel):
    community_id : str

class CommentEdit_Model (BaseModel):
    comment_content : str
    community_id : str
    comment_id : str
    
class CommentRemove_Model (BaseModel):
    comment_id : str

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
    data : dict
    
class Response_PostRemove_Model (BaseModel):
    status : int
    message : str

class Response_CommentWrite_Model (BaseModel):
    status : int
    message : str
    
class Response_CommentEdit_Model (BaseModel):
    status : int
    message : str
    
class Response_CommentRemove_Model (BaseModel):
    status : int
    message : str
    
class Response_CommentRead_Model (BaseModel):
    status : int
    message : str
    data : list