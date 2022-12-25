import tkinter as tk
from tkinter import ttk
from models import Base
from database import engine, SessionLocal, get_db
from datetime import datetime
from sqlalchemy.orm import Session
import crud


Base.metadata.create_all(bind=engine)


@get_db
def buat_kunci(db: Session):
    crud.buat_kunci_akses(db)


buat_kunci()


@get_db
def test(db: Session):
    # crud.tambah_barang(db, "Topi", 12, 12500, 20000, True)
    # crud.tambah_siswa(db, "C:/Users/airel/OneDrive/Desktop/Book1.xlsx")
    # crud.tambah_cicilan(db, ["123"], 1, 3)
    # crud.bayar_cicilan(db, 1, 1, 20_000)
    # crud.bayar_cicilan(db, 1, 1, 20_000)
    # crud.bayar_cicilan(db, 1, 1, 20_000)
    crud.buat_laporan(db, 2, 'SMKN 5 Kota Tangerang', 'C:/Users/airel/OneDrive/Desktop/', dari=datetime(2021, 1, 1), sampai=datetime(2023, 12, 31))
    print(crud.bagi_pembayaran(127000, 20))
    print(sum(crud.bagi_pembayaran(127000, 20)))


test()
# root = tk.Tk()
# root.withdraw()


# root.mainloop()
