from pydantic import BaseModel

class postWrite_Model (BaseModel):
    community_id : str
    community_title : str
    community_content : str
    community_createat : str
    access_token : str
    isNewWrite : bool
    
class PostDelete_Model (BaseModel):
    community_id : str
    community_title : str
    community_content : str
    community_createat : str
    access_token : str

class CommentWrite_Model (BaseModel):
    comment_id : str
    comment_content : str
    comment_create : str
    access_token : str
    
class CommentUpload_Modal (BaseModel):
    comment_id : str
    access_token : str