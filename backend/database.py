# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Ambil URL dari Environment Variable (Neon/Render)
# Kita hapus default "sqlite:///..." agar sistem tidak diam-diam pakai SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "FATAL ERROR: DATABASE_URL tidak ditemukan! "
        "Pastikan Anda sudah mengatur Environment Variable di Render atau file .env Anda."
    )

# 2. Fix untuk format URL Postgres (Neon sering pakai postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Konfigurasi Engine Khusus PostgreSQL
# Kita hapus 'connect_args' karena itu hanya untuk SQLite
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True  # Sangat disarankan untuk Neon agar koneksi tidak sering terputus (idle)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()