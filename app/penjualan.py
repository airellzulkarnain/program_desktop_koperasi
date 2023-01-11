import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy.orm import Session
from database import get_db
import crud


def penjualan(parent: ttk.Notebook):
    global himpunan_barang
    global total_harga_value
    global kredit_tunai
    kredit_tunai = tk.StringVar()
    himpunan_barang = muat_barang()
    himpunan_jual: list = []
    total_harga = tk.StringVar()
    total_harga_value = 0
    total_harga.set("Total Harga: Rp. 0")
    harga = tk.StringVar()
    main_frame = ttk.Frame(parent)
    sub_frame_1 = ttk.Frame(main_frame)
    sub_frame_2 = ttk.Frame(main_frame)
    sub_frame_3 = ttk.Frame(main_frame)
    sub_frame_4 = ttk.Frame(main_frame)
    konfirmasi_button = ttk.Button(
        sub_frame_4,
        text="Konfirmasi",
        command=lambda: konfirmasi(),
        style="green.TButton",
    )
    batalkan_button = ttk.Button(
        sub_frame_4,
        text="Batalkan",
        command=lambda: batalkan(),
        state="disabled",
        style="red.TButton",
    )
    treeview_jual = ttk.Treeview(
        sub_frame_3,
        columns=("barang", "jumlah", "harga_satuan", "total", "keterangan"),
        show="headings",
    )
    scrollbar_jual = ttk.Scrollbar(
        sub_frame_3, orient=tk.VERTICAL, command=treeview_jual.yview_scroll
    )
    pilih_barang_combobox = ttk.Combobox(
        sub_frame_1, values=[x for x in himpunan_barang.keys()]
    )
    jumlah_barang_spinbox = ttk.Spinbox(
        sub_frame_1, from_=0, to=0, command=lambda: spinbox_dipilih()
    )
    jumlah_barang_spinbox.set(0)
    tambah_button = ttk.Button(
        sub_frame_1, text="Tambah", command=lambda: tambah(), style="blue.TButton"
    )
    refresh_button = ttk.Button(
        sub_frame_1, text="Refresh...", command=lambda: refresh()
    )

    radio_button = ttk.Radiobutton(sub_frame_2, text='Tunai', variable=kredit_tunai, value='tunai')
    radio_button.grid(column=1, row=1)
    radio_button.invoke()
    ttk.Radiobutton(sub_frame_2, text='Kredit', variable=kredit_tunai, value='kredit').grid(column=2, row=1)

    def perbarui_harga():
        try:
            harga.set(
                "Harga: Rp. "
                + f"{crud.angka_mudah_dibaca(himpunan_barang[pilih_barang_combobox.get()]['harga'])}"
                + " x "
                + f"{jumlah_barang_spinbox.get()}"
                " (Rp. "
                + f"{crud.angka_mudah_dibaca(int(himpunan_barang[pilih_barang_combobox.get()]['harga'])*int(jumlah_barang_spinbox.get()))})"
            )
        except KeyError:
            harga.set("Harga: Rp. 0 x 0 (Rp. 0)")

    def combobox_dipilih(event):
        jumlah_barang_spinbox.configure(
            from_=1, to=himpunan_barang[pilih_barang_combobox.get()]["tersedia"]
        )
        jumlah_barang_spinbox.set(1)
        perbarui_harga()

    def spinbox_dipilih():
        perbarui_harga()

    def tambah():
        if int(himpunan_barang[pilih_barang_combobox.get()]["tersedia"]) < int(jumlah_barang_spinbox.get()):
            messagebox.showwarning('Warning !', f'Jumlah yang tersedia untuk {pilih_barang_combobox.get()} adalah{himpunan_barang[pilih_barang_combobox.get()]["tersedia"]}')
            refresh()
            return
        global total_harga_value
        total = int(himpunan_barang[pilih_barang_combobox.get()]["harga"]) * int(
            jumlah_barang_spinbox.get()
        )
        himpunan_jual.append(
            {
                "id_barang": himpunan_barang[pilih_barang_combobox.get()]["id"],
                "jumlah_terjual": int(jumlah_barang_spinbox.get()),
                "keterangan": kredit_tunai.get().capitalize()
            }
        )
        treeview_jual.insert(
            "",
            "end",
            values=(
                pilih_barang_combobox.get(),
                jumlah_barang_spinbox.get(),
                crud.angka_mudah_dibaca(
                    himpunan_barang[pilih_barang_combobox.get()]["harga"]
                ),
                crud.angka_mudah_dibaca(total),
                kredit_tunai.get()
            ),
        )
        himpunan_barang[pilih_barang_combobox.get()]["tersedia"] -= int(
            jumlah_barang_spinbox.get()
        )
        pilih_barang_combobox.set("")
        jumlah_barang_spinbox.configure(from_=0, to=0)
        jumlah_barang_spinbox.set(0)
        harga.set("Harga: Rp. 0 x 0 (Rp. 0)")
        radio_button.invoke()
        total_harga_value += total
        total_harga.set(
            "Total Harga: Rp. " + crud.angka_mudah_dibaca(total_harga_value)
        )
        batalkan_button.state(["!disabled"])

    def refresh():
        global himpunan_barang
        global total_harga_value
        treeview_jual.delete(*treeview_jual.get_children())
        total_harga.set("Total Harga: Rp. 0")
        harga.set("Harga: Rp. 0 x 0 (Rp. 0)")
        total_harga_value = 0
        himpunan_barang = muat_barang()
        pilih_barang_combobox.configure(values=[x for x in himpunan_barang.keys()])
        pilih_barang_combobox.set("")
        jumlah_barang_spinbox.configure(from_=0, to=0)
        jumlah_barang_spinbox.set(0)
        radio_button.invoke()
        himpunan_jual.clear()
        batalkan_button.state(["disabled"])

    def konfirmasi():
        if messagebox.askokcancel("Konfirmasi", "Apakah anda yakin ?"):
            for barang in himpunan_jual:
                jual(barang["id_barang"], barang["jumlah_terjual"], barang["keterangan"])
            refresh()

    def batalkan():
        if messagebox.askokcancel(
            "Batalkan", "Apakah anda yakin ?", icon=messagebox.WARNING
        ):
            refresh()

    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)
    main_frame.rowconfigure(3, weight=21)
    main_frame.rowconfigure(4, weight=1)
    sub_frame_1.grid(column=1, row=1, sticky=tk.EW)
    sub_frame_1.rowconfigure(1, weight=1)
    sub_frame_1.columnconfigure(1, weight=1)
    sub_frame_1.columnconfigure(2, weight=2)
    sub_frame_1.columnconfigure(3, weight=5)
    sub_frame_1.columnconfigure(4, weight=2)
    sub_frame_1.columnconfigure(5, weight=5)
    sub_frame_1.columnconfigure(6, weight=3)
    sub_frame_1.columnconfigure(7, weight=6)
    sub_frame_2.grid(column=1, row=2, sticky=tk.NSEW)
    sub_frame_3.columnconfigure(1, weight=1)
    sub_frame_3.rowconfigure(1, weight=1)
    sub_frame_4.rowconfigure(1, weight=1)
    sub_frame_4.columnconfigure(1, weight=6)
    sub_frame_4.columnconfigure(2, weight=2)
    sub_frame_4.columnconfigure(3, weight=2)
    refresh_button.grid(column=1, row=1, sticky=tk.NSEW, padx=6)
    ttk.Label(sub_frame_1, text="Barang", font=("Arial", 12, "normal")).grid(
        column=2, row=1, sticky=tk.EW, padx=6
    )
    ttk.Label(sub_frame_1, text="Jumlah", font=("Arial", 12, "normal")).grid(
        column=4, row=1, sticky=tk.EW, padx=6
    )
    ttk.Label(
        sub_frame_1,
        textvariable=harga,
        font=("Arial", 12, "normal"),
        justify="center",
        width=24,
    ).grid(column=7, row=1, sticky=tk.EW, padx=6)
    pilih_barang_combobox.grid(column=3, row=1, sticky=tk.EW, padx=6)
    jumlah_barang_spinbox.grid(column=5, row=1, sticky=tk.EW, padx=6)
    jumlah_barang_spinbox.bind('<KeyRelease>', lambda e: spinbox_dipilih())
    tambah_button.grid(column=6, row=1, sticky=tk.NSEW, padx=6)
    sub_frame_3.grid(column=1, row=3, sticky=tk.NSEW)
    sub_frame_4.grid(column=1, row=4, sticky=tk.NSEW)
    treeview_jual.grid(column=1, row=1, sticky=tk.NSEW)
    scrollbar_jual.grid(column=2, row=1, sticky=tk.NS)
    treeview_jual.configure(yscrollcommand=scrollbar_jual.set)
    treeview_jual.heading("barang", text="Barang")
    treeview_jual.heading("jumlah", text="Jumlah")
    treeview_jual.heading("harga_satuan", text="Harga Satuan")
    treeview_jual.heading("total", text="Total")
    treeview_jual.heading("keterangan", text="Keterangan")
    treeview_jual.column("barang", width=500)
    treeview_jual.column("jumlah", width=10)
    batalkan_button.grid(column=3, row=1, sticky=tk.NSEW, padx=6, pady=6)
    konfirmasi_button.grid(column=2, row=1, sticky=tk.NSEW, padx=6, pady=6)
    ttk.Label(
        sub_frame_4, textvariable=total_harga, font=("Arial", 14, "bold"), width=24
    ).grid(column=1, row=1, sticky=tk.NSEW, padx=6, pady=6)
    perbarui_harga()

    pilih_barang_combobox.bind("<<ComboboxSelected>>", combobox_dipilih)
    return main_frame


@get_db
def muat_barang(db: Session) -> dict:
    himpunan_barang: dict = dict()
    for barang in crud.ambil_barang(db):
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
def jual(db: Session, id_barang: int, jumlah_terjual: int, keterangan: str):
    crud.jual(db, id_barang, jumlah_terjual, keterangan)
