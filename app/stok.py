import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from sqlalchemy.orm import Session
from database import get_db
import crud


def stok(parent: ttk.Notebook):
    global himpunan_barang
    global himpunan_siswa
    himpunan_barang = []
    himpunan_siswa = []
    main_frame = ttk.Frame(parent)
    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    sub_frame_1 = ttk.Frame(main_frame)
    sub_frame_2 = ttk.Frame(main_frame)
    sub_frame_3 = ttk.Frame(main_frame)
    sub_frame_4 = ttk.Frame(main_frame)
    sub_frame_5 = ttk.Frame(main_frame)
    treeview_barang = ttk.Treeview(sub_frame_2, columns=('nama_barang', 'tersedia', 'modal', 'harga_jual', 'bisa_dicicil'), show='headings')
    treeview_siswa = ttk.Treeview(sub_frame_5, columns=('nisn', 'nama', 'kelas'), show='headings')
    masukan_data_siswa_button = ttk.Button(sub_frame_5, text='Masukan Data', style='green.TButton', command=lambda: masukan_data_siswa_klik())
    hapus_data_siswa_button = ttk.Button(sub_frame_5, text='Hapus Data', style='red.TButton', command=lambda: hapus_data_siswa_klik())
    tambah_barang_baru_button = ttk.Button(sub_frame_3, text='Barang Baru', style='green.TButton', command=lambda: tambah_barang_baru_klik())
    tambah_stok_barang_button = ttk.Button(sub_frame_3, text='Tambah Stok', style='blue.TButton', state='disabled', command=lambda: tambah_stok_barang_klik())
    hapus_barang_button = ttk.Button(sub_frame_3, text='Hapus Barang', style='red.TButton', state='disabled', command=lambda: hapus_barang_klik())
    scrollbar_barang = ttk.Scrollbar(sub_frame_2, orient=tk.VERTICAL, command=treeview_barang.yview)
    scrollbar_siswa = ttk.Scrollbar(sub_frame_5, orient=tk.VERTICAL, command=treeview_siswa.yview)
    cari_siswa_entry = ttk.Entry(sub_frame_5)
    cari_siswa_button = ttk.Button(sub_frame_5, text='Cari', style='blue.TButton', command=lambda: cari_siswa_klik())
    refresh_siswa_button = ttk.Button(sub_frame_5, text='Refresh...', command=lambda: refresh_siswa())
    refresh_barang_button = ttk.Button(sub_frame_3, text='Refresh...', command=lambda: refresh_barang())


    def tambah_barang_baru_klik():
        def konfirmasi():
            if len(nama_barang_entry.get()) > 0 and int(harga_awal_spinbox.get()) >= 100 and int(harga_jual_spinbox.get()) >= 500 and int(jumlah_barang_spinbox.get()) > 0: 
                if messagebox.askokcancel('Warning !', 'Anda yakin ? Pastikan tidak ada data yang salah !', icon=messagebox.WARNING):
                    tambah_barang_baru(nama_barang_entry.get(), int(jumlah_barang_spinbox.get()), int(harga_awal_spinbox.get()), int(harga_jual_spinbox.get()), bool(bisa_dicicil.get()))
                    dissmiss()
                    refresh_barang()
                    
            else: 
                messagebox.showwarning('Warning !', 'Harap lengkapi seluruh data !')


        def dissmiss():
            main_window.grab_release()
            main_window.destroy()
        
        main_window = tk.Toplevel(parent)
        main_window.title('Tambah Barang Baru')
        main_window.geometry(f'300x200+{parent.winfo_screenwidth()//2 - 150}+{parent.winfo_screenheight()//2 - 200}')
        main_window.resizable(tk.FALSE, tk.FALSE)
        main_window.wm_protocol('WM_DELETE_WINDOW', dissmiss)
        main_window.wait_visibility()
        main_window.grab_set()
        main_window.columnconfigure(1, weight=1)
        main_window.rowconfigure(1, weight=1)

        main_frame = ttk.Frame(main_window)
        main_frame.grid(column=1, row=1, sticky=tk.NSEW)
        main_frame.columnconfigure(1, weight=7)
        main_frame.columnconfigure(2, weight=3)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        main_frame.rowconfigure(5, weight=1)
        main_frame.rowconfigure(6, weight=1)

        bisa_dicicil = tk.IntVar()
        nama_barang_entry = ttk.Entry(main_frame, font=('Arial', 12, 'normal'))
        jumlah_barang_spinbox = ttk.Spinbox(main_frame, from_=1, to=100_000)
        harga_awal_spinbox = ttk.Spinbox(main_frame, from_=1, to=10_000_000_000)
        harga_jual_spinbox = ttk.Spinbox(main_frame, from_=1, to=20_000_000_000)
        bisa_dicicil_checkbutton = ttk.Checkbutton(main_frame, text='Bisa dicicil. ', variable=bisa_dicicil)
        konfirmasi_button = ttk.Button(main_frame, text='Konfirmasi', style='blue.TButton', command=lambda: konfirmasi())
        ttk.Label(main_frame, text='Nama Barang', font=('Arial', 12, 'normal')).grid(column=1, row=1, sticky=tk.NSEW)
        ttk.Label(main_frame, text='Jumlah', font=('Arial', 12, 'normal')).grid(column=1, row=2, sticky=tk.NSEW)
        ttk.Label(main_frame, text='Harga Beli', font=('Arial', 12, 'normal')).grid(column=1, row=3, sticky=tk.NSEW)
        ttk.Label(main_frame, text='Harga Jual', font=('Arial', 12, 'normal')).grid(column=1, row=4, sticky=tk.NSEW)
        nama_barang_entry.grid(column=2, row=1, sticky=tk.NSEW, padx=2, pady=4)
        jumlah_barang_spinbox.grid(column=2, row=2, sticky=tk.NSEW, padx=2, pady=4)
        harga_awal_spinbox.grid(column=2, row=3, sticky=tk.NSEW, padx=2, pady=4)
        harga_jual_spinbox.grid(column=2, row=4, sticky=tk.NSEW, padx=2, pady=4)
        bisa_dicicil_checkbutton.grid(column=1, columnspan=2, row=5, sticky=tk.NSEW, padx=2, pady=4)
        konfirmasi_button.grid(column=1, columnspan=2, row=6, sticky=tk.NSEW, padx=2, pady=4)

        nama_barang_entry.focus()
        nama_barang_entry.bind('<Return>', lambda e: jumlah_barang_spinbox.focus())
        jumlah_barang_spinbox.bind('<Return>', lambda e: harga_awal_spinbox.focus())
        harga_awal_spinbox.bind('<Return>', lambda e: harga_jual_spinbox.focus())
        harga_jual_spinbox.bind('<Return>', lambda e: konfirmasi_button.invoke())




    def tambah_stok_barang_klik():
        def konfirmasi():
            jumlah_tambah = int(jumlah_tambah_spinbox.get())
            if jumlah_tambah > 0:
                tambah_stok_barang(int(treeview_barang.selection()[0]), jumlah_tambah)
                refresh_barang()
                dissmiss()
            else: 
                messagebox.showwarning('Warning !', 'Jumlah tambah harus lebih dari 0 !')


        def dissmiss():
            main_window.grab_release()
            main_window.destroy()
        
        main_window = tk.Toplevel(parent)
        main_window.title('Tambah Stok Barang')
        main_window.geometry(f'260x50+{parent.winfo_screenwidth()//2 - 130}+{parent.winfo_screenheight()//2 - 25}')
        main_window.resizable(tk.FALSE, tk.FALSE)
        main_window.wm_protocol('WM_DELETE_WINDOW', dissmiss)
        main_window.wait_visibility()
        main_window.grab_set()
        main_window.columnconfigure(1, weight=1)
        main_window.rowconfigure(1, weight=1)

        main_frame = ttk.Frame(main_window)
        main_frame.grid(column=1, row=1, sticky=tk.NSEW)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        ttk.Label(main_frame, text='Jumlah Tambah Stok: ', justify=tk.CENTER, anchor=tk.CENTER).grid(column=1, row=1, sticky=tk.NSEW)
        jumlah_tambah_spinbox = ttk.Spinbox(main_frame, from_=1, to=100_000)
        jumlah_tambah_spinbox.set(1)
        jumlah_tambah_spinbox.grid(column=1, row=2, sticky=tk.NSEW)
        jumlah_tambah_spinbox.bind('<Return>', lambda e: tombol_konfirmasi.invoke())
        tombol_konfirmasi = ttk.Button(main_frame, text='Konfirmasi', style='blue.TButton', command=lambda: konfirmasi())
        tombol_konfirmasi.grid(column=1, row=3, sticky=tk.NSEW)






    def hapus_barang_klik():
        if messagebox.askokcancel('Warning !', 'Apakah anda yakin ingin menghapus barang ini ? (Barang yang bisa dihapus hanya barang yang belum pernah dibeli atau dicicil. )'):
            if hapus_barang(int(treeview_barang.selection()[0])):
                messagebox.showerror('Error !', 'Barang tidak bisa dihapus karena sudah pernah dibeli atau dicicil !')
        refresh_barang()


    def masukan_data_siswa_klik():
        if messagebox.askokcancel('Warning !', 'File harus berformat xlsx atau xls, hanya merupakan tabel data dan memiliki kolom nisn, nama, dan kelas.', icon=messagebox.WARNING): 
            try: 
                masukan_data_siswa(filedialog.askopenfilename(title='Pilih File Excel untuk data Siswa', filetypes=[('Excel File...', '.xlsx', '.xls')]))
                refresh_siswa()
            except:
                messagebox.showerror('Error !', 'Tidak dapat memasukan data siswa melalui file yang dipilih !')


    def hapus_data_siswa_klik():
        if messagebox.askokcancel('Warning !', 'Apakah anda yakin ? Seluruh data siswa akan dihapus kecuali yang masih memiliki cicilan !'):
            hapus_data_siswa()
            refresh_siswa()


    def cari_siswa_klik():
        if cari_siswa_entry.get() == '':
            refresh_siswa()
        else: 
            treeview_siswa.delete(*treeview_siswa.get_children())
            for siswa in list(filter(lambda siswa: cari_siswa_entry.get().lower() in siswa.nama.lower()+siswa.nisn.lower()+siswa.kelas.lower(), himpunan_siswa)):
                treeview_siswa.insert('', 'end', iid=siswa.nisn, values=(siswa.nisn, siswa.nama, siswa.kelas))


    def refresh_barang():
        global himpunan_barang
        himpunan_barang = muat_barang()
        treeview_barang.delete(*treeview_barang.get_children())
        for barang in himpunan_barang:
            treeview_barang.insert(
                '', 
                'end', 
                iid=str(barang.id), 
                values=(
                    barang.nama_barang, 
                    f'{barang.tersedia_saat_ini}/{barang.tersedia}', 
                    crud.angka_mudah_dibaca(barang.modal), 
                    crud.angka_mudah_dibaca(barang.harga_jual), 
                    'Bisa' if barang.bisa_dicicil else 'Tidak Bisa'
                )
            )
        hapus_barang_button.state(['disabled'])
        tambah_stok_barang_button.state(['disabled'])


    def refresh_siswa():
        global himpunan_siswa
        himpunan_siswa = muat_siswa()
        treeview_siswa.delete(*treeview_siswa.get_children())
        for siswa in himpunan_siswa:
            treeview_siswa.insert('', 'end', iid=siswa.nisn, values=(siswa.nisn, siswa.nama, siswa.kelas))


    ttk.Label(sub_frame_1, text='Barang', font=('Arial', 14, 'bold')).grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    ttk.Label(sub_frame_4, text='Siswa', font=('Arial', 14, 'bold')).grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)

    treeview_barang.heading('nama_barang', text='Nama Barang')
    treeview_barang.heading('tersedia', text='Tersedia')
    treeview_barang.heading('modal', text='Harga Beli')
    treeview_barang.heading('harga_jual', text='Harga Jual')
    treeview_barang.heading('bisa_dicicil', text='Bisa Dicicil')
    treeview_barang.configure(yscrollcommand=scrollbar_barang.set)
    treeview_barang.grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    scrollbar_barang.grid(column=2, row=1, sticky=tk.NS)
    treeview_barang.bind('<<TreeviewSelect>>', lambda e: [hapus_barang_button.state(['!disabled']), tambah_stok_barang_button.state(['!disabled'])] if len(treeview_barang.selection()) > 0 else [])

    treeview_siswa.heading('nisn', text='NISN')
    treeview_siswa.heading('nama', text='Nama Siswa')
    treeview_siswa.heading('kelas', text='Kelas')
    treeview_siswa.configure(yscrollcommand=scrollbar_siswa.set)
    treeview_siswa.grid(column=1, row=1, rowspan=6, sticky=tk.NSEW, padx=4, pady=6)
    scrollbar_siswa.grid(column=2, row=1, rowspan=6, sticky=tk.NS)

    masukan_data_siswa_button.grid(column=3, row=1, sticky=tk.NSEW, padx=4, pady=6)
    hapus_data_siswa_button.grid(column=3, row=2, sticky=tk.NSEW, padx=4, pady=6)
    ttk.Label(sub_frame_5, text='Cari Siswa', font=('Arial', 12, 'normal')).grid(column=3, row=3)
    cari_siswa_entry.grid(column=3, row=4, sticky=tk.NSEW, padx=4, pady=6)
    cari_siswa_button.grid(column=3, row=5, sticky=tk.NSEW, padx=4, pady=6)

    tambah_barang_baru_button.grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    tambah_stok_barang_button.grid(column=2, row=1, sticky=tk.NSEW, padx=4, pady=6)
    refresh_barang_button.grid(column=3, row=1, sticky=tk.NSEW, padx=4, pady=6)
    hapus_barang_button.grid(column=5, row=1, sticky=tk.NSEW, padx=4, pady=6)

    cari_siswa_entry.bind('<Return>', lambda e: cari_siswa_button.invoke())
    refresh_siswa_button.grid(column=3, row=6, sticky=tk.NSEW, padx=4, pady=6)

    sub_frame_1.grid(column=1, row=1, sticky=tk.NSEW)
    sub_frame_2.grid(column=1, row=2, sticky=tk.NSEW)
    sub_frame_3.grid(column=1, row=3, sticky=tk.NSEW)
    sub_frame_4.grid(column=1, row=4, sticky=tk.NSEW)
    sub_frame_5.grid(column=1, row=5, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=5)
    main_frame.rowconfigure(2, weight=60)
    main_frame.rowconfigure(3, weight=10)
    main_frame.rowconfigure(4, weight=5)
    main_frame.rowconfigure(5, weight=20)
    sub_frame_1.columnconfigure(1, weight=1)
    sub_frame_1.rowconfigure(1, weight=1)
    sub_frame_2.columnconfigure(1, weight=1)
    sub_frame_2.rowconfigure(1, weight=1)
    sub_frame_3.columnconfigure(1, weight=1)
    sub_frame_3.columnconfigure(2, weight=1)
    sub_frame_3.columnconfigure(3, weight=1)
    sub_frame_3.columnconfigure(4, weight=8)
    sub_frame_3.columnconfigure(5, weight=1)
    sub_frame_3.rowconfigure(1, weight=1)
    sub_frame_4.columnconfigure(1, weight=1)
    sub_frame_4.rowconfigure(1, weight=1)
    sub_frame_5.columnconfigure(1, weight=8)
    sub_frame_5.columnconfigure(3, weight=4)
    sub_frame_5.rowconfigure(1, weight=3)
    sub_frame_5.rowconfigure(2, weight=3)
    sub_frame_5.rowconfigure(3, weight=2)
    sub_frame_5.rowconfigure(4, weight=2)
    sub_frame_5.rowconfigure(5, weight=3)
    sub_frame_5.rowconfigure(6, weight=2)

    refresh_barang()
    refresh_siswa()
    return main_frame


@get_db
def muat_barang(db: Session):
    return crud.ambil_barang(db)


@get_db
def muat_siswa(db: Session):
    return crud.ambil_siswa(db)


@get_db
def hapus_data_siswa(db: Session):
    crud.hapus_siswa(db)


@get_db
def masukan_data_siswa(db: Session, file_loc: str):
    crud.tambah_siswa(db, file_loc)


@get_db
def tambah_barang_baru(db: Session, nama_barang: str, tersedia: int, modal: int, harga_jual: int, bisa_dicicil: bool):
    crud.tambah_barang(db, nama_barang, tersedia, modal, harga_jual, bisa_dicicil)


@get_db
def tambah_stok_barang(db: Session, id_barang: int, jumlah_tambah: int):
    crud.tambah_stok_barang(db, id_barang, jumlah_tambah)


@get_db
def hapus_barang(db: Session, id_barang: int):
    return crud.hapus_barang(db, id_barang)
