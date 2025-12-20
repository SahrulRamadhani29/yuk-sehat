# symptom_catalog.py
from typing import Optional

# ---------------------------------------------------------
# 1. MILD–MODERATE SYMPTOMS (Kategori Hijau/Kuning)
# ---------------------------------------------------------
# Nama kategori (Keys) telah diselaraskan dengan 32 kategori sistem
# ---------------------------------------------------------

SYMPTOM_MAP = {

    "pernapasan": [
        "batuk", "batuk kering", "batuk berdahak", "pilek", "flu", "ingusan",
        "hidung mampet", "hidung tersumbat", "napas grok", "grok-grok",
        "bersin", "bersin-bersin", "ispa", "bronkitis ringan",
        "tenggorokan berlendir", "suara serak", "idung mampet"
    ],

    "sirkulasi_jantung": [
        "deg-degan ringan", "jantung berdebar", "ndrodok",
        "cepat capek", "mudah lelah", "tangan dingin",
        "pusing saat berdiri", "kunang-kunang",
        "tekanan darah naik ringan", "tekanan darah turun ringan"
    ],

    "neurologis": [
        "pusing", "pening", "puyeng", "kleyengan",
        "sakit kepala", "kepala berat", "cekot-cekot",
        "nyut-nyutan", "migren ringan", "migrain",
        "vertigo ringan", "kepala melayang"
    ],

    "pencernaan": [
        "mual", "eneg", "begah", "kembung", "perut penuh",
        "perut perih", "ulu hati perih", "maag", "sakit maag",
        "asam lambung", "gerd", "perut melilit ringan",
        "lambung tidak enak", "mual setelah makan"
    ],

    "tenggorokan": [
        "sakit tenggorokan", "tenggorokan perih", "tenggorokan gatal",
        "sakit menelan", "nelan sakit", "serak",
        "radang tenggorokan", "tenggorokan panas",
        "amandel bengkak ringan", "tenggorokan kering"
    ],

    "hidung_sinus": [
        "pilek", "hidung mampet", "hidung buntu",
        "ingus kental", "ingus hijau",
        "bersin terus", "nyeri sinus ringan",
        "idung mampet", "hidung gatal"
    ],

    "telinga": [
        "telinga nyeri ringan", "telinga berdenging",
        "telinga terasa penuh", "pendengaran berkurang ringan",
        "telinga gatal", "telinga kemasukan air"
    ],

    "mata": [
        "mata merah", "mata perih", "mata gatal",
        "mata berair", "mata lelah",
        "penglihatan buram ringan", "mata panas"
    ],

    "gigi_mulut": [
        "sakit gigi", "senat-senut gigi", "linu gigi",
        "gigi berlubang", "gusi nyeri",
        "gusi bengkak ringan", "sariawan",
        "bau mulut", "geraham sakit"
    ],

    "kulit": [
        "gatal", "ruam", "ruam ringan",
        "bentol", "biduran", "kaligata",
        "biang keringat", "eksim ringan",
        "kudis", "kurap", "kadas",
        "panu", "kutu air", "kulit merah"
    ],

    "alergi": [
        "alergi", "reaksi alergi ringan",
        "gatal setelah makan", "bentol alergi",
        "bersin alergi", "hidung gatal",
        "mata gatal", "alergi debu", "alergi dingin"
    ],

    "demam_infeksi": [
        "demam", "panas", "meriang", "sumeng",
        "badan hangat", "demam naik turun",
        "panas dingin", "menggigil ringan",
        "anak panas", "bayi panas", "demam rendah"
    ],

    "otot_sendi": [
        "pegal", "pegel", "linu", "pegal linu",
        "nyeri otot", "nyeri sendi",
        "otot kaku", "salah urat",
        "keseleo ringan", "encok",
        "pinggang pegal", "punggung pegal"
    ],

    "saluran_kemih": [
        "anyang-anyangan", "nyeri kencing",
        "kencing sering", "kencing sedikit",
        "kencing tidak tuntas", "air kencing keruh",
        "isk ringan", "perih saat kencing"
    ],

    "reproduksi_wanita": [
        "nyeri haid", "sakit haid", "dismenore",
        "haid tidak teratur", "keputihan",
        "keputihan gatal", "perut bawah nyeri ringan"
    ],

    "reproduksi_pria": [
        "nyeri selangkangan ringan",
        "nyeri testis ringan",
        "gatal area kemaluan",
        "tidak nyaman kemaluan"
    ],

    "kia": [
        "mual hamil ringan", "muntah hamil ringan",
        "asi mampet", "puting nyeri",
        "ruam popok", "bayi rewel",
        "anak susah makan", "mual hamil", "asi mampet", 
        "puting nyeri", "payudara bengkak menyusui", "mastitis"
    ],

    "mental": [
        "cemas", "gelisah", "stres",
        "panik ringan", "overthinking",
        "pikiran tidak tenang", "emosi labil"
    ],

    "tidur": [
        "susah tidur", "insomnia",
        "tidur gelisah", "sering terbangun",
        "ngantuk siang", "pola tidur kacau"
    ],

    "kelelahan": [
        "lemas", "capek", "lelah", "lesu",
        "tidak bertenaga", "badan drop",
        "kurang fit", "ngantuk terus"
    ]
}

# ---------------------------------------------------------
# 2. DANGER CATEGORIES (WHO ETAT & IMCI) - STATUS MERAH
# ---------------------------------------------------------

DANGER_CATEGORIES = {

    "pernapasan": [
        "sesak napas", "susah napas", "sulit bernapas", "tidak bisa bernapas",
        "napas berat", "napas pendek", "napas cepat sekali", "napas megap-megap",
        "ngos-ngosan", "bengek berat", "asma berat", "asma kumat parah",
        "napas bunyi", "napas grok berat", "mengi keras", "stridor",
        "tarikan dinding dada", "cuping hidung kembang kempis",
        "napas satu-satu", "napas putus-putus", "henti napas",
        "tersedak", "tersumbat jalan napas",
        "bibir biru", "lidah biru", "ujung jari biru",
        "sianosis", "oksigen rendah", "saturasi turun",
        "dada sesak berat", "napas ngik", "napas berbunyi keras"
    ],

    "pencernaan": [
        "nyeri perut hebat", "perut keras seperti papan", "perut tegang",
        "muntah darah", "muntah hitam seperti kopi",
        "muntah terus tidak bisa minum", "muntah tidak berhenti",
        "tidak bisa bab dan tidak bisa buang angin",
        "perut melilit hebat sekali", "sakit perut tak tertahankan",
        "keracunan makanan berat", "dehidrasi berat karena diare"
    ],

    "alergi": [
        "syok anafilaktik", "reaksi alergi berat",
        "bibir bengkak hebat", "mata bengkak besar",
        "tenggorokan terasa menutup", "sesak setelah makan",
        "sesak setelah minum obat", "seluruh badan merah dan bengkak",
        "pingsan setelah disengat lebah"
    ],
    
    "sirkulasi_jantung": [
        "nyeri dada hebat", "nyeri dada kiri", "dada terasa ditekan",
        "dada seperti ditimpa", "dada seperti diremas",
        "jantung berdebar hebat", "deg-degan parah",
        "aritmia", "denyut jantung tidak teratur",
        "nadi lemah", "nadi tidak teraba",
        "tangan kaki dingin", "akral dingin",
        "keringat dingin", "keringat jagung",
        "pucat sekali", "lemas mendadak",
        "syok", "shock",
        "pingsan karena jantung",
        "serangan jantung", "henti jantung",
        "tekanan darah turun drastis",
        "kolaps"
    ],

    "neurologis": [
        "pingsan", "tidak sadar", "hilang kesadaran",
        "tidak bisa dibangunkan", "mengantuk berat",
        "penurunan kesadaran",
        "kejang", "kejang-kejang", "step",
        "kejang lama", "kejang berulang",
        "linglung berat", "kebingungan mendadak",
        "bicara pelo", "bicara tidak jelas",
        "mulut miring", "wajah mencong",
        "lemas sebelah badan", "kelumpuhan",
        "setengah badan mati rasa",
        "stroke", "serangan stroke",
        "koma", "mata mendelik",
        "kaku kuduk", "leher kaku",
        "pandangan kabur mendadak",
        "tidak bisa bicara"
    ],

    "perdarahan": [
        "perdarahan hebat", "darah banyak", "darah mengalir",
        "muntah darah", "batuk darah",
        "bab berdarah", "berak berdarah",
        "bab hitam", "tinja hitam",
        "mimisan tidak berhenti",
        "kencing darah",
        "pendarahan vagina banyak",
        "darah segar keluar banyak",
        "pendarahan pasca melahirkan",
        "pendarahan hamil",
        "luka berdarah deras",
        "kehilangan banyak darah"
    ],

    "trauma_cedera": [
        "kecelakaan", "tabrakan", "jatuh keras",
        "jatuh dari ketinggian",
        "patah tulang", "tulang menonjol",
        "benturan kepala keras",
        "kepala terbentur",
        "luka robek besar", "luka dalam",
        "luka parah", "perdarahan luka",
        "luka bakar luas", "terbakar",
        "kesetrum", "tersetrum",
        "tenggelam", "hampir tenggelam",
        "tertancap benda", "kena tusuk",
        "digigit ular", "digigit anjing",
        "keracunan", "minum racun",
        "overdosis obat",
        "terpapar gas beracun"
    ],

    "kia": [
        "kejang kehamilan", "eklampsia",
        "tekanan darah tinggi hamil",
        "pendarahan hamil",
        "ketuban pecah dini",
        "ketuban pecah lama",
        "kontraksi hebat",
        "nyeri perut hamil hebat",
        "bayi tidak bernapas",
        "bayi biru",
        "bayi lemas sekali",
        "bayi tidak menangis",
        "bayi tidak mau minum",
        "anak kejang",
        "anak tidak sadar",
        "demam tinggi anak dengan kejang"
    ]
}

# ---------------------------------------------------------
# 3. MODERATE RISK (Kategori Kuning)
# ---------------------------------------------------------

MODERATE_RISK_KEYWORDS = [

    # Intensitas meningkat
    "nyeri parah", "nyeri berat", "sakit sekali", "tidak tertahankan",
    "makin parah", "semakin parah", "tambah parah", "memberat",
    "rasa sakit hebat tapi tertahan", "sakitnya kuat",

    # Durasi lama / tidak membaik
    "sudah 3 hari", "lebih dari 3 hari", "4 hari", "5 hari", "berhari-hari",
    "sudah lama", "lama tidak sembuh", "tidak kunjung sembuh",
    "belum membaik", "tidak ada perubahan", "gejala menetap",
    "tidak hilang-hilang",

    # Berulang / kambuh
    "berulang", "kambuh", "sering kambuh", "datang pergi",
    "hilang timbul", "bolak balik", "muncul lagi", "sering muncul",

    # Lemas & penurunan kondisi
    "lemas", "lemas sekali", "semakin lemas", "badan lunglai",
    "tidak bertenaga", "tenaga hilang", "badan drop",
    "lesu", "letoy", "nggreges", "capek berat",

    # Pusing & keseimbangan
    "pusing berputar", "vertigo", "kepala muter",
    "pusing saat berdiri", "kunang-kunang",
    "kepala melayang", "kliyengan", "limbung",

    # Dehidrasi / kurang cairan
    "kurang cairan", "jarang minum", "tidak bisa minum",
    "mulut kering", "bibir kering", "kencing sedikit",
    "air kencing sedikit", "warna kencing pekat",
    "dehidrasi", "haus terus",

    # Nafsu makan & muntah ringan menetap
    "tidak nafsu makan", "tidak mau makan",
    "makan sedikit", "muntah terus tapi sedikit",
    "mual tidak hilang", "eneg terus",

    # Aktivitas terganggu
    "tidak bisa aktivitas", "tidak bisa kerja",
    "tidak bisa sekolah", "hanya bisa tiduran",
    "aktivitas terganggu", "tidak kuat jalan",

    # Respons obat buruk
    "tidak mempan obat", "obat tidak bekerja",
    "minum obat tidak membaik", "tidak ada efek obat",
    "sudah minum obat tapi tetap sakit",

    # Tidur & istirahat
    "tidak bisa tidur karena sakit",
    "sulit tidur karena nyeri",
    "tidur tidak nyenyak",

    # Khusus anak & lansia (tanpa red flag)
    "anak rewel terus", "anak lemas", "anak tidak aktif",
    "lansia lemah", "orang tua lemas terus"
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