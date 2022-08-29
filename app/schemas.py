from datetime import datetime
import email
from typing import Optional
from pydantic import BaseModel, EmailStr 
from pydantic.types import conint 
 
class PostBase(BaseModel): 
    title: str
    content: str 
    published: bool  = True 
    
#User to Backend 
class PostCreate(PostBase): 
    pass #inhairte from postcreate 

class UserOut(BaseModel): #response model for not retriving password 
    id: int 
    email: EmailStr
    created_at: datetime 
    
    class Config:   
        orm_mode = True
        
#Backend to user (Response) 
class Post(PostBase): 
    id: int 
    created_at: datetime 
    owner_id: int
    owner: UserOut #returning Pydentic model 
    
    class Config:   #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model
        orm_mode = True
        
class PostOut(PostBase):
    votes: int 
    post: Post 

    class Config:   #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model
        orm_mode = True
        
class UserCreate(BaseModel): 
    email: EmailStr 
    password: str 
        
class UserLogin(BaseModel):  
    email: EmailStr 
    password: str 

class Token(BaseModel):  
    access_token: str 
    token_type: str 
    
class TokenData(BaseModel):  
    id: Optional[str] = None 
    
class Vote(BaseModel): 
    post_id: int 
    dir: conint(le=1) #less then 1/// for like unlike 