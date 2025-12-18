from pydantic import BaseModel, Field
from typing import Optional, List, Any

# --- INPUT SCHEMAS ---
class TriageInput(BaseModel):
    # Kita ubah age menjadi Optional dengan default 0 agar tidak error saat user baru input teks saja
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

# --- RESPONSE SCHEMAS (BARU) ---
class TriageResponse(BaseModel):
    status: str = Field(..., example="COMPLETE", description="Status proses: COMPLETE atau INCOMPLETE")
    message: str = Field(..., description="Pesan dari sistem untuk user")
    ask_for: Optional[List[str]] = Field(None, description="Daftar field yang masih kosong (age, duration_hours)")
    follow_up_questions: Optional[List[str]] = Field(None, description="Pertanyaan tambahan untuk gejala kombinasi")
    
    # Data hasil triase (Hanya ada jika status COMPLETE)
    triage_result: Optional[str] = None
    category: Optional[str] = None
    is_risk_group: Optional[bool] = None
    recommendation: Optional[List[str]] = None
    ai_analysis: Optional[dict] = None