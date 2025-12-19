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
OTC_MAP: Dict[str, List[str]] = {

    "demam_ringan": [
        "Paracetamol 500 mg: 1 tablet setiap 6–8 jam (maks 4.000 mg/hari)",
        "Kompres hangat di area lipatan tubuh (ketiak/leher) selama 15 menit",
        "Gunakan pakaian tipis berbahan katun dan jaga sirkulasi udara ruangan",
        "Perbanyak minum air putih (minimal 2-3 liter/hari) untuk mencegah dehidrasi",
        "Istirahat total (Bedrest) untuk mempercepat pemulihan"
    ],

    "batuk_pilek": [
        "Obat Batuk Hitam (OBH) atau sirup batuk ekspektoran sesuai aturan pakai",
        "Dekongestan (Pseudoefedrin) jika hidung sangat tersumbat (Hanya lingkaran biru)",
        "Tablet hisap antiseptik (Lozenges) untuk melegakan jalan napas",
        "Minum air hangat dan hindari gorengan, santan, atau minuman dingin",
        "Gunakan masker dan cuci tangan rutin agar tidak menulari orang lain",
        "Uap wajah sederhana dengan air panas untuk mengencerkan lendir"
    ],

    "sakit_kepala_ringan": [
        "Paracetamol 500 mg atau Ibuprofen 400 mg (Diminum sesudah makan)",
        "Istirahat di ruangan yang tenang, gelap (minim cahaya), dan sejuk",
        "Pijat ringan di area pelipis atau belakang leher",
        "Pastikan asupan cairan cukup dan hindari paparan layar gadget (HP/Laptop)",
        "Kompres dingin di dahi untuk meredakan denyut kepala"
    ],

    "nyeri_otot_ringan": [
        "Paracetamol 500 mg atau Asam Mefenamat 500 mg (Jika nyeri terasa tajam)",
        "Salep/Balsem otot atau gel yang mengandung Methyl Salicylate/Diclofenac",
        "Koyo atau kompres hangat pada area yang pegal untuk relaksasi otot",
        "Istirahatkan bagian tubuh yang nyeri dan hindari mengangkat beban berat",
        "Lakukan peregangan (stretching) ringan jika tidak ada bengkak"
    ],

    "nyeri_tenggorokan": [
        "Permen pelega tenggorokan (Lozenges) setiap 3-4 jam sekali",
        "Kumur air garam hangat (1/2 sdt garam dalam segelas air) 3 kali sehari",
        "Minum campuran air jeruk nipis hangat dengan madu murni",
        "Hindari rokok, polusi udara, dan makanan yang mengiritasi (pedas/berminyak)",
        "Istirahatkan suara (tidak banyak bicara) jika terasa serak"
    ],

    "sakit_gigi": [
        "Asam Mefenamat 500 mg: 1 tablet setiap 6-8 jam (Sesudah makan)",
        "Paracetamol 500 mg sebagai alternatif pereda nyeri jika alergi NSAID",
        "Kumur air garam hangat untuk membersihkan sisa makanan di lubang gigi",
        "Hindari makanan/minuman yang terlalu manis, terlalu dingin, atau keras",
        "Kompres dingin pada pipi jika mulai terasa sedikit bengkak"
    ],

    "diare_ringan": [
        "Oralit: 1 sachet (larutkan dalam 200 ml air) setiap kali sehabis BAB",
        "Tablet Zinc 20 mg: 1 tablet sehari selama 10 hari (Penting untuk usus)",
        "Attapulgite atau Karbon Aktif untuk menyerap racun dan memadatkan feses",
        "Makan makanan lunak (bubur ayam/pisang/roti tawar) dan hindari susu/kafein",
        "Jaga kebersihan tangan sebelum dan sesudah makan"
    ],

    "mual_ringan": [
        "Antasida DOEN: 1-2 tablet kunyah 1 jam sebelum makan atau saat perut kosong",
        "Minum air jahe hangat atau teh peppermint untuk menenangkan lambung",
        "Makan dengan porsi kecil tapi sering (misal: 5-6 kali sehari)",
        "Hindari posisi berbaring langsung (tunggu 2 jam) setelah makan",
        "Hindari makanan pemicu gas seperti kol, sawi, dan minuman bersoda"
    ],

    "masalah_kulit_ringan": [
        "Bedak Salisil atau Losion Kalamin untuk gatal biang keringat atau biduran",
        "Krim Antihistamin (Hanya lingkaran biru) jika gatal karena alergi gigitan serangga",
        "Salep Antiseptik (Povidone Iodine) untuk luka lecet atau luka kecil",
        "Jaga kulit tetap kering, bersih, dan gunakan pakaian longgar berbahan katun",
        "Jangan menggaruk area yang gatal untuk mencegah infeksi sekunder"
    ],

    "sembelit_konstipasi": [
        "Obat pencahar ringan (Laktulosa atau Bisakodil) jika tidak BAB > 3 hari",
        "Tingkatkan konsumsi serat secara signifikan (Sayuran hijau dan buah pepaya)",
        "Minum air putih minimal 8-10 gelas sehari secara teratur",
        "Lakukan aktivitas fisik ringan atau jalan pagi untuk merangsang gerak usus",
        "Jangan membiasakan menahan keinginan Buang Air Besar"
    ],
    
    "kesehatan_mental_ringan": [
        "Lakukan teknik pernapasan dalam (4-7-8) untuk meredakan kecemasan",
        "Kurangi asupan kafein (kopi/teh) dan gula yang dapat memicu detak jantung",
        "Lakukan rutinitas 'Sleep Hygiene': Matikan gadget 1 jam sebelum tidur",
        "Tuliskan perasaan Anda di buku jurnal (Journaling) untuk meredakan beban pikiran",
        "Dengarkan musik relaksasi atau suara alam untuk membantu tidur"
    ],

    "kesehatan_ibu_anak": [
        "Kompres hangat pada perut bawah untuk meredakan nyeri haid (Dismenore)",
        "Gunakan krim barrier (Zinc Oxide) untuk ruam popok pada bayi",
        "Untuk mual kehamilan: Konsumsi biskuit gandum atau crackers saat bangun pagi",
        "Paracetamol (Hanya jika sangat perlu) adalah pilihan teraman untuk ibu hamil",
        "Konsumsi banyak cairan dan makanan bergizi untuk mendukung produksi ASI",
        "PENTING: Segera hubungi bidan/dokter jika ada pendarahan atau kontraksi hebat"
    ],
    
    "alergi_ringan": [
        "Cetirizine 10 mg: 1 tablet sehari (Perhatian: Dapat menyebabkan kantuk)",
        "Hindari pemicu alergi yang sudah diketahui (Debu, bulu hewan, suhu dingin)",
        "Kompres dingin atau mandi air biasa pada area kulit yang bentol/merah",
        "Gunakan sabun bayi yang tidak mengandung parfum jika kulit sangat sensitif"
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