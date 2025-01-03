from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from src.Books.Book_data import Books
from src.Books.schemas import bookStructure, bookUpdateModel

#APIRouter is used to bundle the similar routes together i.e. if there are two users of website
#i.e. users and admin then it will be used to maintain the user routes under one object and admin
#in another
book_router=APIRouter()

# RETURN THE LIST OF ALL BOOKS AND RESPONSE MODEL IS USED TO DECIDE THE FORMAT VALIDATION BEFORE SENDING TO CLIENT
@book_router.get('/',response_model=List[bookStructure])
async def getAllBooks():
    return Books

#status.HTTP_201_CREATED is used to return the status that resource has been successfully created
#model_dump() is used to convert the model instance into dictionary for the ease of use
@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def createBook(newBookData:bookStructure)->dict:
    newBook=newBookData.model_dump()
    Books.append(newBook)
    return newBook

# Get A single Book with a particular Book_Id
@book_router.get('/{book_id}')
async def getBookByBookId(book_id:int):
    for book in Books:
        if book['id']==book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

#Update a Book
@book_router.patch('/{book_id}')
async def updateBookByBookId(book_id:int, bookUpdate:bookUpdateModel):
    print(book_id)
    for book in Books:
        if book["id"]==book_id:
            book["author"] = bookUpdate.author
            book["title"] = bookUpdate.title
            book["publisher"] = bookUpdate.publisher
            book["published_date"] = bookUpdate.published_date
            book["page_count"] = bookUpdate.page_count
            book["genre"] = bookUpdate.genre
            book["language"] = bookUpdate.language
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found Sorry!!!")

# Delete a Book
@book_router.delete('/{book_id}')
async def deleteBookByBookId(book_id:int):
    for book in Books:
        if book['id']==book_id:
            Books.remove(book)
            return "Removed Successfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found in Book List")