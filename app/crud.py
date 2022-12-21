from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session, relationship
from models import *


def create_access_key(db: Session):
    if not db.scalar(select(Access)):
        key = Access(key="aplikasi_koperasi!!!")
        db.add(key)
        db.commit()


def beli(db: Session, id_barang: int, jumlah_dibeli: int):
    barang = db.scalar(select(Barang).where(Barang.id == id_barang))
    if (barang.tersedia - barang.terjual) >= jumlah_dibeli:
        barang.terjual += jumlah_dibeli
        harga = barang.harga_jual * jumlah_dibeli
        saldo_terakhir = db.execute(
            select(Pembukuan.saldo).order_by(Pembukuan.id.asc())
        ).first()
        pembukuan = Pembukuan(uraian="", debit=harga, saldo=saldo_terakhir + harga)
        db.add(pembukuan)
        db.commit()


def get_barang(db: Session):
    return db.scalars(select(Barang)).all()


def get_siswa(db: Session):
    return db.scalars(select(Siswa)).all()


def get_pembukuan(db: Session):
    return db.scalars(select(Pembukuan)).all()


def get_cicilan(db: Session):
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


