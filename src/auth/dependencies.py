from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, status
from .utils import decode_token
from fastapi.exceptions import HTTPException
from ..db.redis import token_in_blocklist

class tokenBearer(HTTPBearer):

    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        creds=await super().__call__(request)

        token=creds.credentials

        token_data=decode_token(token)

        if not self.isTokenValid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token")

        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "error":"This token is Invalid or has been Revoked",
                "Resolution":"Generate New Access Token"
            })

        self.verify_token_data(token_data)

        return token_data

    def isTokenValid(self, token:str):
        token_data=decode_token(token)

        return True if token_data is not None else False

    def verify_token_data(self,token_data:dict)->None:
        raise NotImplementedError("Please Override this method in child class")

class accessTokenBearer(tokenBearer):
    def verify_token_data(self,token_data:dict)->None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a valid access token")

class refreshTokenBearer(tokenBearer):
    def verify_token_data(self,token_data:dict)->None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a valid refresh token")
