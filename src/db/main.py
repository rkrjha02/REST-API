from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine,text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession

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

async def getSession()-> AsyncSession:

    Session=sessionmaker( bind=engine,class_=AsyncSession,expire_on_commit=False )

    async with Session() as session:
        yield session