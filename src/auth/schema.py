from pydantic import BaseModel,Field
import uuid
from datetime import datetime

class userCreateModel(BaseModel):
    first_name:str=Field(max_length=20)
    last_name:str=Field(max_length=20)
    username:str=Field(max_length=10)
    email:str=Field(max_length=50)
    password:str=Field(min_length=6, max_length=40)

class userModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    password: str = Field(exclude=True)
    first_name: str
    last_name: str
    is_verified: bool
    createdDate: datetime
    updatedDate: datetime

class userLoginModel(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=40)