from fastapi import APIRouter, HTTPException, Depends
from .. import auth, models, schemas
from ..database import get_db
from ..crud import crud_managers

router = APIRouter()


@router.post('/managerCreate')
def createManager(manager: schemas.ManagerCreate, db = Depends(get_db)):
    manager_db = crud_managers.createManager(manager, db)
    if manager_db is None:
        raise HTTPException(status_code=404, detail='This Manager is already exists')

    return f'Hi {manager_db.username}, you are welcome'