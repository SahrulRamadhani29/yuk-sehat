# main.py
from fastapi import FastAPI, HTTPException
from database import SessionLocal
from models import TriageLog
from schemas import TriageInput
from database import engine, Base

# Import logika dari file pendukung
from rules import is_risk_group
from symptom_catalog import detect_danger_category, map_symptoms
from groq_ai import parse_complaint_with_ai
from otc_recommendation import get_otc_recommendations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="YUK SEHAT – Pra-Triase Digital",
    description="Sistem Pra-triase berbasis NLU dan Aturan WHO.",
    version="1.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Izinkan semua akses untuk demo
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
# Konfigurasi AI
USE_AI = True

def save_triage_log(data: TriageInput, triage_result: str, danger_sign: bool, risk_group: bool):
    """Menyimpan data hasil triase ke database"""
    db = SessionLocal()
    try:
        new_log = TriageLog(
            age=data.age,
            complaint=data.complaint,
            triage_result=triage_result,
            danger_sign=danger_sign,
            risk_group=risk_group,
        )
        db.add(new_log)
        db.commit()
    except Exception as e:
        print(f"Error saat menyimpan log: {e}")
    finally:
        db.close()

@app.post("/triage")
def triage(data: TriageInput):
    # 1. Lapis 2: Deteksi Bahaya via Kata Kunci (WHO Rules)
    rule_category = detect_danger_category(data.complaint)

    # 2. Lapis 3: Analisis AI (Mengubah teks menjadi data JSON)
    ai_urgency = "LOW"
    ai_category = "UMUM"
    ai_reason = ""
    
    if USE_AI:
        try:
            ai_res = parse_complaint_with_ai(data.complaint)
            ai_urgency = ai_res.get("urgency_level", "LOW")
            ai_category = ai_res.get("category", "UMUM")
            ai_reason = ai_res.get("reason", "")
        except Exception:
            ai_reason = "AI sedang tidak tersedia"

    # 3. Decision Engine (Pusat Validasi Backend)
    # Status MERAH aktif jika salah satu dari 3 lapis mendeteksi bahaya
    is_danger = bool(rule_category or ai_urgency == "HIGH" or data.danger_sign)
    
    # Cek profil risiko (Lansia/Hamil/Komorbid)
    risk_group = is_risk_group(data.age, data.pregnant, data.comorbidity)

    # Penentuan Klasifikasi Final
    if is_danger:
        triage_result = "MERAH"
    elif ai_urgency == "MEDIUM" or risk_group or (data.duration_hours and data.duration_hours > 48):
        triage_result = "KUNING"
    else:
        triage_result = "HIJAU"

    # 4. Ambil Gejala dan Saran Obat (Hanya jika tidak MERAH)
    symptoms = map_symptoms(data.complaint)
    recommendations = get_otc_recommendations(symptoms) if triage_result != "MERAH" else []

    # 5. Simpan data ke database
    save_triage_log(data, triage_result, is_danger, risk_group)

    return {
        "triage_result": triage_result,
        "category": rule_category or ai_category,
        "is_risk_group": risk_group,
        "recommendation": recommendations,
        "ai_analysis": {
            "urgency": ai_urgency,
            "reason": ai_reason
        }
    }