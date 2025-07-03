from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.crud import crud_books, crud_users, crud_managers
from . import schemas, models, auth
from .database import get_db, engine
from .Routers import users, books, managers 

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(managers.router)


@app.post('/login')
def login(email, password, db = Depends(get_db)):
    token = auth.authentication(email, password, db)
    return token
    
    

    

