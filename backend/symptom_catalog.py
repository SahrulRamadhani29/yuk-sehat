# symptom_catalog.py
from typing import Optional

# ---------------------------------------------------------
# 1. MILD SYMPTOMS (Kategori Hijau/Kuning)
# Pemetaan kata kunci masif: Bahasa Indonesia, Medis, & Daerah
# ---------------------------------------------------------
SYMPTOM_MAP = {
    "demam_ringan": [
        "demam", "panas", "meriang", "sumeng", "badan hangat", "greges", "suhu naik",
        "badan gerah", "keringat dingin", "demam naik turun", "panas dalam", "badan adem panas",
        "menggigil ringan", "badan panas dingin", "anak panas", "bayi panas", "kancing gigi"
    ],
    "batuk_pilek": [
        "batuk", "pilek", "hidung tersumbat", "hidung meler", "bersin", "flu", "ingusan",
        "batuk berdahak", "batuk kering", "pilek mampet", "grok-grok", "suara serak",
        "hidung buntu", "bersin-bersin", "pilek berat", "batuk rejan", "lendir di tenggorokan",
        "ispa", "bronkitis ringan", "napas grok", "idung mampet"
    ],
    "sakit_kepala_ringan": [
        "pusing", "sakit kepala", "kepala berat", "cekot-cekot", "pening", "migrain ringan",
        "nyut-nyutan", "puyeng", "kleyengan", "kepala senat-senut", "migren", "sakit pelipis",
        "pusing tujuh keliling", "kepala pening", "migraine", "vertigo ringan"
    ],
    "nyeri_otot_ringan": [
        "pegal", "nyeri otot", "linu", "nyeri badan", "pegal linu", "badan sakit semua",
        "nyeri sendi", "boyok sakit", "pegel", "otot kaku", "salah urat", "badan remuk",
        "encok", "saraf terjepit", "pegel-pegel", "punggung nyeri", "pinggang sakit", "asam urat"
    ],
    "nyeri_tenggorokan": [
        "sakit tenggorokan", "tenggorokan perih", "sakit menelan", "tenggorokan gatal", "radang",
        "tenggorokan sakit", "tenggorokan mengganjal", "serak", "nelan sakit", "tenggorokan panas",
        "tenggorokan kering", "susah nelan", "amandel kumat", "tenggorokan merah", "sariawan tenggorokan"
    ],
    "sakit_gigi": [
        "sakit gigi", "gigi berlubang", "gigi pecah", "gusi nyeri", "gigi berdenyut", "nyeri gigi",
        "gusi bengkak", "gigi goyang", "linu gigi", "sakit gusi", "geraham sakit", "gusi berdarah",
        "pipi bengkak karena gigi", "gigi bungsu", "senat senut gigi"
    ],
    "diare_ringan": [
        "diare", "mencret", "buang air terus", "murus", "mencret-mencret", "menceret",
        "bab cair", "mencret air", "bab lembek", "urus-urus", "kebelet bab", "feses cair"
    ],
    "mual_ringan": [
        "mual", "ingin muntah", "eneg", "lambung tidak enak", "perut perih", "sakit maag",
        "asam lambung", "perut melilit", "kembung", "begah", "perut kaku", "ulu hati perih",
        "gerd", "lambung perih", "muntah-muntah kecil", "perut sebah", "perut peres"
    ],
    "masalah_kulit_ringan": [
        "gatal", "ruam ringan", "biang keringat", "panu", "kudis", "bentol", "alergi kulit",
        "kulit merah", "budukan", "eksim", "biduran", "kaligata", "kurap", "kutu air",
        "kulit melepuh", "cacar air", "jerawat meradang", "kadas"
    ],
    "sembelit_konstipasi": [
        "susah bab", "sembelit", "konstipasi", "perut begah", "tidak bisa bab", "bab keras",
        "bebelen", "ngeden susah", "bab tidak lancar", "susah buang air besar"
    ],
    "kesehatan_mental_ringan": [
        "cemas", "gelisah", "susah tidur", "insomnia", "stres", "panik", "deg-degan takut"
    ],
    "kesehatan_ibu_anak": [
        "nyeri haid", "haid tidak teratur", "mual hamil", "asi mampet", "ruam popok bayi"
    ]
}

# ---------------------------------------------------------
# 2. DANGER CATEGORIES (WHO ETAT & IMCI) - STATUS MERAH
# ---------------------------------------------------------
DANGER_CATEGORIES = {
    "PERNAPASAN": [
        "sesak napas", "sulit bernapas", "napas berat", "napas cepat", "tidak bisa bernapas", 
        "napas bunyi", "mengi", "ngos-ngosan", "napas megap-megap", "tarikan dinding dada", 
        "bengek", "napas satu-satu", "asma kumat", "napas pendek", "stridor", "sianosis",
        "napas bunyi ngik", "oksigen rendah", "sesak dada", "tersedak", "henti napas"
    ],
    "SIRKULASI": [
        "nyeri dada", "dada terasa tertekan", "jantung berdebar hebat", "nadi tidak teraba", 
        "tangan kaki dingin", "bibir biru", "pucat sekali", "syok", "nyeri jantung", "dada sakit",
        "dada seperti ditusuk", "keringat jagung", "dada sesak sekali", "nadi cepat",
        "jantung deg-degan parah", "pingsan karena jantung", "aritmia", "serangan jantung"
    ],
    "NEUROLOGIS": [
        "pingsan", "tidak sadar", "kejang", "kejang-kejang", "linglung berat", 
        "tidak bisa dibangunkan", "penurunan kesadaran", "kaku kuduk", "leher kaku", 
        "bicara pelo", "lemas sebelah badan", "bicara tidak jelas", "wajah mencong", 
        "stroke", "lumpuh", "setengah badan mati rasa", "koma", "mata mendelik",
        "sulit bicara", "mulut miring", "pandangan kabur mendadak", "kelumpuhan"
    ],
    "PERDARAHAN": [
        "batuk berdarah", "muntah darah", "berak berdarah", "bab berdarah", "bab hitam", 
        "perdarahan hebat", "darah banyak", "mimisan tidak berhenti", "kencing darah", 
        "darah mengalir", "pendarahan vagina", "darah segar", "luka robek besar",
        "pendarahan hamil", "keluar darah banyak"
    ],
    "TRAUMA": [
        "tertancap paku", "luka dalam", "luka parah", "jatuh keras", "kecelakaan", 
        "patah tulang", "benturan kepala", "luka bakar luas", "digigit ular", "keracunan",
        "minum racun", "kena tusuk", "tulang menonjol", "tabrakan", "kesetrum", "tenggelam"
    ],
    "KIA_DARURAT": [
        "kejang kehamilan", "eklampsia", "ketuban pecah", "bayi tidak bernapas", "bayi biru"
    ]
}

# ---------------------------------------------------------
# 3. MODERATE RISK (Kategori Kuning)
# ---------------------------------------------------------
MODERATE_RISK_KEYWORDS = [
    "nyeri parah", "tidak tertahankan", "makin parah", "semakin parah", "berulang", 
    "kambuh", "sudah 3 hari", "lemas", "kurang cairan", "pusing berputar", "vertigo", 
    "lemas sekali", "tidak kunjung sembuh", "sudah lama", "gejala menetap",
    "badan lunglai", "tidak bertenaga", "semakin lemas"
]

def detect_danger_category(complaint_text: str) -> Optional[str]:
    if not complaint_text: return None
    text = complaint_text.lower()
    for category, keywords in DANGER_CATEGORIES.items():
        if any(keyword in text for keyword in keywords):
            return category
    return None

def map_symptoms(complaint_text: str) -> list[str]:
    if not complaint_text: return []
    text = complaint_text.lower()
    found_symptoms = []
    for symptom_key, keywords in SYMPTOM_MAP.items():
        if any(keyword in text for keyword in keywords):
            found_symptoms.append(symptom_key)
    return found_symptoms