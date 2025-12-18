from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# --- MODEL PEMBANTU ---
class FollowUpQuestion(BaseModel):
    """Model untuk struktur pertanyaan dinamis dari AI"""
    q: str = Field(..., description="Isi pertanyaan")
    type: str = Field(..., description="Tipe input: 'number' atau 'boolean'")

# --- INPUT SCHEMAS ---
class TriageInput(BaseModel):
    # Usia opsional agar sistem bisa meminta input belakangan via Incomplete
    age: Optional[int] = Field(0, example=30, description="Usia pasien (tahun)")
    complaint: str = Field(
        ..., example="Nyeri dada mendadak", description="Keluhan utama"
    )
    duration_hours: Optional[int] = Field(
        0, example=24, description="Durasi keluhan (jam)"
    )
    pregnant: bool = Field(
        False, description="Status kehamilan"
    )
    comorbidity: bool = Field(
        False, description="Penyakit penyerta"
    )
    danger_sign: bool = Field(
        False,
        description="Tanda bahaya yang disadari pengguna"
    )

# --- RESPONSE SCHEMAS (REVISI FINAL) ---
class TriageResponse(BaseModel):
    status: str = Field(..., example="COMPLETE", description="Status proses: COMPLETE atau INCOMPLETE")
    message: str = Field(..., description="Pesan dari sistem untuk user")
    
    # REVISI: Menggunakan model FollowUpQuestion untuk mendukung format objek {"q": "...", "type": "..."}
    follow_up_questions: Optional[List[FollowUpQuestion]] = Field(
        default=[], 
        description="Daftar pertanyaan tambahan beserta tipe inputnya"
    )
    
    # Field pendukung validasi lama (Opsional)
    ask_for: Optional[List[str]] = Field(None, description="Daftar field yang masih kosong")
    
    # Data hasil triase (Hanya ada jika status COMPLETE)
    triage_result: Optional[str] = None
    category: Optional[str] = None
    is_risk_group: Optional[bool] = None
    recommendation: Optional[List[str]] = None
    ai_analysis: Optional[Dict[str, Any]] = None