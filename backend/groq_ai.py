# groq_ai.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_complaint_with_ai(text: str) -> dict:
    """
    AI sebagai NLU: Mengubah teks bebas menjadi data JSON terstruktur.
    AI TIDAK menentukan warna triase, hanya level urgensi dan kategori.
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah sistem NLU untuk pra-triase medis Puskesmas. "
                    "Tugasmu mengekstrak informasi kunci dari keluhan pasien. "
                    "Tentukan urgency_level: 'HIGH' (jika ada tanda bahaya nyata), "
                    "'MEDIUM' (gejala sedang atau perlu perhatian), 'LOW' (gejala ringan). "
                    "Tentukan category: 'PERNAPASAN', 'SIRKULASI', 'PENCERNAAN', 'SARAF', atau 'UMUM'. "
                    "Jawab dalam JSON: "
                    "{\"urgency_level\": \"...\", \"category\": \"...\", \"reason\": \"...\"}"
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
            "reason": "AI gagal memproses bahasa"
        }