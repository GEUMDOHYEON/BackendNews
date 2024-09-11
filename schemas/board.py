from pydantic import BaseModel

class PostUpload_Model (BaseModel):
    community_id : str
    user_id : str
    community_title : str
    community_content : str
    community_create : str