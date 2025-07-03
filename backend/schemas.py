from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str

class BookCreate(BookBase):
    pass 

class Book(BookBase):
    id: int
    id_owner: int
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str
    

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id : int
    is_admin: bool
    books: list[Book] 
    
    class Config:
        #orm_mode = True
        from_attributes = True



class ManagerBase(BaseModel):
    username: str
    email: str
    
    

class ManagerCreate(ManagerBase):
    password: str

class Manager(ManagerBase):
    id : int
    is_approved: bool = False
    class Config:
        #orm_mode = True
        from_attributes = True




