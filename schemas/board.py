from pydantic import BaseModel

class postWrite_Model (BaseModel):
    community_id : str
    community_title : str
    community_content : str
    community_createat : str
    access_token : str
    new_write : bool
    
class PostDelete_Model (BaseModel):
    community_id : str
    community_title : str
    community_content : str
    community_createat : str
    access_token : str
    
class PostUpload_Model (BaseModel) :
    community_id : str