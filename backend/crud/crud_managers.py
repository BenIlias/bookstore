from sqlalchemy.orm import Session
from .. import schemas, models, face_recognition, auth



def createManager(manager: schemas.ManagerCreate, db: Session):
    manager_db = db.query(models.Manager).filter(models.Manager.email == manager.email).first()
    if manager_db:
        return None
    manager_db = manager.dict()
    
    hashed_password = auth.get_hashed(manager.password)
    # manager_data = manager.dict(exclude={'password'})
    manager_db.pop('password')
    manager_db = models.Manager(**manager_db, hashed_password=hashed_password)
    face_recognition.face_recognition()
    db.add(manager_db)
    db.commit()
    db.refresh(manager_db)
    return manager_db
    
    
    
    

