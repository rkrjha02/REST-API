import uuid
from sqlmodel import SQLModel,Field,Column
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

#Command - alembic init -t async migration

#alembic init: Initializes Alembic in your project.
#-t async: Sets up asynchronous support for migrations.

class User(SQLModel, table=True):

    __tablename__ = "users"

    uid:uuid.UUID=Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username:str
    email:str
    password:str=Field(exclude=True)
    first_name:str
    last_name:str
    is_verified:bool=Field(default=False)
    createdDate: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updatedDate: datetime = Field(sa_column=Column(pg.TIMESTAMP, onupdate=datetime.now, default=datetime.now))

    def __repr__(self):
        return f"<User {self.username}>"