from fastapi import HTTPException
from .. import auth, schemas, models
from sqlalchemy.orm import Session
from . import crud_users

def getBookById(id: int, db: Session):
    return db.query(models.Book).filter(models.Book.id == id).first()

def createBook(book: schemas.BookCreate, db: Session, id_owner: int):
    book_db = db.query(models.Book).filter(models.Book.title == book.title).first()
    if book_db:
        return None
    owner = crud_users.getUserById(id_owner, db)
    if owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    
    book_db = models.Book(**book.dict(), id_owner=id_owner)
    db.add(book_db)
    db.commit()
    db.refresh(book_db)
    return book_db

def updateBook(book: schemas.BookCreate, db: Session, id: int):
    book_db = db.query(models.Book).filter(models.Book.id == id).first()
    if book_db is None:
        return None
    
    book_db.title = book.title
    book_db.author = book.author
    db.commit()
    db.refresh(book_db)
    return book_db

def deleteBook(id: int, db: Session):
    book_db = getBookById(id, db)
    if book_db is None:
        return None
    db.delete(book_db)
    db.commit()