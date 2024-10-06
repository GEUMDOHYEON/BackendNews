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
    
class PostLoad_Model (BaseModel) :
    is