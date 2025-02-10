from passlib.context import CryptContext

passwd_context=CryptContext(
    schemes=["bcrypt"]
)

def generate_password_hash(password:str)->str:
    Hash=passwd_context.hash(password)
    return Hash

def verify_password(password:str, Hash:str) -> bool:
    return passwd_context.verify(password,Hash)