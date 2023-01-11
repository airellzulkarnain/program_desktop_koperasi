from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    ForeignKey,
    Boolean,
    CheckConstraint,
    Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum
import pytz


class Size(enum.Enum):
    XXL = 'XXL'
    XL = 'XL'
    L = 'L'
    M = 'M'
    S = 'S'
    XS = 'XS'


class Barang(Base):
    __tablename__ = "barang"

    id = Column(Integer, primary_key=True)
    nama_barang = Column(String, nullable=False, index=True)
    tersedia = Column(Integer, nullable=False)
    tersedia_saat_ini = Column(Integer, nullable=False)
    modal = Column(Integer, nullable=False)
    harga_jual = Column(Integer, nullable=False)
    ukuran = Column(String)


class Pembukuan(Base):
    __tablename__ = "pembukuan"

    id = Column(Integer, primary_key=True)
    tanggal = Column(
        Date, nullable=False, default=datetime.now(pytz.timezone("Asia/Jakarta")).date()
    )
    nama_barang = Column(String, nullable=False)
    keterangan = Column(String, nullable=False)
    debit = Column(Integer, nullable=False, default=0)
    kredit = Column(Integer, nullable=False, default=0)
    saldo = Column(Integer, nullable=False, default=0)


class Access(Base):
    __tablename__ = "access"

    key = Column(String, primary_key=True)
