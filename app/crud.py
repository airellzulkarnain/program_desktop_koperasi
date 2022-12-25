from sqlalchemy import select, update, delete, and_, func
from datetime import datetime
from sqlalchemy.orm import Session
from fpdf import FPDF
from models import *
import pandas as pd
import calendar as cld
import subprocess as sp


def buat_kunci_akses(db: Session):
    if not db.scalar(select(Access)):
        key = Access(key=ambil_uuid()*2)
        db.add(key)
        db.commit()


def bagi_pembayaran(nominal: int, dibagi: int)-> list:
    rupiah: int = [100_000, 50_000, 20_000, 10_000, 5_000, 2_000, 1_000, 500]
    result: int = 0

    while nominal:
        x = nominal//dibagi
        for uang in rupiah:
            if uang <= x:
                x = uang
                break
            elif uang == 500:
                return [result+nominal]+[result for i in range(dibagi-1)]

        result += (nominal//(x*dibagi))*x
        nominal = (nominal%(x*dibagi))
    return [result for i in range(dibagi)]


def ambil_uuid():
    return (
        sp.check_output("wmic csproduct get UUID")
        .decode("utf-8")
        .split("\n")[1]
        .strip()
    )


def jual(db: Session, id_barang: int, jumlah_terjual: int):
    barang = db.scalar(select(Barang).where(Barang.id == id_barang))
    if 0 < jumlah_terjual <= barang.tersedia_saat_ini:
        barang.tersedia_saat_ini -= jumlah_terjual
        harga = barang.harga_jual * jumlah_terjual
        saldo_terakhir = db.scalar(
            select(Pembukuan.saldo).order_by(Pembukuan.id.desc())
        )
        db.add(
            Pembukuan(
                uraian=f"Jual: {barang.id}: {barang.nama_barang}: x{jumlah_terjual}",
                debit=harga,
                saldo=saldo_terakhir + harga,
            )
        )
        db.commit()


def ambil_barang(db: Session):
    return db.scalars(select(Barang)).all()


def ambil_siswa(db: Session):
    return db.scalars(select(Siswa)).all()


def ambil_pembukuan(db: Session):
    return db.scalars(select(Pembukuan)).all()


def ambil_cicilan(db: Session):
    return db.scalars(
        select(
            Barang.nama_barang,
            Siswa.nama,
            Cicilan.id_barang,
            Cicilan.nisn_siswa,
            Cicilan.kali_pembayaran,
            Cicilan.sudah_dibayar,
        )
        .select_from(Cicilan)
        .join(Siswa, Cicilan.nisn_siswa == Siswa.nisn)
        .join(Barang, Barang.id == Cicilan.id_barang)
    ).all()


def biaya_tambahan(db: Session, uraian: str, debit: float = 0.0, kredit: float = 0.0):
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).order_by(Pembukuan.id.desc())) or 0
    if debit > 0.0 and kredit == 0.0 and len(uraian) > 0:
        db.add(Pembukuan(uraian=uraian, debit=debit, saldo=saldo_terakhir + debit))
    elif kredit > 0.0 and debit == 0.0 and len(uraian) > 0:
        db.add(
            Pembukuan(
                uraian="Biaya - biaya: " + uraian,
                kredit=kredit,
                saldo=saldo_terakhir - kredit,
            )
        )
    db.commit()


def tambah_barang(
    db: Session,
    nama_barang: str,
    tersedia: int,
    modal: float,
    harga_jual: float,
    bisa_dicicil: bool,
):
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).order_by(Pembukuan.id.desc())) or 0
    kredit = modal * tersedia
    barang = Barang(
        nama_barang=nama_barang,
        tersedia=tersedia,
        tersedia_saat_ini=tersedia,
        modal=modal,
        harga_jual=harga_jual,
        bisa_dicicil=bisa_dicicil,
    )
    db.add(barang)
    db.flush()
    db.add(
        Pembukuan(
            uraian=f"Beli: {barang.id}: {barang.nama_barang}: x{barang.tersedia}",
            kredit=kredit,
            saldo=saldo_terakhir - kredit,
        )
    )
    db.commit()


def tambah_stok_barang(db: Session, id_barang: int, jumlah_tambah: int):
    barang = db.scalar(select(barang).where(Barang.id == id_barang))
    barang.tersedia_saat_ini += jumlah_tambah
    if barang.tersedia_saat_ini > barang.tersedia:
        barang.tersedia = barang.tersedia_saat_ini
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).order_by(Pembukuan.id.desc()))
    kredit = barang.modal * jumlah_tambah
    db.add(
        Pembukuan(
            uraian=f"Tambah: {id_barang}: {barang.nama_barang}: x{jumlah_tambah}",
            kredit=kredit,
            saldo=saldo_terakhir - kredit,
        )
    )
    db.commit()


def hapus_barang(db: Session, id_barang: int):
    barang = db.scalar(select(Barang).where(Barang.id == id_barang))
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).order_by(Pembukuan.id.desc())) or 0.0
    sudah_ditambah = bool(db.scalar(select(func.count(Pembukuan.id)).where(Pembukuan.uraian.like(f'%Tambah: {id_barang}: {barang.nama_barang}: x%'))))
    if barang.tersedia == barang.tersedia_saat_ini and (not barang.bisa_dicicil or barang.himpunan_cicilan == []) and not sudah_ditambah:
        nominal = barang.tersedia*barang.modal
        db.add(Pembukuan(uraian=f'Hapus: {id_barang}: {barang.nama_barang}: x{barang.tersedia}', debit=nominal, saldo=saldo_terakhir+nominal))
        db.delete(barang)
        db.commit()



def tambah_siswa(db: Session, file_loc: str):
    excel_file = pd.read_excel(file_loc)
    excel_file.drop_duplicates(inplace=True)
    excel_file.dropna(inplace=True, how="any")
    excel_file.rename(
        columns={header: header.lower() for header in excel_file.columns.values},
        inplace=True,
    )
    excel_file = excel_file.applymap(str)
    for i, siswa in excel_file.iterrows():
        if not db.scalar(select(Siswa).where(Siswa.nisn == siswa["nisn"])):
            db.add(Siswa(nisn=siswa["nisn"], nama=siswa["nama"], kelas=siswa["kelas"]))
        else:
            db.execute(
                update(Siswa)
                .where(and_(Siswa.nisn == siswa["nisn"], Siswa.kelas != siswa["kelas"]))
                .values(kelas=siswa["kelas"])
            )
    db.commit()


def hapus_siswa(db: Session):
    db.execute(delete(Siswa).where(Siswa.himpunan_cicilan == []))
    db.commit()


def tambah_cicilan(
    db: Session, himpunan_nisn_siswa: list, id_barang: int, kali_pembayaran: int
):
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).order_by(Pembukuan.id.desc()))
    for nisn_siswa in himpunan_nisn_siswa:
        db.add(
            Cicilan(
                id_barang=id_barang,
                nisn_siswa=nisn_siswa,
                kali_pembayaran=kali_pembayaran,
            )
        )
        db.add(
            Pembukuan(
                uraian=f"Buat Cicilan:NISN:{nisn_siswa},ID Barang:{id_barang},pembayaran:0/{kali_pembayaran}",
                saldo=saldo_terakhir,
            )
        )
    db.commit()


def bayar_cicilan(db: Session, id_cicilan: int, kali_bayar: int, harga_barang: float):
    cicilan = db.scalar(select(Cicilan).where(Cicilan.id == id_cicilan))
    barang = db.scalar(
        select(Barang).where(Barang.id == cicilan.id_barang)
    )
    saldo_terakhir = db.scalar(select(Pembukuan.saldo).order_by(Pembukuan.id.desc()))
    harga = sum(bagi_pembayaran(harga_barang, cicilan.kali_pembayaran)[cicilan.sudah_dibayar:cicilan.sudah_dibayar+kali_bayar])
    cicilan.sudah_dibayar += kali_bayar
    db.add(
        Pembukuan(
            uraian=f"Cicilan: {cicilan.id_barang}: {barang.nama_barang}: {cicilan.id}: pembayaran:{cicilan.sudah_dibayar}/{cicilan.kali_pembayaran}",
            debit=harga,
            saldo=saldo_terakhir + harga,
        )
    )
    db.flush()
    if cicilan.sudah_dibayar == cicilan.kali_pembayaran:
        himpunan_cicilan = db.scalars(
            select(Pembukuan).where(
                Pembukuan.uraian.like(
                    f"%Cicilan: {cicilan.id_barang}: {barang.nama_barang}: {cicilan.id}: %"
                )
            )
        )
        for item in himpunan_cicilan:
            item.uraian = item.uraian.replace("Cicilan", "Cicilan Lunas")
        db.delete(cicilan)
        barang.tersedia_saat_ini -= 1
    db.commit()


# Bulan = 0, Tahun = 1, Custom = 2
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
    laporan = dict()
    if range_ == 0:  # Bulan
        himpunan_pembukuan = db.scalars(
            select(Pembukuan).where(
                and_(
                    Pembukuan.tanggal >= datetime(tahun, bulan, 1),
                    Pembukuan.tanggal
                    <= datetime(tahun, bulan, cld.monthrange(tahun, bulan)[1]),
                )
            )
        ).all()
    elif range_ == 1:  # Tahun
        himpunan_pembukuan = db.scalars(
            select(Pembukuan).where(
                and_(
                    Pembukuan.tanggal >= datetime(tahun, 1, 1),
                    Pembukuan.tanggal <= datetime(tahun, 12, 31),
                )
            )
        ).all()
    elif range_ == 2:  # Custom
        himpunan_pembukuan = db.scalars(
            select(Pembukuan).where(
                and_(Pembukuan.tanggal >= dari, Pembukuan.tanggal <= sampai)
            )
        ).all()
    for pembukuan in himpunan_pembukuan:
        uraian = pembukuan.uraian.split(": ")
        try:
            if uraian[0] in ["Beli", "Tambah", "Jual"]:
                laporan[uraian[0] + " " + uraian[1] + " " + uraian[2]] += (
                    pembukuan.debit - pembukuan.kredit
                )
            elif uraian[0] == "Cicilan Lunas":
                laporan["Jual " + uraian[1] + " " + uraian[2]] += pembukuan.debit
            elif uraian[0] == "Cicilan":
                laporan["Cicilan"] += pembukuan.debit
            else:
                raise KeyError
        except KeyError:
            if uraian[0] in ["Beli", "Tambah", "Jual"]:
                laporan[uraian[0] + " " + uraian[1] + " " + uraian[2]] = (
                    pembukuan.debit - pembukuan.kredit
                )
            elif uraian[0] == "Cicilan Lunas":
                laporan["Jual " + uraian[1] + " " + uraian[2]] = pembukuan.debit
            elif uraian[0] == "Cicilan":
                laporan["Cicilan"] = pembukuan.debit
            elif uraian[0] == "Biaya - biaya":
                laporan[pembukuan.uraian] = pembukuan.debit - pembukuan.kredit

    laporan["saldo_awal"] = (
        db.scalar(
            select(Pembukuan.saldo).where(Pembukuan.id == himpunan_pembukuan[0].id - 1)
        )
        or 0
    )
    laporan["saldo_akhir"] = himpunan_pembukuan[-1].saldo

    pdf = FPDF(orientation='P', unit='pt', format='A4')
    pdf.add_page()
    pdf.set_font('Times', 'B', 16)
    pdf.cell(0, 16, sekolah.upper(), align='C')
    pdf.ln(16)
    pdf.set_font('Times', '', 14)
    pdf.cell(0, 14, 'Laporan Koperasi', align='C')
    pdf.ln(14*1.25)
    pdf.set_font('Times', '', 12)
    if range_ == 0: # Bulan
        pdf.cell(0, 10, f'Per Bulan {cld.month_name[bulan]} {tahun}', align='C')
        pdf.ln(12*1.25)
        file_name = f'laporan_{cld.month_name[bulan]}_{tahun}.pdf'
    elif range_ == 1: # Tahun
        pdf.cell(0, 10, f'Per Tahun {tahun}', align='C')
        pdf.ln(12*1.25)
        file_name = f'laporan_{tahun}.pdf'
    elif range_ == 2: # Custom
        pdf.cell(0, 10, f'Per {str(dari.date())} s/d {str(sampai.date())}', align='C')
        pdf.ln(12*1.25)
        file_name = f'laporan_{str(dari.date())}_-_{str(sampai.date())}.pdf'

    pdf.set_font('Times', 'B', 14)
    pdf.cell(232, 16, 'Keterangan', 1, align='C')
    pdf.cell(100, 16, 'Debit', 1, align='C')
    pdf.cell(100, 16, 'Kredit', 1, align='C')
    pdf.cell(100, 16, 'Saldo', 1, align='C')
    pdf.ln()
    pdf.set_font('Times', '', 12)
    saldo = laporan['saldo_awal']
    pdf.cell(432, 16, 'Saldo Awal', 'LRB')
    pdf.cell(100, 16,'Rp. ' + str(laporan['saldo_awal']), 'LRB')
    pdf.ln()
    for keterangan, nominal in laporan.items():
        if keterangan not in ['saldo_akhir', 'saldo_awal']: 
            pdf.cell(232, 16, keterangan, 'LR')
            pdf.cell(100, 16, 'Rp.' + str(nominal) if nominal > 0 else '', 'LR')
            pdf.cell(100, 16, 'Rp.' + str(nominal) if nominal < 0 else '', 'LR')
            saldo += nominal
            pdf.cell(100, 16, 'Rp.' + str(saldo), 'LR')
            pdf.ln()
    pdf.cell(432, 16, 'Saldo Akhir', 'LRT')
    pdf.cell(100, 16,'Rp. ' + str(laporan['saldo_akhir']), 'LRT')
    pdf.ln()
    pdf.cell(532, 16, '', 'T')
    pdf.ln()
    
    pdf.output(dir_loc + file_name)


def verifikasi_kunci_akses(db: Session, key: str):
    return db.scalar(select(Access.key)) == key + ambil_uuid()


def ubah_kunci_akses(db: Session, new_key: str):
    access = db.scalar(select(Access))
    access.key = new_key + ambil_uuid()
    db.commit()
