import logging
import uuid
import jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
from src.config import Config

passwd_context=CryptContext(
    schemes=["bcrypt"]
)

ACCESS_TOKEN_EXPIRY=3600

def generate_password_hash(password:str)->str:
    Hash=passwd_context.hash(password)
    return Hash

def verify_password(password:str, Hash:str) -> bool:
    return passwd_context.verify(password,Hash)

def create_access_token(userData:dict, expiry:timedelta=None, refresh:bool=False):
    payload={}

    payload["user"]=userData
    payload["exp"]=datetime.now()+(expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti']=str(uuid.uuid4())
    payload['refresh']=refresh

    token=jwt.encode(payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    return token

def decode_token(token:str)->dict:
    try:
        token_data=jwt.decode(jwt=token, key=Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None