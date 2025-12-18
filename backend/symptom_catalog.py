# symptom_catalog.py
from typing import Optional

# Pemetaan gejala ringan (Lapis 2 - Rules)
# symptom_catalog.py

# ---------------------------------------------------------
# 1. MILD SYMPTOMS (Kategori Hijau/Kuning)
# ---------------------------------------------------------
SYMPTOM_MAP = {
    "demam_ringan": [
        "demam", "panas", "meriang", "sumeng", "badan hangat", "greges"
    ],
    "batuk_pilek": [
        "batuk", "pilek", "hidung tersumbat", "hidung meler", "bersin", "sakit tenggorokan", "flu", "pilek"
    ],
    "sakit_kepala_ringan": [
        "pusing", "sakit kepala", "kepala berat", "cekot-cekot", "pening", "migrain ringan"
    ],
    "nyeri_otot_ringan": [
        "pegal", "nyeri otot", "linu", "nyeri badan", "pegal linu", "badan sakit semua", "nyeri sendi"
    ],
    "nyeri_tenggorokan": [
        "sakit tenggorokan", "tenggorokan perih", "sakit menelan", "tenggorokan gatal", "radang"
    ],
    "diare_ringan": [
        "diare", "mencret", "buang air terus", "murus", "mencret-mencret"
    ],
    "mual_ringan": [
        "mual", "ingin muntah", "eneg", "lambung tidak enak"
    ],
    "masalah_kulit_ringan": [
        "gatal", "ruam ringan", "biang keringat", "panu", "kudis", "bentol"
    ]
}

# ---------------------------------------------------------
# 2. DANGER CATEGORIES (Lapis 2 - WHO ETAT & IMCI Keywords)
# Pemicu Otomatis Klasifikasi MERAH
# ---------------------------------------------------------
DANGER_CATEGORIES = {
    "PERNAPASAN": [
        "sesak napas", "sulit bernapas", "napas berat", "napas cepat", "tidak bisa bernapas", 
        "napas bunyi", "mengi", "ngos-ngosan", "napas megap-megap", "tarikan dinding dada"
    ],
    "SIRKULASI": [
        "nyeri dada", "dada terasa tertekan", "jantung berdebar hebat", "nadi tidak teraba", 
        "tangan kaki dingin", "bibir biru", "pucat sekali", "syok"
    ],
    "NEUROLOGIS": [
        "pingsan", "tidak sadar", "kejang", "kejang-kejang", "linglung berat", 
        "tidak bisa dibangunkan", "penurunan kesadaran", "kaku kuduk", "leher kaku", "bicara pelo"
    ],
    "PERDARAHAN": [
        "batuk berdarah", "muntah darah", "berak berdarah", "bab berdarah", "bab hitam", 
        "perdarahan hebat", "darah banyak", "mimisan tidak berhenti", "kencing darah"
    ],
    "TRAUMA": [
        "tertancap paku", "luka dalam", "luka parah", "jatuh keras", "kecelakaan", 
        "patah tulang", "benturan kepala", "luka bakar luas", "digigit ular", "keracunan"
    ],
    "INFEKSI_BERAT": [
        "demam tinggi", "menggigil hebat", "badan sangat lemas", "tidak mau makan minum", 
        "muntah terus menerus", "ubun-ubun cekung", "mata cekung"
    ],
    "UMUM_DARURAT": [
        "nyeri hebat", "lemas sekali", "tidak bisa bangun", "kondisi kritis", "butuh oksigen"
    ]
}

# ---------------------------------------------------------
# 3. MODERATE RISK (Kategori Kuning)
# ---------------------------------------------------------
MODERATE_RISK_KEYWORDS = [
    "nyeri parah", "tidak tertahankan", "makin parah", "semakin parah", "berulang", 
    "kambuh", "sudah 3 hari", "lemas", "kurang cairan", "pusing berputar", "vertigo"
]

def detect_danger_category(complaint_text: str) -> Optional[str]:
    """Mendeteksi kategori bahaya berdasarkan kata kunci mati (Lapis 2)."""
    if not complaint_text:
        return None
    text = complaint_text.lower()
    for category, keywords in DANGER_CATEGORIES.items():
        if any(keyword in text for keyword in keywords):
            return category
    return None

def map_symptoms(complaint_text: str) -> list[str]:
    """Memetakan keluhan ke kategori gejala ringan."""
    if not complaint_text:
        return []
    text = complaint_text.lower()
    found_symptoms = []
    for symptom_key, keywords in SYMPTOM_MAP.items():
        if any(keyword in text for keyword in keywords):
            found_symptoms.append(symptom_key)
    return found_symptoms

def detect_moderate_risk(complaint_text: str) -> bool:
    """Mendeteksi indikasi risiko sedang dari teks."""
    MODERATE_RISK_KEYWORDS = ["nyeri hebat", "sakit banget", "nyeri parah", "tidak tertahankan", "makin parah", "semakin parah", "berulang", "kambuh"]
    if not complaint_text:
        return False
    text = complaint_text.lower()
    return any(keyword in text for keyword in MODERATE_RISK_KEYWORDS)