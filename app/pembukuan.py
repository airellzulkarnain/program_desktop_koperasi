import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
import calendar
import crud


def pembukuan(parent: ttk.Notebook):
    global himpunan_pembukuan
    main_frame = ttk.Frame(parent)
    main_frame.grid(column=1, row=1, sticky=tk.NSEW)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)
    main_frame.rowconfigure(3, weight=1)
    main_frame.rowconfigure(4, weight=38)
    main_frame.rowconfigure(5, weight=1)
    main_frame.rowconfigure(6, weight=1)

    sub_frame_1 = ttk.Frame(main_frame)
    sub_frame_2 = ttk.Frame(main_frame)
    sub_frame_3 = ttk.Frame(main_frame)
    sub_frame_4 = ttk.Frame(main_frame)
    sub_frame_5 = ttk.Frame(main_frame)
    sub_frame_6 = ttk.Frame(main_frame)

    sub_frame_1.grid(column=1, row=1, sticky=tk.NSEW)
    sub_frame_2.grid(column=1, row=2, sticky=tk.NSEW)
    sub_frame_3.grid(column=1, row=3, sticky=tk.NSEW)
    sub_frame_4.grid(column=1, row=4, sticky=tk.NSEW)
    sub_frame_5.grid(column=1, row=5, sticky=tk.NSEW)
    sub_frame_6.grid(column=1, row=6, sticky=tk.NSEW)

    sub_frame_1.columnconfigure(1, weight=1)
    sub_frame_1.rowconfigure(1, weight=1)
    sub_frame_2.columnconfigure(1, weight=1)
    sub_frame_2.columnconfigure(2, weight=5)
    sub_frame_2.columnconfigure(3, weight=1)
    sub_frame_2.columnconfigure(4, weight=4)
    sub_frame_2.columnconfigure(5, weight=1)
    sub_frame_2.columnconfigure(6, weight=1)
    sub_frame_2.columnconfigure(7, weight=1)
    sub_frame_2.rowconfigure(1, weight=1)
    sub_frame_3.columnconfigure(1, weight=1)
    sub_frame_3.columnconfigure(2, weight=1)
    sub_frame_3.columnconfigure(3, weight=22)
    sub_frame_3.rowconfigure(1, weight=1)
    sub_frame_4.columnconfigure(1, weight=1)
    sub_frame_4.rowconfigure(1, weight=1)
    sub_frame_5.columnconfigure(1, weight=11)
    sub_frame_5.columnconfigure(2, weight=1)
    sub_frame_5.rowconfigure(1, weight=1)
    sub_frame_6.columnconfigure(1, weight=1)
    sub_frame_6.columnconfigure(2, weight=1)
    sub_frame_6.columnconfigure(3, weight=1)
    sub_frame_6.columnconfigure(4, weight=20)
    sub_frame_6.columnconfigure(5, weight=1)
    sub_frame_6.rowconfigure(1, weight=1)

    ttk.Label(sub_frame_1, text="Biaya - Biaya", font=("Arial", 14, "bold")).grid(
        column=1, row=1, sticky=tk.NSEW
    )
    ttk.Label(sub_frame_2, text="Keterangan", font=("Arial", 12, "normal")).grid(
        column=1, row=1, sticky=tk.EW, padx=4, pady=6
    )
    ttk.Label(sub_frame_2, text="Nominal", font=("Arial", 12, "normal")).grid(
        column=3, row=1, sticky=tk.EW, padx=4, pady=6
    )
    ttk.Label(sub_frame_3, text="Pembukuan", font=("Arial", 14, "bold")).grid(
        column=1, row=1, sticky=tk.NSEW
    )
    ttk.Button(
        sub_frame_3, text="Refresh...", command=lambda: refresh_pembukuan()
    ).grid(column=2, row=1, sticky=tk.NSEW, padx=4, pady=6)

    keterangan_biaya_entry = ttk.Entry(sub_frame_2, font=("Arial", 12, "normal"))
    keterangan_biaya_entry.grid(column=2, row=1, sticky=tk.EW, padx=4, pady=6)
    nominal_biaya_spinbox = ttk.Spinbox(sub_frame_2, from_=500, to=10_000_000_000)
    nominal_biaya_spinbox.grid(column=4, row=1, sticky=tk.EW, padx=4, pady=6)
    debit_kredit = tk.StringVar()
    ttk.Radiobutton(
        sub_frame_2, text="Debit", value="debit", variable=debit_kredit
    ).grid(column=5, row=1, sticky=tk.EW, padx=4, pady=6)
    ttk.Radiobutton(
        sub_frame_2, text="Kredit", value="kredit", variable=debit_kredit
    ).grid(column=6, row=1, sticky=tk.EW, padx=4, pady=6)
    biaya_button = ttk.Button(
        sub_frame_2, text="Tambah", style="green.TButton", command=lambda: biaya_klik()
    )
    biaya_button.grid(column=7, row=1, sticky=tk.EW, padx=4, pady=6)

    pembukuan_treeview = ttk.Treeview(
        sub_frame_4,
        columns=("tanggal", "uraian", "debit", "kredit", "saldo"),
        show="headings",
    )
    pembukuan_treeview.heading("tanggal", text="Tanggal")
    pembukuan_treeview.column("tanggal", width=30)
    pembukuan_treeview.heading("uraian", text="Keterangan")
    pembukuan_treeview.column("uraian", width=360)
    pembukuan_treeview.heading("debit", text="Debit")
    pembukuan_treeview.heading("kredit", text="Kredit")
    pembukuan_treeview.heading("saldo", text="Saldo")
    pembukuan_treeview.grid(column=1, row=1, sticky=tk.NSEW)

    pembukuan_scrollbar = ttk.Scrollbar(
        sub_frame_4, orient=tk.VERTICAL, command=pembukuan_treeview.yview
    )
    pembukuan_scrollbar.grid(column=2, row=1, sticky=tk.NS)
    pembukuan_treeview.configure(yscrollcommand=pembukuan_scrollbar.set)

    cari_pembukuan_entry = ttk.Entry(sub_frame_5, font=("Arial", 12, "normal"))
    cari_pembukuan_entry.bind("<Return>", lambda e: cari_pembukuan_button.invoke())
    cari_pembukuan_button = ttk.Button(
        sub_frame_5,
        text="Cari",
        style="blue.TButton",
        command=lambda: cari_pembukuan_klik(),
    )
    cari_pembukuan_entry.grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    cari_pembukuan_button.grid(column=2, row=1, sticky=tk.NSEW, padx=4, pady=6)

    range_pembukuan = tk.StringVar()
    ttk.Radiobutton(
        sub_frame_6, text="Bulan", variable=range_pembukuan, value="0"
    ).grid(column=1, row=1, sticky=tk.NSEW, padx=4, pady=6)
    ttk.Radiobutton(
        sub_frame_6, text="Tahun", variable=range_pembukuan, value="1"
    ).grid(column=2, row=1, sticky=tk.NSEW, padx=4, pady=6)
    # ttk.Radiobutton(sub_frame_6, text='Custom', variable=range_pembukuan, value='2').grid(column=3, row=1, sticky=tk.NSEW, padx=4, pady=6)
    buat_laporan_button = ttk.Button(
        sub_frame_6,
        text="Buat Laporan",
        style="blue.TButton",
        command=lambda: buat_laporan_klik(),
    )
    buat_laporan_button.grid(column=5, row=1, sticky=tk.NSEW, padx=4, pady=6)

    def refresh_pembukuan():
        global himpunan_pembukuan
        himpunan_pembukuan = ambil_pembukuan()
        pembukuan_treeview.delete(*pembukuan_treeview.get_children())
        for pembukuan in himpunan_pembukuan:
            pembukuan_treeview.insert(
                "",
                "end",
                values=(
                    pembukuan.tanggal.date(),
                    pembukuan.uraian,
                    "Rp. " + crud.angka_mudah_dibaca(pembukuan.debit),
                    "Rp. " + crud.angka_mudah_dibaca(pembukuan.kredit),
                    "Rp. " + crud.angka_mudah_dibaca(pembukuan.saldo),
                ),
            )

    def biaya_klik():
        if messagebox.askokcancel(
            "Warning !",
            "Pastikan seluruh data sudah lengkap dan benar ! Setelah ini data tidak dapat dihapus dari pembukuan !",
            icon=messagebox.WARNING,
        ):
            if (
                len(keterangan_biaya_entry.get()) > 0
                and int(nominal_biaya_spinbox.get()) > 0
                and len(debit_kredit.get()) > 0
            ):
                if debit_kredit.get() == "debit":
                    biaya_tambahan(
                        keterangan_biaya_entry.get(),
                        debit=int(nominal_biaya_spinbox.get()),
                    )
                elif debit_kredit.get() == "kredit":
                    biaya_tambahan(
                        keterangan_biaya_entry.get(),
                        kredit=int(nominal_biaya_spinbox.get()),
                    )
                keterangan_biaya_entry.delete(0, len(keterangan_biaya_entry.get()))
                nominal_biaya_spinbox.set(0)
                debit_kredit.set("")
                refresh_pembukuan()
            else:
                messagebox.showwarning("Warning !", "Harap lengkapi seluruh data !")

    def buat_laporan_klik():
        def dismiss():
            main.grab_release()
            main.destroy()

        main = tk.Toplevel(parent)
        main.title("Buat Laporan")
        main.geometry(
            f"300x200+{parent.winfo_screenwidth()//2-150}+{parent.winfo_screenheight()//2-100}"
        )
        main.resizable(tk.FALSE, tk.FALSE)
        main.wm_protocol("WM_DELETE_WINDOW", dismiss)
        main.wait_visibility()
        main.grab_set()
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)
        main_frame = ttk.Frame(main)
        main_frame.grid(column=1, row=1, sticky=tk.NSEW)
        if range_pembukuan.get() == "0":

            def buat():
                if int(bulan_spinbox.get()) > 0 and int(tahun_spinbox.get()) > 0:
                    buat_laporan(
                        int(range_pembukuan.get()),
                        nama_sekolah_entry.get(),
                        filedialog.askdirectory(title="Pilih Folder"),
                        bulan=int(bulan_spinbox.get()),
                        tahun=int(tahun_spinbox.get()),
                    )
                    dismiss()

            nama_sekolah_entry = ttk.Entry(main_frame)
            ttk.Label(main_frame, text="Bulan").grid(
                column=1, row=1, sticky=tk.NSEW, padx=4, pady=6
            )
            ttk.Label(main_frame, text="Tahun").grid(
                column=2, row=1, sticky=tk.NSEW, padx=4, pady=6
            )
            bulan_spinbox = ttk.Spinbox(main_frame, from_=1, to=12)
            tahun_spinbox = ttk.Spinbox(main_frame, from_=2022, to=2100)
            ttk.Label(main_frame, text="Instansi: ").grid(
                column=1, columnspan=2, row=3, sticky=tk.NSEW, padx=4, pady=6
            )
            nama_sekolah_entry.grid(
                column=1, columnspan=2, row=4, sticky=tk.NSEW, padx=4, pady=6
            )
            bulan_spinbox.grid(column=1, row=2, sticky=tk.NSEW, padx=4, pady=6)
            tahun_spinbox.grid(column=2, row=2, sticky=tk.NSEW, padx=4, pady=6)
            buat_button = ttk.Button(
                main_frame, text="Buat", style="blue.TButton", command=lambda: buat()
            )
            buat_button.grid(
                column=1, columnspan=2, row=5, sticky=tk.NSEW, padx=4, pady=6
            )
            main_frame.columnconfigure(1, weight=1)
            main_frame.columnconfigure(2, weight=1)
            main_frame.rowconfigure(1, weight=1)
            main_frame.rowconfigure(2, weight=1)
            main_frame.rowconfigure(3, weight=1)
            main_frame.rowconfigure(4, weight=1)
            main_frame.rowconfigure(5, weight=1)
        elif range_pembukuan.get() == "1":

            def buat():
                if int(tahun_spinbox.get()) > 0:
                    buat_laporan(
                        int(range_pembukuan.get()),
                        nama_sekolah_entry.get(),
                        filedialog.askdirectory(title="Pilih Folder"),
                        tahun=int(tahun_spinbox.get()),
                    )
                    dismiss()

            nama_sekolah_entry = ttk.Entry(main_frame)
            ttk.Label(main_frame, text="Tahun").grid(column=1, row=1, sticky=tk.NSEW)
            tahun_spinbox = ttk.Spinbox(main_frame, from_=2022, to=2100)
            buat_button = ttk.Button(main_frame, text="Buat")
            ttk.Label(main_frame, text="Instansi: ").grid(
                column=1, row=3, sticky=tk.NSEW, padx=4, pady=6
            )
            nama_sekolah_entry.grid(column=1, row=4, sticky=tk.NSEW, padx=4, pady=6)
            tahun_spinbox.grid(column=1, row=2, sticky=tk.NSEW, padx=4, pady=6)
            buat_button = ttk.Button(
                main_frame, text="Buat", style="blue.TButton", command=lambda: buat()
            )
            buat_button.grid(column=1, row=5, sticky=tk.NSEW, padx=4, pady=6)

            main_frame.columnconfigure(1, weight=1)
            main_frame.rowconfigure(1, weight=1)
            main_frame.rowconfigure(2, weight=1)
            main_frame.rowconfigure(3, weight=1)
            main_frame.rowconfigure(4, weight=1)
            main_frame.rowconfigure(5, weight=1)

    def cari_pembukuan_klik():
        global himpunan_pembukuan
        pembukuan_treeview.delete(*pembukuan_treeview.get_children())
        for pembukuan in filter(
            lambda pembukuan: cari_pembukuan_entry.get().lower()
            in (str(pembukuan.tanggal) + pembukuan.uraian).lower(),
            himpunan_pembukuan,
        ):
            pembukuan_treeview.insert(
                "",
                "end",
                values=(
                    pembukuan.tanggal.date(),
                    pembukuan.uraian,
                    "Rp. " + crud.angka_mudah_dibaca(pembukuan.debit),
                    "Rp. " + crud.angka_mudah_dibaca(pembukuan.kredit),
                    "Rp. " + crud.angka_mudah_dibaca(pembukuan.saldo),
                ),
            )

    refresh_pembukuan()

    return main_frame


@get_db
def ambil_pembukuan(db: Session):
    return crud.ambil_pembukuan(db)


@get_db
def biaya_tambahan(db: Session, uraian: str, debit: int = 0, kredit: int = 0):
    crud.biaya_tambahan(db, uraian, debit, kredit)


@get_db
def buat_laporan(
    db: Session,
    range_: int,
    sekolah: str,
    dir_loc: str,
    bulan: int | None = None,
    tahun: int | None = None,
    dari: datetime | None = None,
    sampai: datetime | None = None,
):
    crud.buat_laporan(db, range_, sekolah, dir_loc, bulan, tahun, dari, sampai)
