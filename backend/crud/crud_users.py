from .. import auth, schemas, models
from sqlalchemy.orm import Session


def getUserById(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

def getUserByEmail(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def createUser(user: schemas.UserCreate, db: Session):
    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    if user_db:
        return None
    user_db = user.dict()
    hashed_password = auth.get_hashed(user.password)
    user_db['hashed_password'] = hashed_password
    user_db.pop('password') # remove password field to replace it with hashed_password
    user_db = models.User(**user_db)
    
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def updateUser(user: schemas.UserCreate, db: Session, id:int):
    user_db = getUserById(id, db)
    if user_db is None:
        return None
    hashed_password = auth.get_hashed(user.password)
    user_db.username = user.username
    user_db.email = user.email
    user_db.hashed_password = hashed_password 
    db.commit()
    return user_db
    
def deleteUser(id: int, db: Session):
    user_db = getUserById(id, db)
    if user_db is None:
        return None
    db.delete(user_db)
    db.commit()
    


    
    