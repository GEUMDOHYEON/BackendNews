from pydantic import BaseModel

class PostUpload_Model (BaseModel):
    community_title : str
    community_content : str
    community_createat : str