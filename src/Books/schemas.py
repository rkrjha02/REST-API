from datetime import datetime
from pydantic import BaseModel
import uuid

class bookStructure(BaseModel):
    uid:uuid.UUID
    author:str
    title: str
    publisher:str
    published_date:str
    page_count:int
    genre:str
    language:str
    createdAt:datetime
    updatedAt:datetime

class createBookModel(BaseModel):
    author: str
    title: str
    publisher: str
    published_date: str
    page_count: int
    genre: str
    language: str

class bookUpdateModel(BaseModel):
    author:str
    title:str
    publisher:str
    page_count:int
    genre:str
    language:str