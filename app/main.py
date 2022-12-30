import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models import Base
from database import engine, get_db
from sqlalchemy.orm import Session
import crud
from penjualan import penjualan
from cicilan import cicilan
from pembukuan import pembukuan
from stok import stok
from stylize import stylize


Base.metadata.create_all(bind=engine)


@get_db
def buat_kunci(db: Session):
    crud.buat_kunci_akses(db)


buat_kunci()

def main(parent: tk.Tk):
    parent.withdraw()
    main_window = tk.Toplevel(parent)
    main_window.wm_protocol('WM_DELETE_WINDOW', lambda: parent.destroy())
    main_window.title('Program Koperasi | Oleh Airell Zulkarnain')
    width = parent.winfo_screenwidth()
    height = parent.winfo_screenheight()
    main_window.geometry(f'{width-40}x{height-90}+{12}+{16}')
    main_window.resizable(tk.FALSE, tk.FALSE)

    panes = ttk.Notebook(main_window)
    panes.grid(column=1, row=1, sticky=tk.NSEW)
    panes.add(stok(panes), text='Stok')
    panes.add(penjualan(panes), text='Penjualan')
    panes.add(cicilan(panes), text='Cicilan')
    panes.add(pembukuan(panes), text='Pembukuan')

    panes.columnconfigure(1, weight=1)
    panes.rowconfigure(1, weight=1)
    main_window.rowconfigure(1, weight=1)
    main_window.columnconfigure(1, weight=1)


@get_db
def masuk(db: Session):
    valid = crud.verifikasi_kunci_akses(db, kunci_akses.get())
    if valid:
        if valid == crud.ambil_uuid()*2:
            ubah_kunci_akses(root)
        else:
            main(root)
    else:
        messagebox.showwarning('Warning', 'Kunci Akses Tidak Valid !')


@get_db
def ubah_kunci_akses(db: Session, parent: tk.Tk):
    def ubah():
        if len(kunci_baru.get()) >= 8 and kunci_baru.get() != crud.ambil_uuid():
            crud.ubah_kunci_akses(db, kunci_baru.get())
            main_window.grab_release()
            main_window.destroy()
            main(parent)
        else:
            messagebox.showwarning('Warning', 'Kunci Akses harus lebih panjang dari 8 karakter !')
    parent.withdraw()
    main_window = tk.Toplevel(parent)
    main_window.title('Ubah Kunci Akses')
    main_window.wm_protocol('WM_DELETE_WINDOW', lambda: root.destroy())
    main_window.geometry(f'400x80+{root.winfo_screenwidth()//2 - 200}+{root.winfo_screenheight()//2 - 40}')
    main_window.resizable(tk.FALSE, tk.FALSE)
    main_window.grab_set()
    main_window.rowconfigure(1, weight=1)
    main_window.columnconfigure(1, weight=1)
    main_frame = ttk.Frame(main_window)
    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    kunci_baru = tk.StringVar()
    ttk.Label(main_frame, text='Buat kunci akses baru (Minimal 8 Karakter)!', anchor='center', font=('Arial', 12, 'normal')).grid(column=1, row=1, sticky=tk.EW)
    masukan_kunci_baru = ttk.Entry(main_frame, textvariable=kunci_baru, font=('Arial', 12, 'normal'))
    masukan_kunci_baru.focus()
    masukan_kunci_baru.bind('<Return>', lambda e: tombol_ubah.invoke())
    masukan_kunci_baru.grid(column=1, row=2, sticky=tk.EW)
    tombol_ubah = ttk.Button(main_frame, text='Ubah', command=ubah, style='blue.TButton')
    tombol_ubah.grid(column=1, row=3, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(3, weight=1)





root = tk.Tk()
root.title('Program Koperasi | Login')
root.resizable(tk.FALSE, tk.FALSE)
root.geometry(f'400x120+{root.winfo_screenwidth()//2 - 200}+{root.winfo_screenheight()//2 - 60}')

stylize(ttk.Style)

kunci_akses = tk.StringVar()
login_frame = ttk.Frame(root)
login_frame.grid(column=1, row=1, sticky=tk.NSEW)

ttk.Label(login_frame, text='Program Koperasi', anchor='center', font=('Arial', 16, 'bold')).grid(column=1, row=1, sticky=tk.EW, pady=4)

masukan_kunci_akses = ttk.Entry(login_frame, textvariable=kunci_akses, justify=tk.CENTER, font=('Arial', 14, 'normal'))
masukan_kunci_akses.grid(column=1, row=2, sticky=tk.EW)
masukan_kunci_akses.bind('<Return>', lambda e: tombol_masuk.invoke())
masukan_kunci_akses.focus()

tombol_masuk = ttk.Button(login_frame, text='Masuk', command=masuk, style='blue.TButton')
tombol_masuk.grid(column=1, row=3, sticky=tk.NSEW)

ttk.Label(login_frame, text='Oleh Airell Zulkarnain', anchor='center', font=('Arial', 8, 'normal')).grid(column=1, row=4, sticky=tk.EW)


login_frame.columnconfigure(1, weight=1)
login_frame.rowconfigure(3, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()