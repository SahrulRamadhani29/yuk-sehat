# groq_ai.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_complaint_with_ai(text: str) -> dict:
    """
    AI sebagai NLU: Mengekstrak urgensi, kategori, durasi, dan mendeteksi 
    kebutuhan konfirmasi gejala kombinasi yang berbahaya.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten medis cerdas untuk pra-triase Puskesmas. "
                    "Analisis teks keluhan pasien dan ekstrak informasi berikut dalam format JSON:\n"
                    "1. urgency_level: 'HIGH' (tanda bahaya nyata/ancaman nyawa), "
                    "'MEDIUM' (gejala sedang/risiko), 'LOW' (gejala ringan/stabil).\n"
                    "2. category: 'PERNAPASAN', 'SIRKULASI', 'PENCERNAAN', 'SARAF', atau 'UMUM'.\n"
                    "3. extracted_duration_hours: Prediksi durasi dalam jam dari teks (misal: '2 hari' = 48). Jika tidak ada, isi 0.\n"
                    "4. needs_follow_up: boolean (true jika ada gejala yang mencurigakan tapi butuh konfirmasi lebih lanjut).\n"
                    "5. follow_up_questions: Daftar pertanyaan singkat (maks 2) jika ada gejala kombinasi yang berbahaya.\n"
                    "   Contoh: Jika 'Nyeri Ulu Hati', tanya: 'Apakah Anda juga berkeringat dingin?'.\n"
                    "6. reason: Penjelasan singkat alasan medisnya.\n\n"
                    "Format Jawaban JSON:\n"
                    "{\"urgency_level\": \"...\", \"category\": \"...\", \"extracted_duration_hours\": 0, "
                    "\"needs_follow_up\": false, \"follow_up_questions\": [], \"reason\": \"...\"}"
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )

    try:
        return json.loads(completion.choices[0].message.content)
    except Exception:
        return {
            "urgency_level": "LOW",
            "category": "UMUM",
            "extracted_duration_hours": 0,
            "needs_follow_up": false,
            "follow_up_questions": [],
            "reason": "AI gagal memproses bahasa"
        }