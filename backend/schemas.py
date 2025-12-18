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
    type: str = Field(..., description="Tipe input yang diminta: 'number' (angka) atau 'boolean' (Ya/Tidak)")

# --- INPUT SCHEMAS ---
class TriageInput(BaseModel):
    """
    Model data yang dikirim oleh Frontend ke API /triage.
    """
    # Usia menggunakan default 0 agar sistem bisa mendeteksi data kosong
    age: Optional[int] = Field(0, example=30, description="Usia pasien dalam satuan tahun")
    
    complaint: str = Field(
        ..., example="Nyeri dada mendadak", description="Keluhan utama yang dirasakan pasien"
    )
    
    # Durasi menggunakan default 0 untuk memicu validasi data dasar di awal
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
    message: str = Field(..., description="Pesan informasi dari sistem untuk ditampilkan ke pengguna")
    
    # Menggunakan model FollowUpQuestion agar tidak terjadi error validasi string vs dict
    follow_up_questions: Optional[List[FollowUpQuestion]] = Field(
        default=[], 
        description="Daftar objek pertanyaan tambahan beserta instruksi tipe inputnya"
    )
    
    # Field pendukung untuk backward compatibility
    ask_for: Optional[List[str]] = Field(None, description="Daftar field teknis yang masih kosong")
    
    # Data hasil triase (Hanya akan berisi data jika status == 'COMPLETE')
    triage_result: Optional[str] = Field(None, description="Klasifikasi warna triase: MERAH, KUNING, atau HIJAU")
    category: Optional[str] = Field(None, description="Kategori keluhan secara sistemis")
    is_risk_group: Optional[bool] = Field(None, description="Apakah pasien termasuk kelompok risiko tinggi")
    recommendation: Optional[List[str]] = Field(default=[], description="Daftar rekomendasi obat bebas atau tindakan")
    ai_analysis: Optional[Dict[str, Any]] = Field(None, description="Data mentah hasil analisis AI")