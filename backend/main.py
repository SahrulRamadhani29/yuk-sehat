# main.py
from fastapi import FastAPI, HTTPException
from database import SessionLocal
from models import TriageLog
from schemas import TriageInput, TriageResponse 
from database import engine, Base

# Import logika dari file pendukung
from rules import is_risk_group
from symptom_catalog import detect_danger_category, map_symptoms
from groq_ai import parse_complaint_with_ai
from otc_recommendation import get_otc_recommendations

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="YUK SEHAT – Pra-Triase Digital",
    description="Sistem Pra-triase dengan Smart-Triage Logic (Safety & Depth Analysis).",
    version="1.6"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
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

@app.post("/triage", response_model=TriageResponse)
def triage(data: TriageInput):
    # --- 1. VALIDASI DATA DASAR (USIA & DURASI) ---
    pre_ai_questions = []
    if not data.age or data.age <= 0:
        pre_ai_questions.append({"q": "Berapa usia Anda saat ini?", "type": "number"})
    if not data.duration_hours or data.duration_hours <= 0:
        pre_ai_questions.append({"q": "Sudah berapa jam Anda merasakan keluhan ini?", "type": "number"})

    if pre_ai_questions:
        return TriageResponse(
            status="INCOMPLETE",
            message="Mohon lengkapi data dasar berikut.",
            follow_up_questions=pre_ai_questions
        )

    # --- 2. ANALISIS AWAL (AI & RULES) ---
    rule_category = detect_danger_category(data.complaint)
    ai_urgency = "LOW"
    ai_category = "UMUM"
    ai_reason = ""
    ai_duration = 0
    needs_follow_up = False
    follow_up_qs = []

    if USE_AI:
        try:
            ai_res = parse_complaint_with_ai(data.complaint)
            ai_urgency = ai_res.get("urgency_level", "LOW")
            ai_category = ai_res.get("category", "UMUM")
            ai_reason = ai_res.get("reason", "")
            ai_duration = ai_res.get("extracted_duration_hours", 0)
            needs_follow_up = ai_res.get("needs_follow_up", False)
            follow_up_qs = ai_res.get("follow_up_questions", [])
        except Exception:
            ai_reason = "AI sedang tidak tersedia"

    # --- 3. DECISION ENGINE PART 1: EMERGENCY FIRST ---
    effective_duration = data.duration_hours if data.duration_hours > 0 else ai_duration
    risk_group = is_risk_group(data.age, data.pregnant, data.comorbidity)
    
    # Jika terdeteksi BAHAYA NYATA (Manual atau High Urgency AI)
    is_immediate_danger = bool(rule_category or ai_urgency == "HIGH" or data.danger_sign)

    if is_immediate_danger:
        triage_result = "MERAH"
        save_triage_log(data, triage_result, True, risk_group)
        return TriageResponse(
            status="COMPLETE",
            message="Hasil triase selesai: KONDISI DARURAT.",
            triage_result=triage_result,
            category=rule_category or ai_category,
            is_risk_group=risk_group,
            recommendation=[],
            ai_analysis={
                "urgency": ai_urgency,
                "reason": ai_reason or "Tanda bahaya terdeteksi.",
                "extracted_duration_hours": effective_duration
            }
        )

    # --- 4. DECISION ENGINE PART 2: SMART FOLLOW-UP ---
    # Jika tidak gawat darurat, tapi AI masih butuh konfirmasi gejala kombinasi
    if needs_follow_up and follow_up_qs:
        return TriageResponse(
            status="INCOMPLETE",
            message="Sistem memerlukan informasi tambahan untuk memastikan tidak ada gejala kombinasi berbahaya.",
            follow_up_questions=follow_up_qs
        )

    # --- 5. KLASIFIKASI AKHIR (Hanya jika AI sudah yakin) ---
    if ai_urgency == "MEDIUM" or risk_group or (effective_duration > 48):
        triage_result = "KUNING"
    else:
        triage_result = "HIJAU"

    symptoms = map_symptoms(data.complaint)
    recommendations = get_otc_recommendations(symptoms) if triage_result == "HIJAU" else []

    save_triage_log(data, triage_result, False, risk_group)

    return TriageResponse(
        status="COMPLETE",
        message="Analisis selesai. Berikut adalah hasil triase Anda.",
        triage_result=triage_result,
        category=rule_category or ai_category,
        is_risk_group=risk_group,
        recommendation=recommendations,
        ai_analysis={
            "urgency": ai_urgency,
            "reason": ai_reason,
            "extracted_duration_hours": effective_duration
        }
    )