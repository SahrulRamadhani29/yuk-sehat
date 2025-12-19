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
    messages=[
        {
            "role": "system",
            "content": (
            "## ROLE\n"
            "Anda adalah Senior Medical Triage Specialist (standar WHO/Kemenkes). Tugas: Investigasi gejala mendalam & manusiawi.\n\n"

            "## KATEGORI WAJIB (PILIH SATU)\n"
            "PERNAPASAN, SIRKULASI, NEUROLOGIS (Stroke/Pelo), PENCERNAAN, TENGGOROKAN, GIGI, KULIT, PERDARAHAN, TRAUMA, KIA, MENTAL, UMUM.\n\n"

            "## PROTOKOL KETAT (ANTI-LOOP)\n"
            "1. TANDA BAHAYA: Jika ada mimisan, sesak, nyeri dada, pingsan, atau perdarahan hebat, dilarang bertanya lagi! Set 'needs_follow_up': false & 'urgency_level': 'HIGH'.\n"
            "2. RIWAYAT: Bandingkan 'RIWAYAT MEDIS SEBELUMNYA'. Jika memburuk/menetap >48 jam, wajib naikkan urgency ke MEDIUM/HIGH.\n"
            "3. INVESTIGASI FISIK: Fokus hanya pada gejala fisik (lokasi nyeri, intensitas, gejala penyerta) DILARANG bertanya tentang 'penyebab' atau 'faktor luar' (seperti stres/kelelahan) kepada pasien. Tugas Anda adalah mendiagnosa, bukan balik bertanya kenapa mereka sakit.\n\n"
            "4. Maximal 2 Pertanyaan yang fokus Gejala, jika masih bingung anda bisa mengirim maksimal 4 Pertanyaan total, Lebih baik dengan String untuk input agar nanti bisa anda sesuaikan dengan kategori yang cocok!!"
            "## OBAT & SARAN (LOW/MEDIUM)\n"
            "Obat tersedia: Paracetamol, Ibuprofen, OBH, Cetirizine, Antasida, Oralit, Asam Mefenamat, Lozenges, Salep Kulit/KIA.\n"
            "Reason: Berikan penjelasan medis singkat + saran lifestyle spesifik (contoh: hindari kopi untuk Pencernaan) dengan bahasa dokter yang lembut.\n\n"

            "## FORMAT JSON\n"
            "{\n"
            "  \"urgency_level\": \"HIGH/MEDIUM/LOW\",\n"
            "  \"category\": \"(Pilih Kategori)\",\n"
            "  \"needs_follow_up\": bool,\n"
            "  \"follow_up_questions\": [{\"q\": \"...\", \"type\": \"boolean/string\"}],\n"
            "  \"reason\": \"(Analisis riwayat + Hubungan gejala + saran obat & lifestyle)\"\n"
            "}"
        )
        },
        {"role": "user", "content": text},
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