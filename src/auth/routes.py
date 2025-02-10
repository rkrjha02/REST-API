from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import getSession
from .service import userService
from .schema import userCreateModel, userModel

auth_router=APIRouter()
user_service=userService()

@auth_router.post('/signup', response_model=userModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_details:userCreateModel,session:AsyncSession=Depends(getSession)):
    email=user_details.email

    userExist=await user_service.getUserByEmail(email,session)
    if userExist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User Already Exists")

    newUser=await user_service.createUser(user_details,session)
    return newUser