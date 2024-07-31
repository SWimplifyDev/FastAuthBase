from models import UserInDB
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import crud
from fastapi import HTTPException

SECRET_KEY = "secret-key"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(SECRET_KEY)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(email:str):
    user_dict = crud.search_user(email)
    if user_dict:
        return UserInDB(**user_dict)

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if user:
        if verify_password(password, user.password):
            return user
        
def encrypt_user(emial:str):
    return serializer.dumps(emial)

def decrypt_user(session_token:str) -> str:
    try:
        username = serializer.loads(session_token, max_age=3600)
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=403, detail="Not authenticated")
    return username

def check_permissions(session_token:str):
    if not session_token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    username = decrypt_user(session_token)
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return user