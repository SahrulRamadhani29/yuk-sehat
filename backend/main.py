# main.py
import os
import re
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

# =========================================================
# DATABASE UTILS & HISTORY (KITA KEMBALIKAN DI SINI)
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
            danger_sign=is_danger,  # Sesuai dengan models.py
            risk_group=is_risk,     # Sesuai dengan models.py
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
def check_nik(nik: str):
    db = SessionLocal()
    last_log = db.query(TriageLog).filter(TriageLog.nik == nik).order_by(TriageLog.created_at.desc()).first()
    db.close()
    if last_log:
        return {"exists": True, "age": last_log.age}
    return {"exists": False, "age": None}

@app.post("/triage", response_model=TriageResponse)
async def triage_endpoint(data: TriageInput):
    # 1. Ekstraksi Durasi Otomatis dari Teks
    if data.duration_hours <= 0:
        data.duration_hours = extract_duration_from_text(data.complaint)

    # 2. Penyiapan Konteks
    risk_group = is_risk_group(data.age, data.pregnant, data.comorbidity)
    rule_danger_cat = detect_danger_category(data.complaint)
    manual_danger = data.danger_sign
    user_history = get_patient_history_context(data.nik)

    # --- BAGIAN MODIFIKASI: PEMBERIAN LABEL JAWABAN AGAR AI TIDAK LOOPING ---
    current_chat = data.complaint.replace("Investigasi:", "\n[PERTANYAAN AI]:").replace("Jawaban:", "\n[JAWABAN PASIEN]:")

    full_context_for_ai = (
        f"{user_history}\n\n"
        f"--- PERCAKAPAN INVESTIGASI BERJALAN ---\n"
        f"{current_chat}\n"
        f"--- INSTRUKSI: JANGAN TANYA HAL YANG SUDAH ADA DI [JAWABAN PASIEN] DI ATAS! ---"
    )

    # 3. Proses Investigasi AI
    try:
        ai_res = parse_complaint_with_ai(
            text=full_context_for_ai,
            age=data.age,
            is_risk=risk_group,
            duration=data.duration_hours,
            is_danger=bool(rule_danger_cat or manual_danger)
        )
        
        ai_urgency = ai_res.get("urgency_level", "LOW")
        ai_category = ai_res.get("category", "UMUM")
        ai_reason = ai_res.get("reason", "Proses AI selesai.")
        needs_follow_up = ai_res.get("needs_follow_up", False)
        
        follow_up_qs = [
            q for q in ai_res.get("follow_up_questions", [])
            if not any(w in q.get('q','').lower() for w in ["usia", "umur", "jam", "lama", "kapan"])
        ]

        if needs_follow_up and follow_up_qs:
            return TriageResponse(status="INCOMPLETE", message="AI mengeksplorasi...", follow_up_questions=follow_up_qs)

    except Exception as e:
        print(f"AI Error: {e}")
        ai_urgency, ai_category, ai_reason = "LOW", "UMUM", "Gagal memproses AI."

    # 4. Penentuan Hasil Akhir (Triase)
    is_immediate_danger = bool(rule_danger_cat or ai_urgency == "HIGH" or manual_danger)
    if is_immediate_danger:
        triage_result = "MERAH"
    elif ai_urgency == "MEDIUM" or risk_group or (data.duration_hours > 48):
        triage_result = "KUNING"
    else:
        triage_result = "HIJAU"

    # 5. Rekomendasi Obat & Kategori
    symptoms = map_symptoms(data.complaint)
    search_keys = symptoms + [ai_category] 
    recommendations = get_otc_recommendations(search_keys) if triage_result != "MERAH" else []
    final_category = ai_category if ai_category != "UMUM" else (rule_danger_cat or "UMUM")

    # 6. Simpan Log
    save_triage_log(data, triage_result, is_immediate_danger, risk_group, final_category)

    # --- PERBAIKAN: SESUAIKAN DENGAN STRUKTUR SCHEMAS & CLIENT ---
    return TriageResponse(
        status="COMPLETE",
        triage_result=triage_result,
        category=final_category,
        recommendation=recommendations,
        # Mengirimkan objek ai_analysis untuk menghindari NoneType error di client
        ai_analysis={
            "urgency": ai_urgency,
            "reason": ai_reason
        }
    )