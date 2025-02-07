from datetime import datetime,date
from pydantic import BaseModel
import uuid

class bookStructure(BaseModel):
    uid:uuid.UUID
    author:str
    title: str
    publisher:str
    published_date:date
    page_count:int
    genre:str
    language:str
    createdDate:datetime
    updatedDate:datetime

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