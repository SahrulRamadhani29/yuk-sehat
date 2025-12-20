# main.py
import os
import re
from dotenv import load_dotenv

load_dotenv()
# MODIFIKASI: Menambahkan Depends dan HTTPException yang diperlukan untuk get_db dan check_nik
from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, engine, Base
from models import TriageLog
from schemas import TriageInput, TriageResponse 

# Import logika pendukung
from rules import is_risk_group
from symptom_catalog import detect_danger_category, map_symptoms
from mistral_ai import parse_complaint_with_ai
from otc_recommendation import get_otc_recommendations
from fastapi.middleware.cors import CORSMiddleware
# MODIFIKASI: Menambahkan Session untuk type hinting database
from sqlalchemy.orm import Session
from sqlalchemy import desc

app = FastAPI(title="YUK SEHAT – AI Driven Exploratory Triage", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# =========================================================
# MODIFIKASI: MENAMBAHKAN FUNGSI get_db UNTUK KONEKSI DATABASE
# =========================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================================================
# LOGIKA EKSTRAKSI DURASI (DARI KELUHAN)
# =========================================================
def extract_duration_from_text(text: str) -> int:
    """Ekstraksi angka durasi dan konversi ke JAM."""
    if not text:
        return 0
        
    text = text.lower()
    match = re.search(r'(\d+)\s*(jam|hari|minggu|bulan)', text)
    
    if match:
        val = int(match.group(1))
        unit = match.group(2)
        if "hari" in unit: return val * 24
        elif "minggu" in unit: return val * 168
        elif "bulan" in unit: return val * 720
        else: return val
    return 0

# Tambahan Fungsi untuk Menghitung Turn Investigasi
def count_investigation_turns(text: str) -> int:
    """Menghitung berapa kali turn investigasi telah berlangsung."""
    return text.count("Investigasi:")

# =========================================================
# MODIFIKASI FINAL: SLOT FILLING MINIMAL (ANTI PERTANYAAN ULANG)
# =========================================================
def extract_answered_slots(text: str) -> dict:
    slots = {"nyeri": None}
    t = text.lower()

    if any(x in t for x in [
        "tidak ada nyeri",
        "tidak nyeri",
        "tanpa nyeri",
        "tidak sakit"
    ]):
        slots["nyeri"] = False
    elif any(x in t for x in [
        "nyeri",
        "sakit",
        "pegal",
        "linu"
    ]):
        slots["nyeri"] = True

    return slots

# =========================================================
# DATABASE UTILS & HISTORY
# =========================================================

@app.get("/user-history/{nik}")
def user_history_list(nik: str):
    """Menampilkan daftar riwayat medis berdasarkan NIK."""
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

def get_patient_history_context(nik: str, limit: int = 3):
    """Fungsi internal untuk memberikan konteks riwayat ke AI."""
    db = SessionLocal()
    try:
        history = db.query(TriageLog).filter(TriageLog.nik == nik)\
                    .order_by(TriageLog.created_at.desc()).limit(limit).all()
        if not history:
            return "PENGGUNA BARU: Tidak ada riwayat medis sebelumnya."
        return "\n".join([f"- {h.created_at.date()}: {h.complaint} (Status: {h.triage_result})" for h in history])
    finally:
        db.close()

def save_triage_log(data: TriageInput, result: str, is_danger: bool, is_risk: bool, category: str):
    db = SessionLocal()
    try:
        new_log = TriageLog(
            nik=data.nik,
            age=data.age,
            complaint=data.complaint,
            duration_hours=data.duration_hours,
            triage_result=result,
            danger_sign=is_danger,
            risk_group=is_risk,
            category=category
        )
        db.add(new_log)
        db.commit()
    finally:
        db.close()

# =========================================================
# ROUTES UTAMA
# =========================================================

@app.get("/check-nik/{nik}")
def check_nik(nik: str, db: Session = Depends(get_db)):
    last_log = db.query(TriageLog).filter(TriageLog.nik == nik).order_by(desc(TriageLog.created_at)).first()
    
    if last_log:
        return {
            "exists": True,
            "age": last_log.age,
            "nickname": "Pasien" 
        }
    
    return {"exists": False, "age": 0}

@app.post("/triage", response_model=TriageResponse)
async def triage_endpoint(data: TriageInput):
    raw_first_line = data.complaint.split('\n')[0]
    original_complaint = re.sub(r'^(Jawaban Pasien:|\[JAWABAN PASIEN\]:)\s*', '', raw_first_line, flags=re.IGNORECASE).strip()
    
    risk_group = is_risk_group(data.age, data.pregnant, data.comorbidity)
    rule_danger_cat = detect_danger_category(original_complaint)
    manual_danger = data.danger_sign

    if data.duration_hours <= 0:
        data.duration_hours = extract_duration_from_text(data.complaint)

    user_history = get_patient_history_context(data.nik)
    current_chat = data.complaint.replace("Investigasi:", "\n[PERTANYAAN AI]:").replace("Jawaban:", "\n[JAWABAN PASIEN]:")

    enhanced_context_for_ai = (
        f"KELUHAN UTAMA PASIEN: {original_complaint}\n\n"
        f"RIWAYAT PERCAKAPAN LENGKAP:\n"
        f"{user_history}\n\n"
        f"{current_chat}\n"
        f"--- INSTRUKSI: JANGAN TANYA HAL YANG SUDAH ADA DI [JAWABAN PASIEN] DI ATAS! ---"
    )

    try:
        ai_res = parse_complaint_with_ai(
            text=enhanced_context_for_ai,
            age=data.age,
            is_risk=risk_group,
            duration=data.duration_hours,
            is_danger=bool(rule_danger_cat or manual_danger)
        )
        
        ai_urgency = ai_res.get("urgency_level", "LOW")
        ai_category = ai_res.get("category", "UMUM")
        ai_reason = ai_res.get("reason", "Proses AI selesai.")
        current_turns = count_investigation_turns(data.complaint)

        raw_qs = ai_res.get("follow_up_questions", [])
        follow_up_qs = []

        answered_slots = extract_answered_slots(data.complaint)

        for q_obj in raw_qs:
            q_text = q_obj.get('q', '')
            q_lower = q_text.lower()

            if "nyeri" in q_lower and answered_slots.get("nyeri") is False:
                continue

            if q_lower not in data.complaint.lower() and not any(w in q_lower for w in ["usia", "umur", "jam", "lama", "kapan"]):
                follow_up_qs.append(q_obj)

        is_real_danger = bool(rule_danger_cat or manual_danger)
        if not is_real_danger and current_turns < 4 and follow_up_qs:
            return TriageResponse(
                status="INCOMPLETE",
                message="AI mengeksplorasi lebih dalam...",
                follow_up_questions=follow_up_qs[:1]
            )

    except Exception as e:
        ai_urgency, ai_category, ai_reason = "LOW", "UMUM", f"Gagal memproses AI: {str(e)}"

    if rule_danger_cat or manual_danger or ai_urgency == "HIGH":
        triage_result = "MERAH"
    elif ai_urgency == "MEDIUM" or risk_group or (data.duration_hours > 48):
        triage_result = "KUNING"
    else:
        triage_result = "HIJAU"

    patient_answers = " ".join(re.findall(r"Jawaban Pasien: (.*)", data.complaint))
    initial_complaint = data.complaint.split("\n")[0]
    search_text = f"{initial_complaint} {patient_answers}"
    
    symptoms = map_symptoms(search_text)
    search_keys = symptoms + [ai_category]
    recommendations = get_otc_recommendations(search_keys) if triage_result != "MERAH" else []

    final_category = ai_category
    if final_category in ["UMUM", "umum_tidak_jelas"] and symptoms:
        final_category = symptoms[0]
    elif final_category in ["UMUM", "umum_tidak_jelas"]:
        final_category = rule_danger_cat or "UMUM"

    save_triage_log(data, triage_result, bool(rule_danger_cat or manual_danger), risk_group, final_category)

    return TriageResponse(
        status="COMPLETE",
        triage_result=triage_result,
        category=final_category,
        recommendation=recommendations,
        ai_analysis={"urgency": ai_urgency, "reason": ai_reason}
    )
