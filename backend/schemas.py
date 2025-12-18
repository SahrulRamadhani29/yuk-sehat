from pydantic import BaseModel, Field
from typing import Optional


class TriageInput(BaseModel):
    age: int = Field(..., example=30, description="Usia pasien (tahun)")
    complaint: str = Field(
        ..., example="Batuk, pilek, pusing", description="Keluhan utama"
    )
    duration_hours: Optional[int] = Field(
        None, example=24, description="Durasi keluhan (jam)"
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
