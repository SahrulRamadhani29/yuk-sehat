# main.py
import os
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from models import TriageLog
from schemas import TriageInput, TriageResponse 

# Import logika pendukung
from rules import is_risk_group
from symptom_catalog import detect_danger_category, map_symptoms
from groq_ai import parse_complaint_with_ai
from otc_recommendation import get_otc_recommendations
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc

app = FastAPI(title="YUK SEHAT – AI Driven Exploratory Triage", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/check-nik/{nik}")
def check_nik(nik: str):
    db = SessionLocal()
    last_log = db.query(TriageLog).filter(TriageLog.nik == nik).order_by(TriageLog.created_at.desc()).first()
    db.close()
    
    if last_log:
        return {"exists": True, "age": last_log.age}
    return {"exists": False, "age": None}

@app.get("/user-history/{nik}")
def user_history_list(nik: str):
    db = SessionLocal()
    try:
        logs = db.query(TriageLog).filter(TriageLog.nik == nik)\
                 .order_by(desc(TriageLog.created_at)).all()
        return [
            {
                "id": log.id,
                "date": log.created_at,
                "complaint": log.complaint,
                "result": log.triage_result,
                "category": getattr(log, 'category', 'UMUM')
            } for log in logs
        ]
    finally:
        db.close()

def get_user_history(nik: str):
    db = SessionLocal()
    try:
        logs = db.query(TriageLog).filter(TriageLog.nik == nik).order_by(desc(TriageLog.created_at)).limit(3).all()
        if not logs:
            return "PENGGUNA BARU: Tidak ada riwayat medis sebelumnya."
        history_text = "RIWAYAT MEDIS SEBELUMNYA DI SISTEM INI:\n"
        for log in logs:
            history_text += f"- Tanggal: {log.created_at.strftime('%Y-%m-%d')}, Keluhan: {log.complaint}, Hasil: {log.triage_result}\n"
        return history_text
    except Exception:
        return "Gagal memuat riwayat medis."
    finally:
        db.close()

# --- FUNGSI SAVE LOG (DIPERBAIKI) ---
def save_triage_log(data, triage_result, danger_sign, risk_group, category): 
    """Menyimpan data triase termasuk NIK dan Kategori ke database."""
    db = SessionLocal()
    try:
        new_log = TriageLog(
            nik=data.nik,
            age=data.age,
            complaint=data.complaint,
            category=category,      # Data kategori dari AI masuk sini
            triage_result=triage_result,
            danger_sign=danger_sign,
            risk_group=risk_group
        )
        db.add(new_log)
        db.commit()
    except Exception as e:
        print(f"Error saving log to Database: {e}")
    finally:
        db.close()

@app.post("/triage", response_model=TriageResponse)
def triage(data: TriageInput):
    # 1. VALIDASI DATA DASAR
    pre_ai_questions = []
    if not data.age or data.age <= 0:
        pre_ai_questions.append({"q": "Berapa usia Anda saat ini?", "type": "number"})
    if not data.duration_hours or data.duration_hours <= 0:
        pre_ai_questions.append({"q": "Sudah berapa jam Anda merasakan keluhan ini?", "type": "number"})
    if not data.nik:
        pre_ai_questions.append({"q": "Masukkan NIK", "type": "string"})

    if pre_ai_questions:
        return TriageResponse(status="INCOMPLETE", message="Lengkapi data.", follow_up_questions=pre_ai_questions)

    # 2. PENYIAPAN KONTEKS
    user_history = get_user_history(data.nik)
    risk_group = is_risk_group(data.age, data.pregnant, data.comorbidity)
    manual_danger = data.danger_sign
    
    original_complaint = data.complaint.split("Investigasi:")[0].split("Jawaban:")[0].strip()
    rule_danger_cat = detect_danger_category(original_complaint)
    full_context_for_ai = f"{user_history}\n\nKELUHAN SAAT INI: {data.complaint}"

    # 3. ALUR AI
    try:
        ai_res = parse_complaint_with_ai(
            text=full_context_for_ai,
            age=data.age,
            is_risk=risk_group,
            duration=data.duration_hours,
            is_danger=manual_danger
        )
        
        ai_urgency = ai_res.get("urgency_level", "LOW")
        ai_category = ai_res.get("category", "UMUM")
        ai_reason = ai_res.get("reason", "")
        needs_follow_up = ai_res.get("needs_follow_up", False)
        
        follow_up_qs = [
            q for q in (ai_res.get("follow_up_questions") or [])
            if isinstance(q, dict) and not any(w in q.get('q','').lower() for w in ["usia", "umur", "lama"])
        ]

        if needs_follow_up and follow_up_qs:
            return TriageResponse(status="INCOMPLETE", message="AI mengeksplorasi...", follow_up_questions=follow_up_qs)

    except Exception as e:
        print(f"AI Error: {e}")
        ai_urgency, ai_category, ai_reason = "LOW", "UMUM", "Gagal memproses AI."

    # 4. TRIASE FINAL
    is_immediate_danger = bool(rule_danger_cat or ai_urgency == "HIGH" or manual_danger)
    if is_immediate_danger:
        triage_result = "MERAH"
    elif ai_urgency == "MEDIUM" or risk_group or (data.duration_hours > 48):
        triage_result = "KUNING"
    else:
        triage_result = "HIJAU"

    # 5. REKOMENDASI & KATEGORI
    symptoms = map_symptoms(original_complaint)
    recommendations = get_otc_recommendations(symptoms) if triage_result != "MERAH" else []
    final_category = ai_category if ai_category != "UMUM" else (rule_danger_cat or "UMUM")

    # 6. SIMPAN KE DATABASE (DIPERBAIKI: Mengirim 5 parameter)
    save_triage_log(data, triage_result, is_immediate_danger, risk_group, final_category)

    return TriageResponse(
        status="COMPLETE", 
        message="Analisis selesai.", 
        triage_result=triage_result,
        category=final_category, 
        is_risk_group=risk_group,
        recommendation=recommendations,
        ai_analysis={"urgency": ai_urgency, "reason": ai_reason, "extracted_duration_hours": data.duration_hours}
    )