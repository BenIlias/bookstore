from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_POSTGRES = 'postgresql://ilias:ilias@localhost:5432/bookstoredb'
engine = create_engine(DATABASE_POSTGRES)
# database comment
LocalSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)




def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
        
