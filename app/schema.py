from pydantic import BaseModel,Field
from typing import Optional


class task(BaseModel):

    id: str = Field(..., alias='_id')
    task: str
    description: str
    date_and_time: str
    completed: bool
    authorized_id: list
    owner_id:str

class taskIn(BaseModel):
    
    task: str
    description: str
    date_and_time: str
    completed: bool
    user_id: list
    
class task_update(BaseModel):
    
    task: str
    description: str
    date_and_time: str
    completed: bool    

class userIn(BaseModel):
    
    name: str
    email:str
    password: str

class userOut(BaseModel):
    
    id: str = Field(..., alias='_id')
    name: str
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class token(BaseModel):
    
    id: Optional[str] = None