# otc_recommendation.py
# =========================================================
# OTC RECOMMENDATION WITH SAFE GENERAL DOSING (EDUCATIONAL)
# Berdasarkan Pedoman Kemenkes & BPOM Indonesia
#
# PENTING:
# - Hanya untuk gejala ringan (Hijau/Kuning)
# - Dosis umum dewasa (Kecuali disebutkan khusus KIA)
# - Baca label kemasan (Lingkaran Hijau/Biru)
# - Segera ke Puskesmas jika gejala memburuk
# =========================================================

from typing import List, Dict

# ---------------------------------------------------------
# OTC RECOMMENDATION MAP DENGAN VARIASI LENGKAP
# ---------------------------------------------------------
# Kunci di sini harus selaras dengan SYMPTOM_MAP di symptom_catalog.py
# otc_recommendation.py
OTC_MAP: Dict[str, List[str]] = {
    "pernapasan": [
        "Sirup batuk ekspektoran atau antitusif sesuai keluhan",
        "Tablet hisap tenggorokan (lozenges)",
        "Minum air hangat dan perbanyak cairan",
        "Uap air hangat untuk melegakan hidung",
        "Gunakan masker dan istirahat cukup"
    ],
    "sirkulasi_jantung": [
        "Istirahat total dan hindari aktivitas berat",
        "Posisikan tubuh duduk atau berbaring nyaman",
        "Hindari kopi, rokok, dan minuman berenergi",
        "Lakukan teknik relaksasi pernapasan"
    ],
    "neurologis": [
        "Paracetamol 500 mg atau Ibuprofen 400 mg (sesudah makan)",
        "Istirahat di ruangan tenang dan minim cahaya",
        "Kompres dingin di dahi atau pelipis"
    ],
    "pencernaan": [
        "Antasida DOEN bila nyeri ulu hati atau kembung",
        "Simetikon untuk mengurangi gas di perut",
        "Makan porsi kecil tapi sering",
        "Hindari makanan pedas, asam, dan berlemak"
    ],
    "tenggorokan": [
        "Permen pelega tenggorokan (lozenges)",
        "Kumur air garam hangat 2–3 kali sehari",
        "Minum air hangat atau madu"
    ],
    "hidung_sinus": [
        "Obat semprot hidung saline (air garam steril)",
        "Uap air hangat untuk melegakan sumbatan",
        "Cukupi asupan cairan"
    ],
    "telinga": [
        "Hindari memasukkan benda apapun ke telinga",
        "Tetes telinga pelunak kotoran (jika hanya tersumbat)",
        "Paracetamol bila nyeri ringan"
    ],
    "mata": [
        "Tetes mata steril (artificial tears) untuk iritasi",
        "Kompres dingin pada mata yang teriritasi",
        "Hindari mengucek mata dengan tangan",
        "Gunakan kacamata pelindung bila berdebu"
    ],
    "gigi_mulut": [
        "Kumur air garam hangat untuk gusi bengkak",
        "Asam Mefenamat atau Paracetamol untuk nyeri gigi",
        "Jaga kebersihan mulut dengan sikat gigi lembut"
    ],
    "kulit": [
        "Losion kalamin atau bedak salisil untuk gatal",
        "Krim antihistamin topikal untuk alergi kulit",
        "Jaga kulit tetap kering dan bersih"
    ],
    "alergi": [
        "Cetirizine 10 mg 1x sehari",
        "Hindari pemicu alergi (debu/makanan/dingin)",
        "Kompres dingin pada area gatal/bentol"
    ],
    "demam_infeksi": [
        "Paracetamol 500 mg: 1 tablet tiap 6–8 jam",
        "Kompres hangat pada ketiak atau leher",
        "Perbanyak minum air putih"
    ],
    "otot_sendi": [
        "Salep/balsem otot pada area nyeri",
        "Kompres hangat atau koyo",
        "Istirahatkan area yang nyeri"
    ],
    "saluran_kemih": [
        "Perbanyak minum air putih",
        "Jangan menahan buang air kecil",
        "Paracetamol bila nyeri ringan"
    ],
    "reproduksi_wanita": [
        "Paracetamol atau Ibuprofen untuk nyeri haid",
        "Kompres hangat perut bawah",
        "Istirahat cukup"
    ],
    "reproduksi_pria": [
        "Gunakan pakaian dalam longgar",
        "Istirahat dan hindari aktivitas berat",
        "Jaga kebersihan area genital"
    ],
    "kia": [
        "Paracetamol sirup sesuai dosis usia anak",
        "Pastikan asupan ASI/minum tetap lancar",
        "Pantau aktivitas dan suhu tubuh anak"
    ],
    "bayi_balita": [
        "ASI lebih sering atau susu formula sesuai jadwal",
        "Oralit bila diare ringan/BAB cair",
        "Pantau tanda dehidrasi (ubun-ubun cekung/lemas)"
    ],
    "lansia": [
        "Minum air putih sedikit tapi sering",
        "Makan makanan lunak dan bergizi",
        "Pantau kondisi umum dan kesadaran"
    ],
    "mental": [
        "Latihan pernapasan relaksasi (box breathing)",
        "Kurangi kafein dan gula",
        "Istirahat cukup dan teratur"
    ],
    "tidur": [
        "Hindari gadget 1 jam sebelum tidur",
        "Minum teh herbal hangat (chamomile) tanpa kafein",
        "Ciptakan suasana kamar yang gelap dan tenang"
    ],
    "metabolik": [
        "Atur pola makan rendah gula",
        "Minum air putih cukup",
        "Istirahat cukup"
    ],
    "hormonal": [
        "Tidur teratur dan olahraga ringan",
        "Kurangi stres berlebih",
        "Makan bergizi seimbang"
    ],
    "keracunan": [
        "Minum air putih perlahan tapi sering",
        "Hentikan konsumsi pemicu segera",
        "Istirahat dan pantau tanda bahaya"
    ],
    "gigitan_sengatan": [
        "Cuci area gigitan dengan sabun dan air",
        "Kompres dingin untuk kurangi bengkak",
        "Losion kalamin untuk rasa gatal"
    ],
    "luka_bakar": [
        "Aliri luka dengan air mengalir suhu normal 15 menit",
        "Tutup dengan kasa bersih tanpa ditekan",
        "Jangan oles odol atau mentega"
    ],
    "kelelahan": [
        "Istirahat cukup dan kurangi beban kerja",
        "Cukupi kebutuhan cairan dan nutrisi",
        "Multivitamin bila perlu"
    ],
    "pasca_prosedur": [
        "Jaga area bekas tindakan tetap kering",
        "Paracetamol bila nyeri ringan",
        "Ikuti saran dokter yang menangani"
    ]
}

# ---------------------------------------------------------
# GET OTC RECOMMENDATION FUNCTION
# ---------------------------------------------------------

def get_otc_recommendations(symptom_keys: list[str]) -> list[str]:
    """
    Menggabungkan rekomendasi obat dari berbagai kategori gejala yang ditemukan.
    Mencegah duplikasi item dan memberikan peringatan medis yang sesuai.
    """
    recommendations = []
    seen_items = set() 

    for key in symptom_keys:
        items = OTC_MAP.get(key, [])
        for item in items:
            if item not in seen_items:
                recommendations.append(item)
                seen_items.add(item)

    # Tambahkan disclaimer umum dan khusus di akhir jika ada rekomendasi
    if recommendations:
        recommendations.append("--- PERINGATAN MEDIS (WAJIB BACA) ---")
        recommendations.append("1. Obat Bebas Terbatas (Lingkaran Biru) memiliki aturan pakai khusus, baca label!")
        recommendations.append("2. Jika gejala menetap > 48 jam, bertambah parah, atau muncul tanda bahaya, segera ke Puskesmas/RS.")
        recommendations.append("3. Obat ini hanya pereda gejala sementara (simtomatik), bukan pengganti diagnosa dokter.")
        recommendations.append("4. Khusus kategori KUNING: Anda sangat disarankan melakukan pemeriksaan fisik ke tenaga medis.")

    return recommendations