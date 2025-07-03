from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import auth, models, schemas
from ..database import get_db
from ..crud import crud_users

router = APIRouter()


@router.post('/userCreate')
def createUser(user: schemas.UserCreate, db = Depends(get_db)):
    user_db = crud_users.createUser(user, db)
    if user_db is None:
        raise HTTPException(status_code=404, detail='This user is already exists')
    return {f'Hi {user_db.username}, your account has been created successfully'}

@router.delete('/deleteUser')
def deleteUser(userEmail: str, db: Session = Depends(get_db)):
    user_db = crud_users.getUserByEmail(userEmail, db)
    if user_db is None:
        raise HTTPException(status_code=404, detail='Sorry, this user is not existing')
    crud_users.deleteUser(user_db.id, db)
    
    return f'The user {user_db.email} has been deleted'

@router.get('/cuurentSession')
def checkCurrentSession(request: Request, db: Session = Depends(get_db)):
    token = auth.extract_token(request)
    username = auth.decode_token(token)
    user_db = db.query(models.User).filter(models.User.username == username).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail='The token is not valid')
    
    return user_db