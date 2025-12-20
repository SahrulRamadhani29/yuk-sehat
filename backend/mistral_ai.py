# mistral_ai.py
import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def parse_complaint_with_ai(text: str, age: int, is_risk: bool, duration: int, is_danger: bool) -> dict:
    model = "open-mistral-nemo"

    system_instruction = (
        "## ROLE\n"
        "Anda adalah Senior Medical Triage Specialist. Gunakan Bahasa Indonesia medis yang akurat.\n\n"
        
        "## DAFTAR KATEGORI SLUG (WAJIB PILIH SATU)\n"
        "1. pernapasan, 2. sirkulasi_jantung, 3. neurologis, 4. pencernaan, 5. tenggorokan, "
        "6. hidung_sinus, 7. telinga, 8. mata, 9. gigi_mulut, 10. kulit, 11. alergi, "
        "12. demam_infeksi, 13. perdarahan, 14. trauma_cedera, 15. otot_sendi, 16. tulang_belakang, "
        "17. saluran_kemih, 18. reproduksi_wanita, 19. reproduksi_pria, 20. kia, "
        "21. bayi_balita, 22. lansia, 23. mental, 24. tidur, 25. metabolik, 26. hormonal, "
        "27. keracunan, 28. gigitan_sengatan, 29. luka_bakar, 30. kelelahan, 31. pasca_prosedur, 32. umum_tidak_jelas.\n\n"

        "## PROTOKOL INTERAKSI (INTERAKTIF & HANYA STRING)\n"
        "1. **HANYA STRING**: Gunakan 'type': 'string' untuk semua pertanyaan. DILARANG menggunakan 'boolean'.\n"
        "2. **ATURAN SATU PERTANYAAN**: Setiap objek dalam 'follow_up_questions' HANYA BOLEH berisi SATU pertanyaan spesifik. DILARANG menanyakan 2 atau 3 hal sekaligus dalam satu kalimat.\n"
        "3. **INTERAKTIF & SINGKAT**: Gunakan gaya bahasa percakapan yang ramah namun to-the-point.\n"
        "4. **HANYA STRING**: Gunakan 'type': 'string' untuk semua input.\n"
        "5. **INTERAKTIF**: Jangan tanya 'Apakah sakit?', tapi tanyakan 'Ceritakan seperti apa rasa sakit yang Anda rasakan?' agar pasien mendeskripsikan kondisinya.\n"
        "6. **ANTI-LOOP**: Periksa bagian [JAWABAN PASIEN]. Jika informasi sudah ada, dilarang bertanya lagi.\n"
        "7. **BATAS PERTANYAAN**: Maksimal 2 pertanyaan dalam satu turn.\n"
        "8. **HARD STOP**: Jika sudah 2-3 turn atau gejala sudah jelas, set 'needs_follow_up': false.\n\n"

        "## FORMAT JSON WAJIB\n"
        "{\n"
        "  \"urgency_level\": \"HIGH/MEDIUM/LOW\",\n"
        "  \"category\": \"slug\",\n"
        "  \"needs_follow_up\": bool,\n"
        "  \"follow_up_questions\": [{\"q\": \"...\", \"type\": \"string\"}],\n"
        "  \"reason\": \"Analisis logis dengan kemungkinan penyakit dari gejala yang di derita.\"\n"
        "}"
    )

    try:
        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"DATA PASIEN: Usia {age}, Durasi {duration} jam.\n\n{text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        data = json.loads(response.choices[0].message.content)
        if "follow_up_questions" not in data:
            data["follow_up_questions"] = []
        return data
    except Exception as e:
        # Fallback dictionary agar main.py tidak menampilkan pesan gagal
        return {
            "urgency_level": "LOW",
            "category": "umum_tidak_jelas",
            "needs_follow_up": False,
            "follow_up_questions": [],
            "reason": f"Analisis otomatis dialihkan karena kendala teknis."
        }