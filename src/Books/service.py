from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import createBookModel,bookUpdateModel
from src.db.models import Book
from sqlmodel import select, desc

# Use of Session
# Session is like a temporary workspace for database changes.
# You add, modify, or delete data in the session before committing it to the actual database.
# If something goes wrong, you can rollback the changes to avoid corruption.

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

    #SQLAlchemy/SQLModel's execute() method does not automatically return the query results in the
    # format you expect. session.execute() returns a Result object, not the actual records directly

    async def createBook(self, book_data:createBookModel, session:AsyncSession):
        bookDictData=book_data.model_dump()
        newBookData=Book(
            **bookDictData
        )

        newBookData.published_date=datetime.strptime(bookDictData['published_date'],"%Y-%m-%d")

        newBookData.createdDate = datetime.now()
        newBookData.updatedDate = datetime.now()

        session.add(newBookData)
        await session.commit()

        return newBookData

    # **bookDictData syntax is Python's dictionary unpacking operator (**kwargs). It is used to pass
    # the dictionary’s key-value pairs as keyword arguments to the Book model.

    async def updateBook(self, book_id:str, book_data:bookUpdateModel, session:AsyncSession):
        bookToUpdate=await self.getBook(book_id,session)

        if bookToUpdate is not None:
            updateBookDataDict = book_data.model_dump()
            for key,value in updateBookDataDict.items():
                setattr(bookToUpdate,key,value)

            await session.commit()
            return bookToUpdate
        else:
            return None

    async def deleteBook(self, book_id:str, session:AsyncSession):
        bookToDelete = await self.getBook(book_id, session)

        if bookToDelete is not None:
            await session.delete(bookToDelete)
            await session.commit()
            return {}
        else:
            return None