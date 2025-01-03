from pydantic import BaseModel

class bookStructure(BaseModel):
    id:int
    author:str
    title: str
    publisher:str
    published_date:str
    page_count:int
    genre:str
    language:str

class bookUpdateModel(BaseModel):
    author:str
    title:str
    publisher:str
    published_date:str
    page_count:int
    genre:str
    language:str