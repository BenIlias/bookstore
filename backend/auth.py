from fastapi import HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.crud import crud_users
from jose import jwt, JWTError
from datetime import timedelta, datetime


KEY_CODE = 'lifeisgood'
Algorithm = 'HS256'



token_checker = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def extract_token(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer'):
        raise HTTPException(status_code=404, detail='Missing or invalid Authorization header')
    
    token = auth_header.split(" ")[1]
    return token

    


def get_hashed(password):
    return pwd_context.hash(password)

def verify_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def createAccessToken(data: dict, expiry_time: timedelta):
    to_code = data.copy()
    if expiry_time:
        to_code.update({'exp': datetime.utcnow() + expiry_time})
    else:
        to_code.update({'exp': datetime.utcnow() + timedelta(minutes=15)})
    
    access_token = jwt.encode(to_code, KEY_CODE, Algorithm)
    
    return access_token
    
def decode_token(token: str):
    try:
        payload = jwt.decode(token, KEY_CODE, Algorithm)
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def authentication(email: str, password: str, db: Session):
    user_db = crud_users.getUserByEmail(email, db)
    if user_db is None:
        raise HTTPException(status_code=404, detail='The email or the password is not correct') 
    
    if not verify_hash(password, user_db.hashed_password):
        raise HTTPException(status_code=404, detail='The email or the password is not correct') 
    
    access_token = createAccessToken(data={'sub': user_db.username}, expiry_time=timedelta(minutes=30))
    
    return access_token

