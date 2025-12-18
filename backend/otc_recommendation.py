# otc_recommendation.py
# =========================================================
# OTC RECOMMENDATION WITH SAFE GENERAL DOSING (EDUCATIONAL)
# Berdasarkan Pedoman Kemenkes & BPOM Indonesia
#
# PENTING:
# - Hanya untuk gejala ringan (Hijau/Kuning)
# - Dosis umum dewasa
# - Baca label kemasan (Lingkaran Hijau/Biru)
# - Segera ke Puskesmas jika gejala memburuk
# =========================================================

from typing import List, Dict

# ---------------------------------------------------------
# OTC RECOMMENDATION MAP DENGAN VARIASI LENGKAP
# ---------------------------------------------------------
OTC_MAP: Dict[str, List[str]] = {

    "demam_ringan": [
        "Paracetamol 500 mg: 1 tablet setiap 6–8 jam (maks 4.000 mg/hari)",
        "Kompres hangat di area lipatan tubuh (ketiak/leher)",
        "Gunakan pakaian tipis dan jaga sirkulasi udara",
        "Perbanyak minum air putih untuk mencegah dehidrasi"
    ],

    "batuk_pilek": [
        "Obat Batuk Hitam (OBH) atau sirup batuk OTC sesuai aturan pakai",
        "Dekongestan (Pseudoefedrin) jika hidung sangat tersumbat",
        "Tablet hisap antiseptik untuk melegakan jalan napas",
        "Minum air hangat dan hindari gorengan/minuman dingin",
        "Gunakan masker agar tidak menulari orang lain"
    ],

    "sakit_kepala_ringan": [
        "Paracetamol 500 mg atau Ibuprofen 400 mg (diminum sesudah makan)",
        "Istirahat di ruangan yang tenang dan minim cahaya",
        "Pijat ringan di area pelipis",
        "Pastikan asupan cairan cukup"
    ],

    "nyeri_otot_ringan": [
        "Paracetamol 500 mg atau asam mefenamat 500 mg (jika nyeri)",
        "Salep/Balsem otot yang mengandung Methyl Salicylate",
        "Koyo atau kompres hangat pada area yang pegal",
        "Istirahatkan bagian tubuh yang nyeri"
    ],

    "nyeri_tenggorokan": [
        "Permen pelega tenggorokan (Lozenges) setiap 3 jam",
        "Kumur air garam hangat 2-3 kali sehari",
        "Minum air jeruk nipis hangat dengan madu",
        "Hindari rokok dan polusi udara"
    ],

    "diare_ringan": [
        "Oralit: 1 sachet (200 ml air) setiap kali sehabis Buang Air Besar",
        "Tablet Zinc 20 mg (10 hari berturut-turut sesuai anjuran)",
        "Attapulgite atau Karbon Aktif untuk menyerap racun di usus",
        "Makan makanan lunak (bubur/pisang) dan hindari susu sementara"
    ],

    "mual_ringan": [
        "Antasida DOEN: 1-2 tablet kunyah 1 jam sebelum makan",
        "Minum air jahe hangat untuk menenangkan lambung",
        "Makan dengan porsi kecil tapi sering",
        "Hindari posisi berbaring langsung setelah makan"
    ],

    "masalah_kulit_ringan": [
        "Bedak Salisil atau Losion Kalamin untuk gatal biang keringat",
        "Krim Antihistamin (setelah konsultasi) jika gatal karena alergi",
        "Salep Antiseptik untuk luka lecet kecil",
        "Jaga kulit tetap kering dan gunakan pakaian longgar"
    ],

    "sembelit_konstipasi": [
        "Obat pencahar pencahar ringan (Laktulosa) jika diperlukan",
        "Tingkatkan konsumsi serat (sayur dan buah)",
        "Minum minimal 8 gelas air sehari",
        "Lakukan aktivitas fisik ringan untuk merangsang usus"
    ],
    
    "alergi_ringan": [
        "Cetirizine 10 mg: 1 tablet sehari (dapat menyebabkan kantuk)",
        "Hindari pemicu alergi (debu, dingin, makanan tertentu)",
        "Kompres dingin pada area kulit yang bentol/gatal"
    ]
}

# ---------------------------------------------------------
# GET OTC RECOMMENDATION FUNCTION
# ---------------------------------------------------------
def get_otc_recommendations(symptom_keys: list[str]) -> list[str]:
    """
    Menggabungkan rekomendasi obat dari berbagai kategori gejala yang ditemukan.
    Menghapus duplikasi jika ada obat yang sama di kategori berbeda.
    """
    recommendations = []

    for key in symptom_keys:
        items = OTC_MAP.get(key, [])
        for item in items:
            if item not in recommendations:
                recommendations.append(item)

    # Tambahkan disclaimer umum di akhir jika ada rekomendasi
    if recommendations:
        recommendations.append("CATATAN: Segera ke Puskesmas jika gejala menetap > 48 jam.")

    return recommendations