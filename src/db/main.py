from sqlmodel import create_engine,text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config

#ORM- Object Relational Mapper translates programming language and database.
    #--> Classes=Tables
    #--> Objects=Each Row

#SQLAlchemy- most popular ORM for Python

#SQLModel- offers seamless integration of SQLAlchemy and Pydantic Model

engine=AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))

async def dataBaseinit():
    async with engine.begin() as conn:
        # noinspection PyUnresolvedReferences
        from src.db.models import Book

        print("MetaData Start...")
        await conn.run_sync(SQLModel.metadata.create_all)
        print("MetaData End...")