import tkinter as tk
from tkinter import ttk
import tkcalendar as tkc
from datetime import datetime
from tkinter import messagebox
from sqlalchemy.orm import Session
from database import get_db
from models import Size
import crud


def stok(parent: ttk.Notebook):
    global himpunan_barang
    himpunan_barang = []
    main_frame = ttk.Frame(parent)
    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    sub_frame_1 = ttk.Frame(main_frame)
    sub_frame_2 = ttk.Frame(main_frame)
    sub_frame_3 = ttk.Frame(main_frame)
    treeview_barang = ttk.Treeview(
        sub_frame_2,
        columns=("nama_barang", "ukuran", "tersedia", "modal", "harga_jual"),
        show="headings",
    )
    tambah_barang_baru_button = ttk.Button(
        sub_frame_3,
        text="Stok",
        style="green.TButton",
        command=lambda: tambah_barang_baru_klik(),
    )
    tambah_stok_barang_button = ttk.Button(
        sub_frame_3,
        text="Pembelian",
        style="blue.TButton",
        state="disabled",
        command=lambda: tambah_stok_barang_klik(),
    )
    hapus_barang_button = ttk.Button(
        sub_frame_3,
        text="Hapus Barang",
        style="red.TButton",
        state="disabled",
        command=lambda: hapus_barang_klik(),
    )
    scrollbar_barang = ttk.Scrollbar(
        sub_frame_2, orient=tk.VERTICAL, command=treeview_barang.yview
    )
    refresh_barang_button = ttk.Button(
        sub_frame_3, text="Refresh...", command=lambda: refresh_barang()
    )

    def tambah_barang_baru_klik():
        def konfirmasi():
            if (
                len(nama_barang_entry.get()) > 0
                and int(harga_awal_spinbox.get()) >= 0
                and int(harga_jual_spinbox.get()) >= 0
                and int(jumlah_barang_spinbox.get()) > 0
            ):
                if messagebox.askokcancel(
                    "Warning !",
                    "Anda yakin ? Pastikan tidak ada data yang salah !",
                    icon=messagebox.WARNING,
                ):
                    tambah_barang_baru(
                        nama_barang_entry.get(),
                        int(jumlah_barang_spinbox.get()),
                        int(harga_awal_spinbox.get()),
                        int(harga_jual_spinbox.get()),
                        tanggal.get_date(), 
                        ukuran_combobox.get() if len(ukuran_combobox.get()) > 0 else None,
                    )
                    dissmiss()
                    refresh_barang()

            else:
                messagebox.showwarning("Warning !", "Harap lengkapi seluruh data !")

        def dissmiss():
            main_window.grab_release()
            main_window.destroy()

        main_window = tk.Toplevel(parent)
        main_window.title("Stok")
        main_window.geometry(
            f"300x200+{parent.winfo_screenwidth()//2 - 150}+{parent.winfo_screenheight()//2 - 200}"
        )
        main_window.resizable(tk.FALSE, tk.FALSE)
        main_window.wm_protocol("WM_DELETE_WINDOW", dissmiss)
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
        main_frame.rowconfigure(7, weight=1)

        nama_barang_entry = ttk.Entry(main_frame, font=("Arial", 12, "normal"))
        jumlah_barang_spinbox = ttk.Spinbox(main_frame, from_=1, to=100_000)
        harga_awal_spinbox = ttk.Spinbox(main_frame, from_=1, to=10_000_000_000)
        harga_jual_spinbox = ttk.Spinbox(main_frame, from_=1, to=20_000_000_000)
        konfirmasi_button = ttk.Button(
            main_frame,
            text="Konfirmasi",
            style="blue.TButton",
            command=lambda: konfirmasi(),
        )
        ukuran_combobox = ttk.Combobox(main_frame, values=list(map(lambda x: x.value, Size.__iter__())), state='readonly')
        tanggal = tkc.DateEntry(main_frame)

        ttk.Label(main_frame, text="Nama Barang", font=("Arial", 12, "normal")).grid(
            column=1, row=1, sticky=tk.NSEW
        )
        ttk.Label(main_frame, text="Jumlah", font=("Arial", 12, "normal")).grid(
            column=1, row=2, sticky=tk.NSEW
        )
        ttk.Label(main_frame, text="Harga Beli", font=("Arial", 12, "normal")).grid(
            column=1, row=3, sticky=tk.NSEW
        )
        ttk.Label(main_frame, text="Harga Jual", font=("Arial", 12, "normal")).grid(
            column=1, row=4, sticky=tk.NSEW
        )
        ttk.Label(main_frame, text="Ukuran", font=("Arial", 12, "normal")).grid(
            column=1, row=5, sticky=tk.NSEW
        )
        ttk.Label(main_frame, text="Tanggal", font=("Arial", 12, "normal")).grid(
            column=1, row=6, sticky=tk.NSEW
        )
        nama_barang_entry.grid(column=2, row=1, sticky=tk.NSEW, padx=2, pady=4)
        jumlah_barang_spinbox.grid(column=2, row=2, sticky=tk.NSEW, padx=2, pady=4)
        harga_awal_spinbox.grid(column=2, row=3, sticky=tk.NSEW, padx=2, pady=4)
        harga_jual_spinbox.grid(column=2, row=4, sticky=tk.NSEW, padx=2, pady=4)
        konfirmasi_button.grid(
            column=1, columnspan=2, row=7, sticky=tk.NSEW, padx=2, pady=4
        )
        ukuran_combobox.grid(column=2, row=5, sticky=tk.NSEW, padx=2, pady=4)
        tanggal.grid(column=2, row=6, sticky=tk.NSEW)

        nama_barang_entry.focus()
        nama_barang_entry.bind("<Return>", lambda e: jumlah_barang_spinbox.focus())
        jumlah_barang_spinbox.bind("<Return>", lambda e: harga_awal_spinbox.focus())
        harga_awal_spinbox.bind("<Return>", lambda e: harga_jual_spinbox.focus())
        harga_jual_spinbox.bind("<Return>", lambda e: ukuran_combobox.focus())
        ukuran_combobox.bind("<Return>", lambda e: tanggal.focus())
        tanggal.bind("<Return>", lambda e: konfirmasi_button.invoke())

    def tambah_stok_barang_klik():
        def konfirmasi():
            jumlah_tambah = int(jumlah_tambah_spinbox.get())
            if jumlah_tambah > 0:
                tambah_stok_barang(int(treeview_barang.selection()[0]), jumlah_tambah, tanggal_1.get_date())
                refresh_barang()
                dissmiss()
            else:
                messagebox.showwarning(
                    "Warning !", "Jumlah tambah harus lebih dari 0 !"
                )

        def dissmiss():
            main_window.grab_release()
            main_window.destroy()

        main_window = tk.Toplevel(parent)
        main_window.title("Pembelian")
        main_window.geometry(
            f"260x100+{parent.winfo_screenwidth()//2 - 130}+{parent.winfo_screenheight()//2 - 25}"
        )
        main_window.resizable(tk.FALSE, tk.FALSE)
        main_window.wm_protocol("WM_DELETE_WINDOW", dissmiss)
        main_window.wait_visibility()
        main_window.grab_set()
        main_window.columnconfigure(1, weight=1)
        main_window.rowconfigure(1, weight=1)

        main_frame = ttk.Frame(main_window)
        main_frame.grid(column=1, row=1, sticky=tk.NSEW)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)
        main_frame.rowconfigure(5, weight=1)

        ttk.Label(
            main_frame, text="Jumlah: ", justify=tk.CENTER, anchor=tk.CENTER
        ).grid(column=1, row=1, sticky=tk.NSEW)
        jumlah_tambah_spinbox = ttk.Spinbox(main_frame, from_=1, to=100_000)
        tanggal_1 = tkc.DateEntry(main_frame)
        tanggal_1.grid(column=1, row=4, sticky=tk.NSEW)
        ttk.Label(
            main_frame, text="Tanggal: ", justify=tk.CENTER, anchor=tk.CENTER
        ).grid(column=1, row=3, sticky=tk.NSEW)
        jumlah_tambah_spinbox.set(1)
        jumlah_tambah_spinbox.focus()
        jumlah_tambah_spinbox.grid(column=1, row=2, sticky=tk.NSEW)
        jumlah_tambah_spinbox.bind("<Return>", lambda e: tanggal_1.focus())
        tanggal_1.bind("<Return>", lambda e: tombol_konfirmasi.invoke())
        tombol_konfirmasi = ttk.Button(
            main_frame,
            text="Konfirmasi",
            style="blue.TButton",
            command=lambda: konfirmasi(),
        )
        tombol_konfirmasi.grid(column=1, row=5, sticky=tk.NSEW)

    def hapus_barang_klik():
        if messagebox.askokcancel(
            "Warning !",
            "Apakah anda yakin ingin menghapus barang ini ? (Barang yang bisa dihapus hanya barang yang belum pernah dibeli. )",
        ):
            if hapus_barang(int(treeview_barang.selection()[0])):
                messagebox.showerror(
                    "Error !",
                    "Barang tidak bisa dihapus karena sudah pernah dibeli !",
                )
        refresh_barang()


    def refresh_barang():
        global himpunan_barang
        himpunan_barang = muat_barang()
        treeview_barang.delete(*treeview_barang.get_children())
        for barang in himpunan_barang:
            treeview_barang.insert(
                "",
                "end",
                iid=str(barang.id),
                values=(
                    barang.nama_barang,
                    barang.ukuran, 
                    f"{barang.tersedia_saat_ini}/{barang.tersedia}",
                    crud.angka_mudah_dibaca(barang.modal),
                    crud.angka_mudah_dibaca(barang.harga_jual),
                ),
            )
        hapus_barang_button.state(["disabled"])
        tambah_stok_barang_button.state(["disabled"])


    ttk.Label(sub_frame_1, text="Barang", font=("Arial", 14, "bold")).grid(
        column=1, row=1, sticky=tk.NSEW, padx=4, pady=6
    )

    treeview_barang.heading("nama_barang", text="Nama Barang")
    treeview_barang.heading("tersedia", text="Tersedia")
    treeview_barang.heading("modal", text="Harga Beli")
    treeview_barang.heading("harga_jual", text="Harga Jual")
    treeview_barang.heading("ukuran", text="Ukuran")
    treeview_barang.configure(yscrollcommand=scrollbar_barang.set)
    treeview_barang.grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    scrollbar_barang.grid(column=2, row=1, sticky=tk.NS)
    treeview_barang.bind(
        "<<TreeviewSelect>>",
        lambda e: [
            hapus_barang_button.state(["!disabled"]),
            tambah_stok_barang_button.state(["!disabled"]),
        ]
        if len(treeview_barang.selection()) > 0
        else [],
    )


    tambah_barang_baru_button.grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    tambah_stok_barang_button.grid(column=2, row=1, sticky=tk.NSEW, padx=4, pady=6)
    refresh_barang_button.grid(column=3, row=1, sticky=tk.NSEW, padx=4, pady=6)
    hapus_barang_button.grid(column=5, row=1, sticky=tk.NSEW, padx=4, pady=6)


    sub_frame_1.grid(column=1, row=1, sticky=tk.NSEW)
    sub_frame_2.grid(column=1, row=2, sticky=tk.NSEW)
    sub_frame_3.grid(column=1, row=3, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=10)
    main_frame.rowconfigure(3, weight=1)
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

    refresh_barang()
    return main_frame


@get_db
def muat_barang(db: Session):
    return crud.ambil_barang(db)


@get_db
def tambah_barang_baru(
    db: Session,
    nama_barang: str,
    tersedia: int,
    modal: int,
    harga_jual: int,
    tanggal: datetime.date, 
    ukuran: str, 
):
    crud.tambah_barang(db, nama_barang, tersedia, modal, harga_jual, tanggal, ukuran)


@get_db
def tambah_stok_barang(db: Session, id_barang: int, jumlah_tambah: int, tanggal: datetime.date):
    crud.tambah_stok_barang(db, id_barang, jumlah_tambah, tanggal)


@get_db
def hapus_barang(db: Session, id_barang: int):
    return crud.hapus_barang(db, id_barang)
