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
    description="Sistem Pra-triase berbasis NLU dan Aturan WHO.",
    version="1.4" # Update ke 1.4: Pre-AI Validation Logic
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
    # --- 1. VALIDASI DATA DASAR (PRE-AI) ---
    # Memastikan Usia dan Durasi diisi sebelum melakukan analisis AI mendalam
    # Ini mencegah input double dan meningkatkan akurasi NLU
    pre_ai_questions = []
    
    if not data.age or data.age <= 0:
        pre_ai_questions.append({"q": "Berapa usia Anda saat ini?", "type": "number"})
    
    if not data.duration_hours or data.duration_hours <= 0:
        pre_ai_questions.append({"q": "Sudah berapa jam Anda merasakan keluhan ini? (Masukkan angka saja)", "type": "number"})

    # Jika data dasar belum lengkap, langsung kembalikan status INCOMPLETE tanpa panggil AI
    if pre_ai_questions:
        return TriageResponse(
            status="INCOMPLETE",
            message="Mohon lengkapi data dasar berikut sebelum sistem melakukan analisis medis.",
            follow_up_questions=pre_ai_questions
        )

    # --- 2. ANALISIS AI (PANGGIL JIKA DATA DASAR LENGKAP) ---
    rule_category = detect_danger_category(data.complaint)
    
    ai_urgency = "LOW"
    ai_category = "UMUM"
    ai_reason = ""
    ai_duration = 0
    needs_follow_up = False
    follow_up_qs = []

    if USE_AI:
        try:
            # AI sekarang menerima state yang sudah berisi Age dan Duration yang valid
            ai_res = parse_complaint_with_ai(data.complaint)
            ai_urgency = ai_res.get("urgency_level", "LOW")
            ai_category = ai_res.get("category", "UMUM")
            ai_reason = ai_res.get("reason", "")
            ai_duration = ai_res.get("extracted_duration_hours", 0)
            needs_follow_up = ai_res.get("needs_follow_up", False)
            follow_up_qs = ai_res.get("follow_up_questions", [])
        except Exception:
            ai_reason = "AI sedang tidak tersedia"

    # --- 3. LOGIKA VALIDASI LANJUTAN (FOLLOW-UP AI) ---
    # Jika AI mendeteksi butuh konfirmasi gejala lain (Ya/Tidak)
    if needs_follow_up and follow_up_qs:
        # Filter untuk memastikan AI tidak menanyakan Usia/Durasi lagi (Anti-Double)
        filtered_qs = [q for q in follow_up_qs if "usia" not in q['q'].lower() and "lama" not in q['q'].lower()]
        
        if filtered_qs:
            return TriageResponse(
                status="INCOMPLETE",
                message="Sistem mendeteksi gejala yang perlu perhatian khusus. Mohon jawab pertanyaan berikut.",
                follow_up_questions=filtered_qs
            )

    # --- 4. DECISION ENGINE (COMPLETE) ---
    effective_duration = data.duration_hours if data.duration_hours > 0 else ai_duration
    
    is_danger = bool(rule_category or ai_urgency == "HIGH" or data.danger_sign)
    risk_group = is_risk_group(data.age, data.pregnant, data.comorbidity)

    if is_danger:
        triage_result = "MERAH"
    elif ai_urgency == "MEDIUM" or risk_group or (effective_duration > 48):
        triage_result = "KUNING"
    else:
        triage_result = "HIJAU"

    # --- 5. OUTPUT FINAL ---
    symptoms = map_symptoms(data.complaint)
    recommendations = get_otc_recommendations(symptoms) if triage_result != "MERAH" else []

    save_triage_log(data, triage_result, is_danger, risk_group)

    return TriageResponse(
        status="COMPLETE",
        message="Hasil triase Anda telah selesai dianalisis.",
        triage_result=triage_result,
        category=rule_category or ai_category,
        is_risk_group=risk_group,
        recommendation=recommendations,
        ai_analysis={
            "urgency": ai_urgency,
            "reason": ai_reason,
            "extracted_duration_hours": ai_duration
        }
    )