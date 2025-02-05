from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import createBookModel,bookUpdateModel
from src.db.models import Book
from sqlmodel import select, desc

class bookService:
    async def getAllBooks(self, session:AsyncSession):
        statement=select(Book).order_by(desc(Book.createdDate))

        result=await session.exec(statement)
        return result.all()

    async def getBook(self, book_id:str, session:AsyncSession):
        statement = select(Book).where(Book.uid==book_id)

        result=await session.exec(statement)
        book=result.first()

        return book if book is not None else None

    async def createBook(self, book_data:createBookModel, session:AsyncSession):
        bookDictData=book_data.model_dump()
        newBookData=Book(
            **bookDictData
        )

        session.add(newBookData)
        await session.commit()

        return newBookData

    async def updateBook(self, book_id:str, book_data:bookUpdateModel, session:AsyncSession):
        bookToUpdate=self.getBook(book_id,session)
        updateBookDataDict=book_data.model_dump()

        if bookToUpdate is not None:
            for key,value in updateBookDataDict:
                setattr(bookToUpdate,key,value)

            await session.commit()
            return bookToUpdate
        else:
            return None

    async def deleteBook(self, book_id:str, session:AsyncSession):
        pass