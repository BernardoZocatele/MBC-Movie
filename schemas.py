from pydantic import BaseModel

class filmModel(BaseModel):
    user_id: int
    movie: str
    gender: str
    release: str
    
class userModel(BaseModel):
    user_id:int
    username: str
    password: str