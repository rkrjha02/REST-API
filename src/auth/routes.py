from datetime import datetime, timedelta
from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from src.db.main import getSession
from .service import userService
from .schema import userCreateModel, userModel, userLoginModel
from .utils import create_access_token, verify_password
from .dependencies import refreshTokenBearer

auth_router=APIRouter()
user_service=userService()

Refresh_Token_Expiry=2

@auth_router.post('/signup', response_model=userModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_details:userCreateModel,session:AsyncSession=Depends(getSession)):
    email=user_details.email

    userExist=await user_service.getUserByEmail(email,session)
    if userExist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User Already Exists")

    newUser=await user_service.createUser(user_details,session)
    return newUser

@auth_router.post('/login')
async def login_user(login_data:userLoginModel, session:AsyncSession=Depends(getSession)):
    email=login_data.email
    password=login_data.password

    user=await user_service.getUserByEmail(email,session)

    if user is not None:
        password_valid=verify_password(password, user.password)

        if password_valid:
            user_data = {'email': email, 'uid': str(user.uid)}
            access_token=create_access_token(user_data)

            refresh_token=create_access_token(user_data, refresh=True, expiry=timedelta(days=Refresh_Token_Expiry))

            return JSONResponse(
                content={
                    "message":"login Success",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":email,
                        "uid":str(user.uid)
                    }
                }
            )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email or Password")

@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict=Depends(refreshTokenBearer())):
    expiry_timestamp=token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp)>datetime.now():
        new_access_token=create_access_token(userData=token_details['user'])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired token")