# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from datetime import datetime
import pytz
from database import Base

def wib_now():
    """Mengembalikan waktu saat ini dalam zona waktu Asia/Jakarta."""
    return datetime.now(pytz.timezone("Asia/Jakarta"))

class TriageLog(Base):
    __tablename__ = "triage_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Menambahkan kolom NIK sebagai identitas log
    nik = Column(String, index=True, nullable=False) 
    
    age = Column(Integer)
    
    # TAMBAHAN: Kolom durasi untuk mendukung logika ekstraksi baru
    duration_hours = Column(Integer, nullable=True) 
    
    # Menggunakan Text untuk mendukung riwayat percakapan yang panjang
    complaint = Column(Text) 
    category = Column(String, default="UMUM")
    triage_result = Column(String)
    danger_sign = Column(Boolean)
    risk_group = Column(Boolean)
    
    # Timestamp pencatatan kunjungan
    created_at = Column(DateTime, default=wib_now)