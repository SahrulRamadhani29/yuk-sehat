# rules.py
# =========================================================
# WHO-BASED PRE-TRIAGE RULE ENGINE (BACKEND SAFETY NET)
#
# References:
# - WHO Emergency Triage Assessment and Treatment (ETAT)
# - WHO Integrated Management of Childhood Illness (IMCI)
#
# IMPORTANT:
# - Rules are deterministic (Pasti)
# - Berfungsi sebagai Jaring Pengaman jika AI memberikan hasil LOW
# =========================================================

from typing import Optional

# -----------------------------
# TRIAGE CATEGORIES
# -----------------------------
TRIAGE_RED = "MERAH"
TRIAGE_YELLOW = "KUNING"
TRIAGE_GREEN = "HIJAU"


# -----------------------------
# RISK GROUP EVALUATION
# -----------------------------
def is_risk_group(
    age: int,
    pregnant: bool,
    comorbidity: bool,
) -> bool:
    """
    Menentukan kelompok risiko berdasarkan standar WHO.
    Lansia, Ibu Hamil, Komorbid, dan Anak-anak adalah Prioritas.
    """
    # Pasien Hamil
    if pregnant:
        return True

    # Pasien dengan Penyakit Penyerta (Diabetes, Jantung, dll)
    if comorbidity:
        return True

    # Lansia (Standar WHO umum >= 60 tahun)
    if age >= 60:
        return True

    # Balita (Standar WHO IMCI/ETAT < 5 tahun)
    if age < 5:                                                                                                     
        return True

    return False


# -----------------------------
# MAIN TRIAGE CLASSIFICATION
# -----------------------------
def classify_triage(
    danger_sign: bool,
    duration_hours: Optional[int],
    risk_group: bool,
) -> str:
    """
    Logika Klasifikasi Triase Akhir (Backend Decision).
    Digunakan oleh main.py untuk menyelaraskan temuan AI.
    
    Output:
    - MERAH  : Darurat (Segera ke IGD)
    - KUNING : Waspada (Prioritas Penanganan)
    - HIJAU  : Non-Urgen (Bisa Perawatan Mandiri)
    """

    # 1. EMERGENCY SIGNS (Prioritas Utama)
    # Jika ada tanda bahaya manual atau dari katalog, otomatis MERAH.
    if danger_sign:
        return TRIAGE_RED

    # 2. PRIORITY SIGNS (Status KUNING)
    # Meskipun gejala ringan, jika masuk kelompok risiko, status menjadi KUNING.
    if risk_group:
        return TRIAGE_YELLOW

    # Durasi sakit lebih dari 2 hari (48 jam) menjadi prioritas evaluasi.
    if duration_hours is not None and duration_hours > 48:
        return TRIAGE_YELLOW

    # 3. NON-URGENT (Status HIJAU)
    # Hanya untuk pasien tanpa risiko dan durasi baru.
    return TRIAGE_GREEN