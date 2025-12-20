# chat_client.py
import requests
import re

# URL Backend (Sesuaikan jika sudah deploy ke Render)
# URL_BASE = "http://127.0.0.1:8000"
URL_BASE = "https://yuk-sehat.onrender.com"

URL_TRIAGE = f"{URL_BASE}/triage"
URL_CHECK_NIK = f"{URL_BASE}/check-nik"
URL_HISTORY = f"{URL_BASE}/user-history"

def extract_duration_local(text: str) -> bool:
    """Cek apakah user sudah memasukkan durasi dalam teks keluhan."""
    text = text.lower()
    return bool(re.search(r'\d+\s*(jam|hari|minggu|bulan)', text))

def start_chat():
    print("=== SISTEM TRIASE DIGITAL ===")
    
    nik = input("Masukkan NIK Anda: ")

    # 1. Tampilkan Tabel Riwayat (User History)
    try:
        history_resp = requests.get(f"{URL_HISTORY}/{nik}")
        if history_resp.status_code == 200:
            history_list = history_resp.json()
            if history_list:
                print("\n" + "="*75)
                print(f"{'TANGGAL':<12} | {'KELUHAN':<35} | {'HASIL':<7} | {'KATEGORI':<15}")
                print("-" * 75)
                for log in history_list[:5]:
                    date_only = log['date'].split("T")[0]
                    # Bersihkan teks agar rapi di tabel
                    clean_comp = log['complaint'].split("\n")[0][:32]
                    print(f"{date_only:<12} | {clean_comp:<35} | {log['result']:<7} | {log['category']:<15}")
                print("="*75 + "\n")
            else:
                print("\n(Belum ada riwayat medis untuk NIK ini)\n")
    except Exception as e:
        print(f"\n(Gagal memuat riwayat: {e})\n")

    # 2. Deteksi NIK & Usia
    user_data = {"exists": False, "age": None}
    try:
        check_resp = requests.get(f"{URL_CHECK_NIK}/{nik}")
        if check_resp.status_code == 200:
            user_data = check_resp.json()
    except: pass

    # 3. Input Keluhan Utama
    complaint = input("Apa keluhan Anda saat ini? ")
    
    # 4. Logika Durasi Otomatis (PEMBARUAN)
    duration = 0
    # Jika dalam teks keluhan TIDAK ada kata 'jam/hari/minggu/bulan', baru tanya manual
    if not extract_duration_local(complaint):
        try:
            duration_input = input("Sudah berapa jam keluhan dirasakan? (Kosongkan jika sudah ada di teks): ")
            duration = int(duration_input) if duration_input.strip() else 0
        except ValueError:
            duration = 0
    else:
        print("Sistem mendeteksi durasi dari keluhan Anda...")

    # 5. Deteksi Usia Otomatis
    if user_data.get("exists") and user_data["age"]:
        age = user_data["age"]
        print(f"Sistem mengenali Anda (Usia: {age} tahun).")
    else:
        try:
            age = int(input("Berapa usia Anda? (Angka saja): "))
        except ValueError:
            print("Error: Usia harus angka!")
            return

    # 6. Persiapan Payload
    payload = {
        "nik": nik,
        "complaint": complaint,
        "age": age,
        "duration_hours": duration,
        "pregnant": False,
        "comorbidity": False,
        "danger_sign": False
    }

    print("\nSedang menganalisis keluhan Anda...")

    # 7. Loop Investigasi AI
    while True:
        try:
            response = requests.post(URL_TRIAGE, json=payload)
            if response.status_code != 200:
                print(f"Server Error: {response.status_code}")
                break
            
            data = response.json()
        except Exception as e:
            print(f"Koneksi terputus: {e}")
            break

        if data["status"] == "COMPLETE":
            print("\n" + "="*50)
            print(f"HASIL TRIASE : {data['triage_result']}")
            print(f"KATEGORI     : {data['category']}")
            
            # Mendukung format respons baru dari main.py
            # Ubah baris 109 menjadi:
            ai_data = data.get("ai_analysis") or {}
            reason = ai_data.get("reason") or data.get("analysis") or "Selesai."
            print(f"ANALISIS AI  : {reason}")
            
            recs = data.get("recommendation") or data.get("recommendations")
            if recs:
                print("\nSARAN TINDAKAN & OBAT:")
                for rec in recs:
                    print(f"- {rec}")
            
            if data["triage_result"] == "MERAH":
                print("\n!!! SEGERA KE IGD RUMAH SAKIT TERDEKAT !!!")
            print("="*50)
            break
        
        elif data["status"] == "INCOMPLETE":
            print("\n--- Pertanyaan dari Investigator AI ---")
            new_responses = ""
            for q in data["follow_up_questions"]:
                ans = input(f"[{q['type'].upper()}] {q['q']} \n>> Jawab: ")
                # Gunakan label baru agar sinkron dengan backend
                new_responses += f"\nInvestigasi: {q['q']}\nJawaban Pasien: {ans}"
            
            payload["complaint"] += new_responses
            print("\nMenyinkronkan data...")

if __name__ == "__main__":
    start_chat()