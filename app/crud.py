from sqlalchemy import select, update, delete, and_, func
from datetime import datetime
from sqlalchemy.orm import Session
from fpdf import FPDF
from models import *
import calendar as cld
import subprocess as sp


def buat_kunci_akses(db: Session):
    if not db.scalar(select(Access)):
        key = Access(key=ambil_uuid() * 2)
        db.add(key)
        db.commit()


def angka_mudah_dibaca(angka: str | int) -> str:
    angka = list(angka[::-1]) if isinstance(angka, str) else list(str(angka)[::-1])
    for i in range(len(angka)):
        angka[i] = angka[i] + "." if not (i + 1) % 3 else angka[i]
    angka[-1] = angka[-1].replace(".", "")
    return "".join(angka)[::-1]


def ambil_uuid():
    return (
        sp.check_output("wmic csproduct get UUID")
        .decode("utf-8")
        .split("\n")[1]
        .strip()
    )


def jual(db: Session, id_barang: int, jumlah_terjual: int, keterangan: str):
    barang = db.scalar(select(Barang).where(Barang.id == id_barang))
    if 0 < jumlah_terjual <= barang.tersedia_saat_ini:
        barang.tersedia_saat_ini -= jumlah_terjual
        saldo_terakhir = db.scalar(
            select(Pembukuan.saldo).where(Pembukuan.nama_barang == barang.nama_barang+' '+(barang.ukuran or '#')).order_by(Pembukuan.id.desc())
        )
        db.add(
            Pembukuan(
                nama_barang=barang.nama_barang+' '+(barang.ukuran or '#'), 
                keterangan=f'Penjualan {keterangan}', 
                kredit=jumlah_terjual, 
                saldo=saldo_terakhir - jumlah_terjual, 
            )
        )
        db.commit()


def ambil_barang(db: Session):
    return db.scalars(select(Barang)).all()


def ambil_pembukuan(db: Session):
    return db.scalars(select(Pembukuan).order_by(Pembukuan.nama_barang, Pembukuan.id)).all()


def tambah_barang(
    db: Session,
    nama_barang: str,
    tersedia: int,
    modal: int,
    harga_jual: int,
    tanggal: datetime.date,
    ukuran: str | None = None, 
):
    barang = Barang(
        nama_barang=nama_barang,
        tersedia=tersedia,
        tersedia_saat_ini=tersedia,
        modal=modal,
        harga_jual=harga_jual,
        ukuran=ukuran
    )
    db.add(barang)
    db.flush()
    db.add(
        Pembukuan(
            tanggal=tanggal, 
            nama_barang=barang.nama_barang + ' ' + (barang.ukuran or '#'), 
            keterangan=f'Saldo', 
            debit=tersedia,
            saldo=tersedia,
        )
    )
    db.commit()


def tambah_stok_barang(db: Session, id_barang: int, jumlah_tambah: int, tanggal: datetime.date):
    barang = db.scalar(select(Barang).where(Barang.id == id_barang))
    barang.tersedia_saat_ini += jumlah_tambah
    if barang.tersedia_saat_ini > barang.tersedia:
        barang.tersedia = barang.tersedia_saat_ini
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).where(Pembukuan.nama_barang == barang.nama_barang+' '+(barang.ukuran or '#')).order_by(Pembukuan.id.desc()))
    db.add(
        Pembukuan(
            tanggal=tanggal, 
            nama_barang=barang.nama_barang + ' ' + (barang.ukuran or '#'), 
            keterangan='Pembelian', 
            debit=jumlah_tambah,
            saldo=saldo_terakhir + jumlah_tambah,
        )
    )
    db.commit()


def hapus_barang(db: Session, id_barang: int):
    barang = db.scalar(select(Barang).where(Barang.id == id_barang))
    saldo_terakhir = (
        db.scalar(select(Pembukuan.saldo).where(Pembukuan.nama_barang == barang.nama_barang+' '+(barang.ukuran or '#')).order_by(Pembukuan.id.desc())) or 0.0
    )
    if (barang.tersedia == barang.tersedia_saat_ini):
        db.add(
            Pembukuan(
                nama_barang=barang.nama_barang + ' ' + (barang.ukuran or '#'), 
                keterangan='Hapus', 
                kredit=barang.tersedia,
                saldo=saldo_terakhir - barang.tersedia,
            )
        )
        db.delete(barang)
        db.commit()
    elif barang.tersedia_saat_ini == 0:
        db.add(
            Pembukuan(
                nama_barang=barang.nama_barang + ' ' + (barang.ukuran or '#'), 
                keterangan='Hapus', 
                saldo=saldo_terakhir,
            )
        )
        db.delete(barang)
        db.commit()
    else:
        return -1

# Bulan = 0, Tahun = 1
def buat_laporan(
    db: Session,
    range_: int,
    sekolah: str,
    dir_loc: str,
    bulan: int | None = None,
    tahun: int | None = None,
):
    if range_ == 0:  # Bulan
        himpunan_pembukuan = db.scalars(
            select(Pembukuan).where(
                and_(
                    Pembukuan.tanggal >= datetime(tahun, bulan, 1),
                    Pembukuan.tanggal
                    <= datetime(tahun, bulan, cld.monthrange(tahun, bulan)[1]),
                )
            ).order_by(Pembukuan.nama_barang, Pembukuan.id)
        ).all()
    elif range_ == 1:  # Tahun
        himpunan_pembukuan = db.scalars(
            select(Pembukuan).where(
                and_(
                    Pembukuan.tanggal >= datetime(tahun, 1, 1),
                    Pembukuan.tanggal <= datetime(tahun, 12, 31),
                )
            ).order_by(Pembukuan.nama_barang, Pembukuan.id)
        ).all()

    pdf = FPDF(orientation="P", unit="pt", format="A4")
    pdf.add_page()
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 16, sekolah.upper(), align="C")
    pdf.ln(16)
    pdf.set_font("Times", "", 14)
    pdf.cell(0, 14, "Laporan Koperasi", align="C")
    pdf.ln(14 * 1.25)
    pdf.set_font("Times", "", 12)
    if range_ == 0:  # Bulan
        pdf.cell(0, 10, f"Per Bulan {cld.month_name[bulan]} {tahun}", align="C")
        pdf.ln(12 * 1.25)
        file_name = f"laporan_{cld.month_name[bulan]}_{tahun}.pdf"
    elif range_ == 1:  # Tahun
        pdf.cell(0, 10, f"Per Tahun {tahun}", align="C")
        pdf.ln(12 * 1.25)
        file_name = f"laporan_{tahun}.pdf"

    pdf.set_font("Times", "B", 14)
    pdf.cell(116, 16, "Nama Barang", 1, align="C")
    pdf.cell(116, 16, "Keterangan", 1, align="C")
    pdf.cell(100, 16, "Debit", 1, align="C")
    pdf.cell(100, 16, "Kredit", 1, align="C")
    pdf.cell(100, 16, "Saldo", 1, align="C")
    pdf.ln()
    pdf.set_font("Times", "", 12)
    himpunan_barang = dict()
    for pembukuan in himpunan_pembukuan:
        border = 'LR'
        try: 
            himpunan_barang[pembukuan.nama_barang] += pembukuan.kredit
        except KeyError:
            himpunan_barang.update({pembukuan.nama_barang: pembukuan.kredit })
            border = 'LRT'

        nominal = pembukuan.debit - pembukuan.kredit
        pdf.cell(116, 16, pembukuan.nama_barang, border)
        pdf.cell(116, 16, pembukuan.keterangan, border)
        pdf.cell(
            100,
            16,
            angka_mudah_dibaca(nominal) if nominal > 0 else "",
            border,
        )
        pdf.cell(
            100,
            16,
            angka_mudah_dibaca(nominal) if nominal < 0 else "",
            border,
        )
        pdf.cell(100, 16, angka_mudah_dibaca(pembukuan.saldo), border)
        pdf.ln()
    pdf.cell(532, 16, "", "T")
    pdf.ln()
    pdf.ln()
    pdf.set_font("Times", "B", 12)
    pdf.cell(532, 16, "Keuntungan")
    pdf.set_font("Times", "", 12)
    pdf.ln()
    for barang, jumlah in himpunan_barang.items():
        nama_barang, ukuran = barang.split(' ')
        ukuran = None if ukuran == '#' else ukuran
        barang_ = db.scalar(select(Barang).where(and_(Barang.nama_barang == nama_barang, Barang.ukuran == ukuran)))
        pdf.cell(532, 16, f"{barang}:\t\t{angka_mudah_dibaca(jumlah)} x (Rp. {angka_mudah_dibaca(barang_.harga_jual)} - Rp. {angka_mudah_dibaca(barang_.modal)}) = Rp. {angka_mudah_dibaca(jumlah*(barang_.harga_jual-barang_.modal))}")
        pdf.ln()

    pdf.output(dir_loc + "/" + file_name)


def verifikasi_kunci_akses(db: Session, key: str):
    key_di_db = db.scalar(select(Access.key))
    if key_di_db == key + ambil_uuid():
        return key_di_db
    else:
        return False


def ubah_kunci_akses(db: Session, new_key: str):
    access = db.scalar(select(Access))
    access.key = new_key + ambil_uuid()
    db.commit()
