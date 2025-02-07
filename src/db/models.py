from sqlmodel import SQLModel, Field, Column
from datetime import datetime, date
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func

# SQLAlchemy dialects allow it to communicate with different database engines, such as PostgreSQL,
# MySQL, SQLite and others.

class Book(SQLModel, table=True):
    __tablename__ = "Books"  # define the name of the table

    # UUID- Universally Unique Identifier instead of traditional integer-based primary keys
    # (id column with AUTO_INCREMENT)

    # Normally, SQLModel automatically converts Field() into an SQLAlchemy Column().
    # However, in some cases, we need to specify additional database-level properties that SQLModel
    # does not directly support, such as: Using PostgreSQL-specific types (e.g., pg.UUID)

    uid: uuid.UUID=Field( #used to define and configure attributes in a table class e.g primary keys etc
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    author: str
    title: str
    publisher: str
    published_date: date
    page_count: int
    genre: str
    language: str
    createdDate: datetime = Field(sa_column=Column(pg.TIMESTAMP,default=datetime.now))
    updatedDate: datetime = Field(sa_column=Column(pg.TIMESTAMP,onupdate=datetime.now,default=datetime.now))

    # repr is not a keyword but a special method (dunder) used to provide the string representation of
    # object

    def __repr__(self):
        return f"<Book {self.title}>"