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
    kebutuhan konfirmasi gejala dengan tipe input yang spesifik untuk frontend.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "system",
                "content": (
                    "Anda adalah asisten medis cerdas untuk pra-triase Puskesmas. "
                    "Analisis teks keluhan pasien dan ekstrak informasi dalam format JSON.\n\n"
                    "ATURAN PENTING:\n"
                    "1. urgency_level: 'HIGH', 'MEDIUM', 'LOW'.\n"
                    "2. category: 'PERNAPASAN', 'SIRKULASI', 'PENCERNAAN', 'SARAF', atau 'UMUM'.\n"
                    "3. extracted_duration_hours: angka int jam (0 jika tidak disebutkan).\n"
                    "4. needs_follow_up: boolean. TRUE jika informasi kritis seperti usia atau durasi hilang, "
                    "atau jika ada gejala kombinasi yang perlu dipastikan.\n"
                    "5. follow_up_questions: Harus berupa LIST OBJECT dengan format: "
                    "{\"q\": \"pertanyaan\", \"type\": \"boolean\" atau \"number\"}.\n"
                    "   - Gunakan 'number' untuk pertanyaan durasi, usia, atau suhu.\n"
                    "   - Gunakan 'boolean' untuk konfirmasi gejala (Ya/Tidak).\n"
                    "6. reason: string alasan medis singkat.\n\n"
                    "Jawab HANYA dalam JSON valid: "
                    "{\"urgency_level\": \"...\", \"category\": \"...\", \"extracted_duration_hours\": 0, "
                    "\"needs_follow_up\": false, \"follow_up_questions\": [{\"q\": \"...\", \"type\": \"...\"}], \"reason\": \"...\"}"
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
        return {
            "urgency_level": "LOW",
            "category": "UMUM",
            "extracted_duration_hours": 0,
            "needs_follow_up": False,
            "follow_up_questions": [],
            "reason": "AI gagal memproses bahasa"
        }