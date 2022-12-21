import tkinter as tk
from tkinter import ttk
from models import Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import crud


Base.metadata.create_all(bind=engine)

def get_db(func):
    def wrapper(*args, **kwargs):
        db = SessionLocal()
        try:
            result = func(db)
        finally:
            db.close()
        return result
    return wrapper

@get_db
def create_key(db: Session):
    crud.create_access_key(db)

create_key()
@get_db
def get_cicilan(db: Session): 
    print(crud.get_cicilan(db))
get_cicilan()
# root = tk.Tk()
# root.withdraw()



# root.mainloop()
