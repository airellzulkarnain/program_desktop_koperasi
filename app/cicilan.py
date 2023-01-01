import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy.orm import Session
from database import get_db
import crud


def cicilan(parent: ttk.Notebook):
    global himpunan_siswa, himpunan_cicilan, himpunan_barang
    main_frame = ttk.Frame(parent)
    sub_frame_1 = ttk.Frame(main_frame)
    sub_frame_2 = ttk.Frame(main_frame)
    harga_barang = tk.StringVar()
    cicilan_canvas = tk.Canvas(
        sub_frame_1, bg="white", width=parent.winfo_screenwidth() // 2 + 160
    )
    cicilan_scrollbar = ttk.Scrollbar(
        sub_frame_1, orient=tk.VERTICAL, command=cicilan_canvas.yview
    )
    cari_cicilan_entry = ttk.Entry(sub_frame_1, font=("Arial", 12, "normal"))
    cari_cicilan_button = ttk.Button(
        sub_frame_1,
        text="Cari",
        style="blue.TButton",
        command=lambda: cari_cicilan_klik(),
    )
    siswa_canvas = tk.Canvas(sub_frame_2, bg="white")
    siswa_scrollbar = ttk.Scrollbar(
        sub_frame_2, orient=tk.VERTICAL, command=siswa_canvas.yview
    )
    cari_siswa_entry = ttk.Entry(sub_frame_2, font=("Arial", 12, "normal"))
    cari_siswa_button = ttk.Button(
        sub_frame_2,
        text="Cari",
        style="blue.TButton",
        command=lambda: cari_siswa_klik(),
    )
    pilih_semua = tk.IntVar()
    pilih_semua_checkbutton = ttk.Checkbutton(
        sub_frame_2,
        text="Pilih Semuanya. ",
        variable=pilih_semua,
        command=lambda: pilih_semua_klik(),
        style="pilihsemua.TCheckbutton",
    )
    pilih_barang_combobox = ttk.Combobox(sub_frame_2)
    kali_bayar_spinbox = ttk.Spinbox(sub_frame_2, state="readonly")
    konfirmasi_button = ttk.Button(
        sub_frame_2,
        text="Konfirmasi",
        style="green.TButton",
        command=lambda: konfirmasi_klik(),
    )

    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=10)
    main_frame.columnconfigure(2, weight=2)
    main_frame.rowconfigure(1, weight=1)
    sub_frame_1.grid(column=1, row=1, sticky=tk.NSEW)
    sub_frame_1.rowconfigure(1, weight=2)
    sub_frame_1.rowconfigure(2, weight=45)
    sub_frame_1.rowconfigure(3, weight=1)
    sub_frame_1.columnconfigure(1, weight=1)
    sub_frame_2.columnconfigure(2, weight=1)
    sub_frame_2.grid(column=2, row=1, sticky=tk.NSEW)
    sub_frame_2.rowconfigure(1, weight=2)
    sub_frame_2.rowconfigure(2, weight=21)
    sub_frame_2.rowconfigure(3, weight=1)
    sub_frame_2.rowconfigure(4, weight=1)
    sub_frame_2.rowconfigure(5, weight=1)
    sub_frame_2.rowconfigure(6, weight=1)
    sub_frame_2.rowconfigure(7, weight=1)
    sub_frame_2.columnconfigure(1, weight=1)
    sub_frame_2.columnconfigure(2, weight=5)
    sub_frame_2.columnconfigure(3, weight=1)
    sub_frame_2.columnconfigure(4, weight=5)

    ttk.Label(sub_frame_1, text="Cicilan", font=("Arial", 14, "bold")).grid(
        column=1, row=1, sticky=tk.NSEW
    )
    ttk.Label(sub_frame_2, text="Tambah Cicilan", font=("Arial", 14, "bold")).grid(
        column=1, columnspan=3, row=1, sticky=tk.NSEW
    )
    ttk.Button(
        sub_frame_2,
        text="Refresh...",
        command=lambda: [refresh_barang(), refresh_siswa()],
    ).grid(column=4, columnspan=2, row=1, sticky=tk.NSEW, padx=4, pady=6)
    ttk.Label(sub_frame_2, text="Barang", font=("Arial", 12, "normal")).grid(
        column=1, row=5, sticky=tk.NSEW, padx=4, pady=6
    )
    ttk.Label(sub_frame_2, text="Kali Bayar", font=("Arial", 12, "normal")).grid(
        column=3, row=5, sticky=tk.NSEW, padx=4, pady=6
    )
    harga_barang.set("Harga Barang: Rp. 0")
    ttk.Label(sub_frame_2, textvariable=harga_barang, font=("Arial", 12, "bold")).grid(
        column=1, columnspan=5, row=6, sticky=tk.NSEW, padx=4, pady=6
    )

    cicilan_canvas.grid(column=1, columnspan=2, row=2, sticky=tk.NS, padx=4, pady=6)
    cicilan_scrollbar.grid(column=3, row=2, sticky=tk.NSEW, pady=6)
    cicilan_canvas.configure(yscrollcommand=cicilan_scrollbar.set)
    cari_cicilan_entry.grid(column=1, row=3, sticky=tk.NSEW, padx=4, pady=6)
    cari_cicilan_button.grid(
        column=2, columnspan=2, row=3, sticky=tk.NSEW, padx=4, pady=6
    )
    siswa_canvas.grid(column=1, columnspan=4, row=2, sticky=tk.NSEW, padx=4, pady=6)
    siswa_scrollbar.grid(column=5, row=2, sticky=tk.NSEW, pady=6)
    siswa_canvas.configure(yscrollcommand=siswa_scrollbar.set)

    cari_siswa_entry.grid(
        column=1, columnspan=3, row=3, sticky=tk.NSEW, padx=4, pady=10
    )
    cari_siswa_button.grid(
        column=4, columnspan=2, row=3, sticky=tk.NSEW, padx=4, pady=10
    )
    pilih_semua_checkbutton.grid(
        column=1, columnspan=5, row=4, sticky=tk.NSEW, padx=4, pady=6
    )
    pilih_barang_combobox.grid(column=2, row=5, sticky=tk.NSEW, padx=4, pady=6)
    kali_bayar_spinbox.grid(
        column=4, columnspan=2, row=5, sticky=tk.NSEW, padx=4, pady=6
    )
    konfirmasi_button.grid(
        column=1, columnspan=5, row=7, sticky=tk.NSEW, padx=4, pady=6
    )

    cari_siswa_entry.bind("<Return>", lambda e: cari_siswa_button.invoke())
    pilih_barang_combobox.bind("<<ComboboxSelected>>", lambda e: pilih_barang_changed())
    cari_cicilan_entry.bind("<Return>", lambda e: cari_cicilan_button.invoke())

    def panel_cicilan(
        siswa: str,
        kali_bayar: int,
        sudah_dibayar: int,
        harga_barang: int,
        id_cicilan: int,
        nama_barang: str,
    ) -> ttk.Frame:
        harga_dibayar = tk.StringVar()
        harga_dibayar.set("Total: Rp. -")
        frame = ttk.Frame(cicilan_canvas, borderwidth=1, relief=tk.SOLID)
        frame.columnconfigure(1, weight=5)
        frame.columnconfigure(2, weight=5)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)
        frame.rowconfigure(1, weight=3)
        frame.rowconfigure(2, weight=9)
        kali_pembayaran_spinbox = ttk.Spinbox(
            frame,
            from_=1,
            to=kali_bayar - sudah_dibayar,
            state="readonly",
            command=lambda: kali_pembayaran_changed(),
            width=3,
        )
        cicil_button = ttk.Button(
            frame, text="Bayar", command=lambda: cicil_klik(), style="blue.TButton"
        )
        kali_pembayaran_spinbox.grid(column=3, row=2, sticky=tk.NSEW, padx=4, pady=6)
        cicil_button.grid(column=4, row=2, sticky=tk.NSEW, padx=4, pady=6)
        ttk.Label(frame, text=siswa, font=("Arial", 12, "normal")).grid(
            column=1, columnspan=2, row=1, sticky=tk.NSEW, padx=4, pady=6
        )
        ttk.Label(frame, text=nama_barang, font=("Arial", 12, "normal"), width=24).grid(
            column=1, row=2, sticky=tk.NSEW, padx=4, pady=6
        )
        ttk.Label(
            frame, textvariable=harga_dibayar, font=("Arial", 12, "normal"), width=24
        ).grid(column=2, row=2, sticky=tk.NSEW, padx=4, pady=6)
        ttk.Label(
            frame,
            text=f"{sudah_dibayar}/{kali_bayar}",
            font=("Arial", 12, "normal"),
            justify=tk.RIGHT,
            anchor=tk.E,
        ).grid(column=4, row=1, sticky=tk.NSEW, padx=4, pady=6)

        def kali_pembayaran_changed():
            harga_dibayar.set(
                "Total: Rp. "
                + crud.angka_mudah_dibaca(
                    sum(
                        crud.bagi_pembayaran(harga_barang, kali_bayar)[
                            sudah_dibayar : sudah_dibayar
                            + int(kali_pembayaran_spinbox.get())
                        ]
                    )
                )
            )

        def cicil_klik():
            if messagebox.askokcancel("Info", "Lanjutkan Pembayaran cicilan ?"):
                bayar_cicilan(
                    id_cicilan, int(kali_pembayaran_spinbox.get()), harga_barang
                )
                refresh_barang()
                refresh_siswa()
                refresh_cicilan()

        return frame

    def refresh_siswa():
        global himpunan_siswa
        himpunan_siswa = dict()
        siswa_canvas.delete("all")
        siswa_canvas.update_idletasks()
        height = 20
        width = siswa_canvas.winfo_width() - 8
        counter = 0
        for siswa in ambil_siswa():
            text = "NISN: " + siswa.nisn + ", " + siswa.nama + " " + siswa.kelas
            himpunan_siswa.update({text: tk.IntVar()})
            siswa_canvas.create_window(
                4,
                6 + counter * (height + 6),
                anchor=tk.NW,
                window=ttk.Checkbutton(
                    siswa_canvas,
                    text=text,
                    variable=himpunan_siswa[text],
                    command=lambda: siswa_checkbutton_changed(text),
                    style="cicilan.TCheckbutton",
                ),
                width=width,
                height=height,
            )
            counter += 1
        siswa_canvas.configure(scrollregion=siswa_canvas.bbox("all"))

    def refresh_barang():
        global himpunan_barang
        himpunan_barang = ambil_barang()
        pilih_barang_combobox.configure(values=[key for key in himpunan_barang.keys()])
        pilih_barang_combobox.set("")
        harga_barang.set("Harga Barang: Rp. 0")
        kali_bayar_spinbox.set(0)

    def refresh_cicilan():
        global himpunan_cicilan
        himpunan_cicilan = ambil_cicilan()
        cicilan_canvas.delete("all")
        cicilan_canvas.update_idletasks()
        height = 80
        width = cicilan_canvas.winfo_width() - 14
        counter = 0
        for cicilan in himpunan_cicilan:
            cicilan_canvas.create_window(
                7,
                7 + counter * (height + 7),
                anchor=tk.NW,
                window=panel_cicilan(
                    cicilan.nama + " " + cicilan.kelas,
                    cicilan.kali_pembayaran,
                    cicilan.sudah_dibayar,
                    cicilan.harga_jual,
                    cicilan.id,
                    cicilan.nama_barang,
                ),
                width=width,
                height=height,
            )
            counter += 1
        cicilan_canvas.configure(scrollregion=cicilan_canvas.bbox("all"))

    def cari_cicilan_klik():
        global himpunan_cicilan
        cicilan_canvas.delete("all")
        cicilan_canvas.update_idletasks()
        height = 80
        width = cicilan_canvas.winfo_width() - 12
        counter = 0
        for cicilan in filter(
            lambda cicilan: cari_cicilan_entry.get().lower()
            in (
                cicilan.nama_barang + cicilan.nama + cicilan.kelas,
                himpunan_cicilan,
            ).lower()
        ):
            cicilan_canvas.create_window(
                7,
                6 + counter * (height + 6),
                anchor=tk.NW,
                window=panel_cicilan(
                    cicilan.nama + " " + cicilan.kelas,
                    cicilan.kali_pembayaran,
                    cicilan.sudah_dibayar,
                    cicilan.harga_jual,
                    cicilan.id,
                    cicilan.nama_barang,
                ),
                width=width,
                height=height,
            )
            counter += 1
        cicilan_canvas.configure(scrollregion=cicilan_canvas.bbox("all"))

    def cari_siswa_klik():
        global himpunan_siswa
        siswa_canvas.update_idletasks()
        height = 20
        width = siswa_canvas.winfo_width() - 8
        siswa_canvas.delete("all")
        counter = 0
        for siswa in filter(
            lambda siswa: cari_siswa_entry.get().lower() in siswa.lower(),
            himpunan_siswa.keys(),
        ):
            siswa_canvas.create_window(
                4,
                6 + counter * (height + 6),
                anchor=tk.NW,
                window=ttk.Checkbutton(
                    siswa_canvas,
                    text=siswa,
                    variable=himpunan_siswa[siswa],
                    command=lambda: siswa_checkbutton_changed(siswa),
                    style="cicilan.TCheckbutton",
                ),
                width=width,
                height=height,
            )
            counter += 1
        siswa_canvas.configure(scrollregion=siswa_canvas.bbox("all"))

    def konfirmasi_klik():
        global himpunan_siswa, himpunan_barang
        if any(himpunan_siswa.values()) and messagebox.askokcancel(
            "Warning !",
            "Anda yakin ingin menambahkan cicilan ? pastikan seluruh data sudah tepat !",
            icon=messagebox.WARNING,
        ):
            himpunan_nisn_siswa = [
                nisn.split(", ")[0].replace("NISN: ", "")
                for nisn, selected in himpunan_siswa.items()
                if selected.get() == 1
            ]
            tambah_cicilan(
                himpunan_nisn_siswa,
                himpunan_barang[pilih_barang_combobox.get()]["id"],
                int(kali_bayar_spinbox.get()),
            )
            refresh_cicilan()
            refresh_barang()
            refresh_siswa()
        else:
            messagebox.showwarning("Warning !", "Harap lengkapi seluruh data !")

    def pilih_barang_changed():
        global himpunan_barang
        kali_bayar_spinbox.configure(
            from_=1, to=int(himpunan_barang[pilih_barang_combobox.get()]["tersedia"])
        )
        kali_bayar_spinbox.set(1)
        harga_barang.set(
            "Harga Barang: Rp. "
            + crud.angka_mudah_dibaca(
                himpunan_barang[pilih_barang_combobox.get()]["harga"]
            )
        )

    def pilih_semua_klik():
        if pilih_semua.get():
            for key in himpunan_siswa.keys():
                himpunan_siswa[key].set(1)
        else:
            for key in himpunan_siswa.keys():
                himpunan_siswa[key].set(0)

    def siswa_checkbutton_changed(key: str):
        if all([bool(x.get()) for x in himpunan_siswa.values()]):
            pilih_semua.set(1)
        else:
            pilih_semua.set(0)

    refresh_siswa()
    refresh_barang()
    refresh_cicilan()
    return main_frame


@get_db
def ambil_cicilan(db: Session):
    return crud.ambil_cicilan(db)


@get_db
def ambil_barang(db: Session):
    himpunan_barang: dict = dict()
    for barang in crud.ambil_barang(db, True):
        if barang.tersedia_saat_ini > 0:
            himpunan_barang.update(
                {
                    barang.nama_barang: {
                        "harga": barang.harga_jual,
                        "tersedia": barang.tersedia_saat_ini,
                        "id": barang.id,
                    }
                }
            )
    return himpunan_barang


@get_db
def ambil_siswa(db: Session):
    return crud.ambil_siswa(db)


@get_db
def tambah_cicilan(
    db: Session, himpunan_nisn_siswa: list, id_barang: int, kali_pembayaran: int
):
    crud.tambah_cicilan(db, himpunan_nisn_siswa, id_barang, kali_pembayaran)


@get_db
def bayar_cicilan(db: Session, id_cicilan: int, kali_bayar: int, harga_barang: int):
    crud.bayar_cicilan(db, id_cicilan, kali_bayar, harga_barang)
