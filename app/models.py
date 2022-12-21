from sqlalchemy import Column, String, Integer, Date, DateTime, Numeric, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import pytz


class Barang(Base):
    __tablename__ = 'barang'

    id = Column(Integer, primary_key=True)
    nama_barang = Column(String, nullable=False, index=True)
    tersedia = Column(Integer, nullable=False)
    terjual = Column(Integer, nullable=False, default=0)
    modal = Column(Numeric(12, 2), nullable=False)
    harga_jual = Column(Numeric(12, 2), nullable=False)
    bisa_dicicil = Column(Boolean, nullable=False, default=False)

    himpunan_cicilan = relationship('Cicilan', back_populates='barang')


class Cicilan(Base):
    __tablename__ = 'cicilan'

    id = Column(Integer, primary_key=True)
    id_barang = Column(Integer, ForeignKey('barang.id'), nullable=False)
    nisn_siswa = Column(String, ForeignKey('siswa.nisn'), nullable=False)
    kali_pembayaran = Column(Integer, CheckConstraint('kali_pembayaran > 1'),  nullable=False)
    sudah_dibayar = Column(Integer, default=0)

    barang = relationship('Barang', back_populates='himpunan_cicilan')
    siswa = relationship('Siswa', back_populates='himpunan_cicilan')


class Pembukuan(Base):
    __tablename__ = 'pembukuan'

    id = Column(Integer, primary_key=True)
    tanggal = Column(DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Jakarta')))
    uraian = Column(String, nullable=False)
    debit = Column(Numeric(12, 2), nullable=False, default=0.0)
    kredit = Column(Numeric(12, 2), nullable=False, default=0.0)
    saldo = Column(Numeric(12, 2), nullable=False, default=0.0)


class Siswa(Base):
    __tablename__ = 'siswa'

    nisn = Column(String, primary_key=True)
    nama = Column(String, nullable=False, index=True)
    kelas = Column(String, nullable=False, index=True)

    himpunan_cicilan = relationship('Cicilan', back_populates='siswa')


class Access(Base):
    __tablename__ = 'access'

    key = Column(String, primary_key=True)
