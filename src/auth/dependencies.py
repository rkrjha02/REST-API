from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, status
from .utils import decode_token
from fastapi.exceptions import HTTPException

class accessTokenBearer(HTTPBearer):

    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        creds=await super().__call__(request)

        token=creds.credentials

        token_data=decode_token(token)

        if not self.isTokenValid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token")

        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a valid access token")

        print(creds.scheme)
        print(creds.credentials)

        return creds

    def isTokenValid(self, token:str):
        token_data=decode_token(token)

        return True if token_data is not None else False