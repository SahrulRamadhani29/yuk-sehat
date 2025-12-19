# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- MODEL PEMBANTU ---
class FollowUpQuestion(BaseModel):
    """
    Model untuk struktur pertanyaan dinamis.
    Mendukung validasi objek JSON dari AI maupun sistem internal.
    """
    q: str = Field(..., description="Isi teks pertanyaan yang akan ditampilkan")
    type: str = Field(..., description="Tipe input: 'number' (angka), 'boolean' (Ya/Tidak), atau 'string' (teks bebas)")

# --- INPUT SCHEMAS ---
class TriageInput(BaseModel):
    """
    Model data yang dikirim oleh Frontend ke API /triage.
    """
    # Menambahkan NIK sebagai identitas unik sesi log
    nik: str = Field(..., example="3201234567890001", description="Nomor Induk Kependudukan pasien")
    
    age: Optional[int] = Field(0, example=30, description="Usia pasien dalam satuan tahun")
    
    complaint: str = Field(
        ..., example="Nyeri dada mendadak", description="Keluhan utama yang dirasakan pasien"
    )
    
    duration_hours: Optional[int] = Field(
        0, example=24, description="Durasi keluhan berlangsung dalam satuan jam"
    )
    
    pregnant: bool = Field(
        False, description="Status kehamilan pasien"
    )
    
    comorbidity: bool = Field(
        False, description="Status kepemilikan penyakit penyerta atau riwayat penyakit"
    )
    
    danger_sign: bool = Field(
        False,
        description="Flag tanda bahaya yang diklik secara manual oleh pengguna"
    )

# --- RESPONSE SCHEMAS ---
class TriageResponse(BaseModel):
    """
    Model data yang dikirim balik oleh API ke Frontend.
    """
    status: str = Field(..., example="COMPLETE", description="Status proses: 'COMPLETE' atau 'INCOMPLETE'")
    message: Optional[str] = Field(None, description="Pesan informasi dari sistem untuk ditampilkan ke pengguna")
    
    follow_up_questions: List[FollowUpQuestion] = Field(
        default=[], 
        description="Daftar objek pertanyaan tambahan beserta instruksi tipe inputnya"
    )
    
    triage_result: Optional[str] = Field(None, description="Klasifikasi warna triase: MERAH, KUNING, atau HIJAU")
    category: Optional[str] = Field(None, description="Kategori keluhan secara sistemis")
    is_risk_group: Optional[bool] = Field(None, description="Apakah pasien termasuk kelompok risiko tinggi")
    recommendation: List[str] = Field(default=[], description="Daftar rekomendasi obat bebas atau tindakan")
    ai_analysis: Optional[Dict[str, Any]] = Field(None, description="Data mentah hasil analisis AI")