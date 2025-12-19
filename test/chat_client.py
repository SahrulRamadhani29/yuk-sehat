# chat_client.py
import requests

# URL Backend Lokal
URL_TRIAGE = "http://127.0.0.1:8000/triage"
URL_CHECK_NIK = "http://127.0.0.1:8000/check-nik"
URL_HISTORY = "http://127.0.0.1:8000/user-history"

def start_chat():
    print("=== SISTEM TRIASE DIGITAL ===")
    
    # Inisialisasi variabel default untuk menghindari warning/garis kuning
    nik = ""
    age = 0
    duration = 0
    complaint = ""
    user_data = {"exists": False, "age": None}

    # 1. Input NIK
    nik = input("Masukkan NIK Anda: ")
    # 2. Fitur Baru: Tabel Riwayat Lengkap (Diperbaiki)
    try:
        history_resp = requests.get(f"{URL_HISTORY}/{nik}")
        if history_resp.status_code == 200:
            history_list = history_resp.json()
            if history_list:
                print("\n" + "="*85)
                # GUNAKAN TEKS MANUAL UNTUK JUDUL (Bukan variabel)
                print(f"{'TANGGAL':<12} | {'KELUHAN':<30} | {'KATEGORI':<15} | {'HASIL':<7}")
                print("-" * 85)
                
                for log in history_list[:5]:
                    date_only = log['date'].split("T")[0]
                    category = log.get('category', 'UMUM')
                    
                    # Bersihkan teks keluhan dari sisa investigasi AI agar rapi di tabel
                    clean_complaint = log['complaint'].split("- Investigasi:")[0].strip()
                    complaint_short = (clean_complaint[:27] + '..') if len(clean_complaint) > 27 else clean_complaint
                    
                    print(f"{date_only:<12} | {complaint_short:<30} | {category:<15} | {log['result']:<7}")
                print("="*85 + "\n")
            else:
                print("\n(Belum ada riwayat medis terdaftar untuk NIK ini)\n")
    except Exception as e:
        print(f"\n(Sistem gagal memuat tabel riwayat: {e})\n")
    # 3. Cek NIK untuk Auto-Detect Usia
    try:
        check_resp = requests.get(f"{URL_CHECK_NIK}/{nik}")
        if check_resp.status_code == 200:
            user_data = check_resp.json()
    except:
        user_data = {"exists": False, "age": None}

    # 4. Input Keluhan & Data Dasar
    complaint = input("Apa keluhan Anda saat ini? ")
    
    if user_data.get("exists"):
        age = user_data["age"]
        print(f"Sistem mengenali Anda (Usia: {age} tahun).")
    else:
        try:
            age = int(input("Berapa usia Anda? (Angka saja): "))
        except ValueError:
            print("Error: Usia harus angka!")
            return

    try:
        duration = int(input("Sudah berapa jam keluhan ini dirasakan? (Angka saja): "))
    except ValueError:
        print("Error: Durasi harus angka!")
        return
    
    # 5. Persiapan Payload untuk Triase
    payload = {
        "nik": nik,
        "complaint": complaint,
        "age": age,
        "duration_hours": duration,
        "pregnant": False,
        "comorbidity": False,
        "danger_sign": False
    }

    print("\nSedang menganalisis keluhan awal Anda...")

    # 6. Loop Investigasi AI (Follow-up)
    while True:
        try:
            response = requests.post(URL_TRIAGE, json=payload)
            if response.status_code != 200:
                print(f"Server Error: {response.status_code}")
                break
            
            data = response.json()
        except Exception as e:
            print(f"Gagal terhubung ke server: {e}")
            break

        # A. Jika Analisis Selesai
        if data["status"] == "COMPLETE":
            print("\n" + "="*45)
            print(f"HASIL TRIASE : {data['triage_result']}")
            print(f"KATEGORI     : {data['category']}")
            print(f"ANALISIS AI  : {data['ai_analysis']['reason']}")
            
            if data["recommendation"]:
                print("\nSARAN TINDAKAN & OBAT:")
                for rec in data["recommendation"]:
                    print(f"- {rec}")
            
            if data["triage_result"] == "MERAH":
                print("\n!!! SEGERA KE IGD RUMAH SAKIT TERDEKAT !!!")
            elif data["triage_result"] == "KUNING":
                print("\nDisarankan segera berkonsultasi dengan dokter.")
            
            print("="*45)
            break
        
        # B. Jika AI Meminta Informasi Tambahan
        elif data["status"] == "INCOMPLETE":
            print("\n--- Pertanyaan dari Investigator AI ---")
            new_responses = ""
            
            for q in data["follow_up_questions"]:
                prompt_label = f"[{q['type'].upper()}]"
                user_answer = input(f"{prompt_label} {q['q']} \n>> Jawab: ")
                new_responses += f"\n- Investigasi: {q['q']} | Jawaban Pasien: {user_answer}"
            
            # Gabungkan jawaban baru ke keluhan untuk dikirim ulang
            payload["complaint"] += new_responses
            print("\nMenyinkronkan jawaban Anda dengan sistem...")

if __name__ == "__main__":
    start_chat()