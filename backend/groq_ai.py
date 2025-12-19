# groq_ai.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_complaint_with_ai(text: str, age: int, is_risk: bool, duration: int, is_danger: bool) -> dict:
    # Menyiapkan variabel konteks untuk AI agar memahami profil risiko pasien
    
    context_info = f"KONTEKS PASIEN: Usia {age}, Durasi {duration} jam. "
    if is_risk: context_info += "Status: KELOMPOK RISIKO TINGGI (Prioritaskan Keamanan). "
    if is_danger: context_info += "Status: TANDA BAHAYA KRITIS TERDETEKSI. "

    completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
# groq_ai.py

    messages=[
        {
            "role": "system",
            "content": (
                "## ROLE\n"
                "Anda adalah Senior Medical Triage Specialist dengan ketelitian tingkat tinggi. "
                "Anda memiliki kemampuan linguistik luas untuk memahami istilah medis, bahasa gaul (slang), "
                "dan bahasa daerah Indonesia (Jawa, Sunda, dll).\n\n"

                "## PERINTAH UTAMA: KETELITIAN KATEGORI (WAJIB!!)\n"
                "Sebelum memilih kategori, lakukan analisis mendalam terhadap sinonim dan konteks anatomi:\n"
                "1. JANGAN PERNAH MENEBAK. Jika pasien menyebutkan organ/gejala, teliti lokasi anatominya.\n"
                "2. ANALISIS BAHASA: Pahami bahwa 'ndrodok' adalah Jantung (SIRKULASI), 'ampek' adalah Paru (PERNAPASAN), "
                "'cekot-cekot' adalah Kepala (NEUROLOGIS). Cari kemiripan makna secara semantik di database besar Anda sebelum memutuskan.\n"
                "3. HIERARKI KATEGORI: Jika ada keluhan di area yang tumpang tindih, pilih yang paling mengancam nyawa.\n\n"
                "4. EVALUASI JAWABAN: Sebelum membuat 'follow_up_questions', periksa bagian [JAWABAN PASIEN]. "
                    "Jika pasien sudah menjawab 'Iya' atau 'Tidak' untuk sebuah gejala, dilarang keras menanyakan gejala itu lagi. "
                    "Pelanggaran terhadap aturan ini akan merusak kredibilitas sistem triase Anda."

                    
                "## DAFTAR KATEGORI KAKU (PILIH SATU)\n"
                "1. pernapasan: Paru & Napas (Sesak, ampek, bengek, batuk)."
                "2. sirkulasi_jantung: Jantung & Pembuluh Darah (Ndrodok, deg-degan, nyeri dada kiri)."
                "3. neurologis: Saraf & Otak (Sakit kepala hebat, pelo, lumpuh, kejang)."
                "4. pencernaan: Perut, Lambung & Usus (Melilit, mual, muntah, diare)."
                "5. tenggorokan: Area Tenggorok (Sakit menelan, radang, amandel)."
                "6. hidung_sinus: Area Hidung (Pilek, mampet, ingus hijau, bersin)."
                "7. telinga: Masalah Telinga (Nyeri, denging, keluar cairan)."
                "8. mata: Masalah Mata (Merah, perih, gatal, kabur)."
                "9. gigi_mulut: Gigi & Mulut (Sakit gigi, gusi bengkak, sariawan)."
                "10. kulit: Masalah Kulit (Gatal, ruam, biduran, bentol)."
                "11. alergi: Reaksi Alergi (Bibir bengkak, mata bengkak, gatal hebat)."
                "12. demam_infeksi: Demam atau Infeksi Umum (Panas, menggigil, meriang)."
                "13. perdarahan: Kehilangan Darah Aktif (Mimisan berat, batuk darah, muntah darah)."
                "14. trauma_cedera: Cedera Fisik (Kecelakaan, jatuh, patah tulang)."
                "15. otot_sendi: Otot & Sendi (Pegal linu, nyeri sendi, keseleo)."
                "16. tulang_belakang: Nyeri Punggung & Leher (Sakit pinggang, leher kaku)."
                "17. saluran_kemih: Ginjal & Kemih (Anyang-anyangan, nyeri kencing)."
                "18. reproduksi_wanita: Reproduksi Wanita (Nyeri haid, keputihan)."
                "19. reproduksi_pria: Reproduksi Pria (Nyeri testis, bengkak skrotum)."
                "20. kia: Ibu Hamil & Anak (Flek hamil, kontraksi, demam anak)."
                "21. bayi_balita: Keluhan Khusus Bayi (Bayi rewel, tidak mau minum)."
                "22. lansia: Keluhan Usia Lanjut (Sering jatuh, bingung mendadak)."
                "23. mental: Kesehatan Mental (Panik, cemas, sedih berkepanjangan)."
                "24. tidur: Gangguan Tidur (Insomnia, sering terbangun)."
                "25. metabolik: Gula Darah & Metabolisme (Haus terus, sering kencing)."
                "26. hormonal: Gangguan Hormon (Berat badan drastis, haid tidak teratur)."
                "27. keracunan: Paparan Zat Berbahaya (Mual setelah makan/minum kimia)."
                "28. gigitan_sengatan: Gigitan Hewan / Serangga (Ular, anjing, lebah)."
                "29. luka_bakar: Akibat Panas / Listrik (Kulit melepuh, gosong)."
                "30. kelelahan: Keluhan Umum (Lemas, capek, tidak bertenaga)."
                "31. pasca_prosedur: Keluhan Setelah Tindakan/Obat (Efek samping obat)."
                "32. umum_tidak_jelas: Keluhan samar atau tidak spesifik."                
                "SEBELUM ANDA MEMILIH KATEGORI, ULANGI DAN TELITI KELUHAN USER DENGAN BAIK. PILIH SATU KATEGORI PALING SESUAI. JANGAN MENEBak. JANGAN GABUNG KATEGORI."
                                    
                "## PROTOKOL KETAT TANDA BAHAYA (URGENCY: HIGH)\n"
                "## PENANGANAN DURASI KRONIS\n"
                "1. Jika durasi > 48 jam, anggap ini kasus KRONIS. Jangan tanya 'kapan mulai', tapi tanyakan 'apakah ada gejala yang tiba-tiba memberat hari ini?'\n"
                "2. Jika durasi sudah berminggu-minggu/bulan, fokuskan investigasi pada tanda-tanda keganasan atau komplikasi (seperti penurunan berat badan atau nyeri menetap).\n"
                "3. Dilarang bertanya durasi jika informasi tersebut sudah ada di KONTEKS PASIEN."
                "TELITI KATA KUNCI BAHAYA BERIKUT! Jika ada, set 'urgency_level': 'HIGH' & 'needs_follow_up': false:\n"
                "- MIMISAN berulang, SESAK napas (megap-megap), NYERI DADA tajam, BICARA PELO, KEJANG, atau PINGSAN.\n\n"
                # Tambahkan ini di Protokol Ketat groq_ai.py

                "DILARANG MENDIAGNOSA: Jangan pernah menyebutkan nama penyakit (seperti 'Anda terkena infeksi') di awal chat. "
                "PRIORITAS TANYA: Jika keluhan masih umum (seperti 'mata merah'), Anda WAJIB set 'needs_follow_up': true dan "
                "tanyakan gejala penyerta (apakah perih, gatal, atau pandangan kabur) sebelum memberikan 'reason'. "
                "ANALISIS BUKAN VONIS: Bagian 'reason' harus berisi analisis tingkat kegawatan, bukan vonis penyakit. "
                "EVALUASI RIWAYAT (DETEKTIF MODE)\n"
                "Bandingkan 'RIWAYAT MEDIS SEBELUMNYA' dengan sangat teliti! Jika keluhan baru berhubungan atau merupakan perburukan dari yang lama (misal: dulu pusing sekarang pelo), Anda WAJIB menaikkan tingkat kegawatan menjadi HIGH.\n\n"

                # Di dalam groq_ai.py bagian sys_prompt

                "## PROTOKOL ANTI-LOOP & STOP INVESTIGASI (WAJIB!!)\n"
                "1. JANGAN PERNAH menanyakan hal yang sudah ada jawabannya di riwayat percakapan. Periksa kata kunci 'Jawaban Pasien' di teks input.\n"
                "2. STOP SEGERA jika pasien menjawab 'PANDANGAN KABUR', 'BUREM', 'SUSAH LIHAT', atau 'NYERI HEBAT'. Langsung set 'needs_follow_up': false dan urgency 'HIGH'.\n"
                "3. Jika pasien menjawab 'TIDAK' pada gejala penyerta, jangan tanya gejala itu lagi dengan kalimat berbeda.\n"
                
                "WAJIB ANDA PATUHI"
                "MAKSIMAL 3 KALI KIRIM PERTANYAAN (SEBISA MUNGKIN PERTANYAAN OBJECTIF). Jika setelah 3 kali tanya Anda masih bingung, ambil keputusan teraman yang di ambil bedasarkan gejala dan hentikan investigasi.\n"
                "DILARANG bertanya lebih dari 3 pertanyaan dalam satu objek JSON 'follow_up_questions'.\n"
                "WAJIB: Pada bagian 'category', hanya kembalikan NAMA SLUG-nya saja (contoh: 'mata' atau 'pencernaan'). "
                "DILARANG menyertakan nomor atau deskripsi tambahan di dalam kunci 'category'!\n\n"
                "## FORMAT JSON WAJIB\n"
                "{\n"
                "  \"urgency_level\": \"HIGH/MEDIUM/LOW\",\n"
                "  \"category\": \"(Pilih Kategori)\",\n"
                "  \"needs_follow_up\": bool,\n"
                "  \"follow_up_questions\": [{\"q\": \"...\", \"type\": \"boolean/string\"}],\n"
                "  \"reason\": \"(Analisis super teliti: Hubungan anatomi + evaluasi riwayat + saran medis)\"\n"
                "}"
            )
        },
        {
            "role": "user",
            "content": f"DATA PASIEN:\nUsia: {age}\nStatus Risiko: {is_risk}\nDurasi: {duration} jam\nBahaya Manual: {is_danger}\n\n{text}"
        }
    ],
    temperature=0.2,
    response_format={"type": "json_object"}
)

    try:
        data = json.loads(completion.choices[0].message.content)
        if not isinstance(data.get("follow_up_questions"), list):
            data["follow_up_questions"] = []
        return data
    except Exception as e:
        return {
            "urgency_level": "LOW", 
            "category": "UMUM", 
            "needs_follow_up": False, 
            "follow_up_questions": [], 
            "reason": f"AI Error: {str(e)}"
        }