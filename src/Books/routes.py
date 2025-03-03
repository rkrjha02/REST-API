from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.Books.schemas import bookStructure, bookUpdateModel, createBookModel
from .service import bookService
from ..db.main import getSession
from ..auth.dependencies import accessTokenBearer

#APIRouter is used to bundle the similar routes together i.e. if there are two users of website
#i.e. users and admin then it will be used to maintain the user routes under one object and admin
#in another
book_router=APIRouter()
book_service=bookService()
access_token_bearer=accessTokenBearer()

# RETURN THE LIST OF ALL BOOKS AND RESPONSE MODEL IS USED TO DECIDE THE FORMAT VALIDATION BEFORE SENDING TO CLIENT
@book_router.get('/',response_model=List[bookStructure])
async def getAllBooks(session:AsyncSession=Depends(getSession), user_details=Depends(access_token_bearer)):
    Books=await book_service.getAllBooks(session)
    return Books

#status.HTTP_201_CREATED is used to return the status that resource has been successfully created
#model_dump() is used to convert the model instance into dictionary for the ease of use
@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=bookStructure)
async def createBook(newBookData:createBookModel, session:AsyncSession=Depends(getSession), user_details=Depends(access_token_bearer))->dict:
    newBook=await book_service.createBook(newBookData,session)
    return newBook

# Get A single Book with a particular Book_Id
@book_router.get('/{book_id}',response_model=bookStructure)
async def getBookByBookId(book_id:str, session:AsyncSession=Depends(getSession), user_details=Depends(access_token_bearer)):

    book=await book_service.getBook(book_id,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

#Update a Book
@book_router.patch('/{book_id}', response_model=bookStructure)
async def updateBookByBookId(book_id:str, bookUpdate:bookUpdateModel,session:AsyncSession=Depends(getSession), user_details=Depends(access_token_bearer)):
    updated_book=await book_service.updateBook(book_id,bookUpdate,session)

    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found Sorry!!!")

# Delete a Book
@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteBookByBookId(book_id:str, session:AsyncSession=Depends(getSession), user_details=Depends(access_token_bearer)):

    delete_book=await book_service.deleteBook(book_id, session)

    if delete_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found in Book List")
    else:
        return {}