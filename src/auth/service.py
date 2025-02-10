from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import User
from .schema import userCreateModel
from .utils import generate_password_hash

class userService:
    async def getUserByEmail(self, email:str, session:AsyncSession):
        statement=select(User).where(User.email==email)

        result=await session.exec(statement)
        user=result.first()

        return user

    async def userExists(self, email:str, session:AsyncSession):
        user = await self.getUserByEmail(email,session)

        return True if user is not None else False

    async def createUser(self, userData:userCreateModel, session:AsyncSession):
        userDataDict=userData.model_dump()
        newUser=User(**userDataDict)

        newUser.password=generate_password_hash(userDataDict['password'])
        session.add(newUser)

        await session.commit()
        return newUser