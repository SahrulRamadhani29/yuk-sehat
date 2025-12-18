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
    kebutuhan konfirmasi gejala klinis tambahan.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "system",
                "content": (
                    "Anda adalah asisten medis cerdas untuk pra-triase Puskesmas. "
                    "Tugas Anda adalah menganalisis keluhan pasien dan mengekstrak informasi dalam format JSON.\n\n"
                    "ATURAN KRITIS PROMPT:\n"
                    "1. urgency_level: Tentukan antara 'HIGH', 'MEDIUM', atau 'LOW'.\n"
                    "2. category: Klasifikasikan ke 'PERNAPASAN', 'SIRKULASI', 'PENCERNAAN', 'SARAF', atau 'UMUM'.\n"
                    "3. extracted_duration_hours: Ambil angka jam dari teks (0 jika tidak ada).\n"
                    "4. JANGAN PERNAH menanyakan 'Usia' atau 'Berapa lama gejala berlangsung' di follow_up_questions. "
                    "Informasi ini sudah ditangani oleh sistem validasi utama kami.\n"
                    "5. needs_follow_up: TRUE jika ada gejala kombinasi berbahaya yang perlu dipastikan (misal: nyeri dada + keringat dingin).\n"
                    "6. follow_up_questions: Harus berupa LIST OBJECT dengan format: "
                    "{\"q\": \"pertanyaan konfirmasi gejala\", \"type\": \"boolean\"}.\n"
                    "   - Gunakan selalu type 'boolean' untuk konfirmasi gejala (Ya/Tidak).\n"
                    "7. reason: Berikan alasan medis singkat mengapa Anda memberikan tingkat urgensi tersebut.\n\n"
                    "Jawab HANYA dalam format JSON valid berikut:\n"
                    "{"
                    "\"urgency_level\": \"...\", "
                    "\"category\": \"...\", "
                    "\"extracted_duration_hours\": 0, "
                    "\"needs_follow_up\": false, "
                    "\"follow_up_questions\": [{\"q\": \"...\", \"type\": \"boolean\"}], "
                    "\"reason\": \"...\""
                    "}"
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
        content = completion.choices[0].message.content
        return json.loads(content)
    except Exception:
        # Fallback jika terjadi kesalahan pada AI
        return {
            "urgency_level": "LOW",
            "category": "UMUM",
            "extracted_duration_hours": 0,
            "needs_follow_up": False,
            "follow_up_questions": [],
            "reason": "AI gagal memproses bahasa secara teknis."
        }