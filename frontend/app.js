const API_URL = "https://yuk-sehat.onrender.com/triage";
//const API_URL = "http://127.0.0.1:8000/triage";

let state = {
    complaint: "",
    age: 0,
    duration_hours: 0,
    pregnant: false,
    comorbidity: false,
    danger_sign: false
};

let selectedFollowUps = {};

function renderInputPage() {
    const container = document.getElementById('app-container');
    container.innerHTML = `
        <div class="page-fade-in text-slate-800">
            <div class="flex justify-between items-center mb-8 bg-white p-6 rounded-3xl shadow-sm border border-slate-100">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 bg-slate-200 rounded-full flex items-center justify-center text-slate-400">
                        <i class="fas fa-user text-xl"></i>
                    </div>
                    <div>
                        <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest leading-none mb-1">Halo,</p>
                        <p class="font-extrabold tracking-tight">Sampaikan Keluhan Anda</p>
                    </div>
                </div>
                <div class="relative text-slate-300">
                    <i class="fas fa-bell text-xl"></i>
                </div>
            </div>

            <div class="space-y-6">
                <textarea id="complaint-input" rows="7" 
                    class="w-full border-2 border-slate-100 rounded-[2rem] p-7 outline-none shadow-inner bg-white text-slate-700 placeholder:text-slate-300 focus:border-blue-400"
                    placeholder="Jelaskan apa yang anda rasakan...">${state.complaint}</textarea>
                
                <button onclick="handleInitialSubmit()" class="btn-click-effect w-full bg-blue-600 text-white font-bold py-5 rounded-2xl shadow-lg text-lg">
                    Kirim Keluhan
                </button>
            </div>
        </div>
    `;
}

function renderValidationPage(data) {
    const container = document.getElementById('app-container');
    let htmlFields = "";

    const questions = data.follow_up_questions || [];
    
    if (questions.length > 0) {
        questions.forEach((item, i) => {
            const questionText = typeof item === 'object' ? item.q : item;
            const questionType = typeof item === 'object' ? item.type : "boolean";

            if (questionType === "number") {
                htmlFields += `
                    <div class="bg-blue-50/50 p-6 rounded-[2rem] border border-blue-100 mb-6 shadow-sm">
                        <label class="block text-sm font-bold text-blue-900 mb-4 text-center">${questionText}</label>
                        <input type="number" id="extra-input-${i}" 
                            class="extra-data-input w-full p-5 rounded-2xl border-2 border-white outline-none focus:border-blue-500 shadow-inner text-center font-black text-slate-700 text-xl" 
                            placeholder="Ketik angka..." data-index="${i}">
                    </div>
                `;
            } else {
                const isYaActive = selectedFollowUps[i] === true;
                const isTidakActive = selectedFollowUps[i] === false;

                htmlFields += `
                    <div class="bg-blue-50/50 p-6 rounded-[2rem] border border-blue-100 mb-6 shadow-sm">
                        <p class="text-sm font-bold text-blue-900 mb-5 text-center leading-relaxed">${questionText}</p>
                        <div class="flex gap-4">
                            <button onclick="setVisualChoice(true, ${i})" 
                                class="flex-1 py-4 rounded-2xl font-bold border-2 transition-all
                                ${isYaActive ? 'bg-blue-600 text-white border-blue-600 shadow-lg' : 'bg-white text-blue-600 border-white'}">
                                Ya
                            </button>
                            <button onclick="setVisualChoice(false, ${i})" 
                                class="flex-1 py-4 rounded-2xl font-bold border-2 transition-all
                                ${isTidakActive ? 'bg-blue-600 text-white border-blue-600 shadow-lg' : 'bg-white text-slate-400 border-white'}">
                                Tidak
                            </button>
                        </div>
                    </div>
                `;
            }
        });
    } else {
        htmlFields = `<p class="text-center text-slate-500">Memproses data tambahan...</p>`;
    }

    container.innerHTML = `
        <div class="page-fade-in">
            <div class="flex items-center gap-4 mb-6">
                <div class="bg-yellow-100 p-3 rounded-2xl text-yellow-600 shadow-sm"><i class="fas fa-user-edit text-xl"></i></div>
                <h3 class="text-2xl font-black text-slate-800 tracking-tight">Lengkapi Data</h3>
            </div>
            <div id="fields-area">${htmlFields}</div>
            <button onclick="handleSecondarySubmit()" class="btn-click-effect w-full bg-blue-600 text-white font-bold py-5 rounded-2xl mt-4 shadow-xl text-lg">
                Lanjutkan Analisis
            </button>
        </div>
    `;
}

// FUNGSI INI HANYA BOLEH ADA SATU
function handleSecondarySubmit() {
    const extraInputs = document.querySelectorAll('.extra-data-input');
    const storedData = sessionStorage.getItem('last_incomplete_data');
    
    if (!storedData) return sendToTriage();
    const lastData = JSON.parse(storedData);

    extraInputs.forEach(input => {
        const val = parseInt(input.value) || 0;
        const index = input.getAttribute('data-index');
        const item = lastData.follow_up_questions[index];
        const questionText = (typeof item === 'object' ? item.q : item).toLowerCase();

        // Pemetaan data yang lebih kuat
        if (questionText.includes("usia")) state.age = val;
        if (questionText.includes("lama") || questionText.includes("jam") || questionText.includes("suhu")) {
            state.duration_hours = val;
        }
        
        state.complaint += `. Jawaban tambahan (${questionText}): ${val}`;
    });

    sendToTriage();
}

function setVisualChoice(val, index) {
    const storedData = sessionStorage.getItem('last_incomplete_data');
    if (!storedData) return;
    
    const lastData = JSON.parse(storedData);
    const item = lastData.follow_up_questions[index];
    const questionText = (typeof item === 'object' ? item.q : item).toLowerCase();

    if (questionText.includes("hamil")) state.pregnant = val;
    if (questionText.includes("komorbid") || questionText.includes("riwayat")) state.comorbidity = val;
    if (val === true) state.danger_sign = true;

    selectedFollowUps[index] = val; 
    renderValidationPage(lastData);
}

async function handleInitialSubmit() {
    const input = document.getElementById('complaint-input');
    if (!input || !input.value) return alert("Isi keluhan dulu.");
    state.complaint = input.value;
    sendToTriage();
}

async function sendToTriage() {
    renderLoading();
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(state)
        });
        const data = await response.json();
        
        if (data.status === "INCOMPLETE") {
            sessionStorage.setItem('last_incomplete_data', JSON.stringify(data));
            renderValidationPage(data);
        } else {
            renderResultPage(data);
        }
    } catch (error) {
        alert("Gagal terhubung ke server.");
        renderInputPage();
    }
}

function renderLoading() {
    document.getElementById('app-container').innerHTML = `
        <div class="flex flex-col items-center justify-center py-24 text-center animate-pulse">
            <div class="loader-circle mb-6"></div>
            <p class="text-slate-600 font-black text-xl">Menganalisis...</p>
        </div>`;
}

function renderResultPage(data) {
    const container = document.getElementById('app-container');
    const res = (data.triage_result || "HIJAU").toUpperCase(); 
    
    let config = {};
    if (res === "MERAH") {
        config = { color: "text-red-600", bg: "bg-red-100", icon: "fa-exclamation-circle", btn: "bg-red-600", label: "Hubungi IGD (119)" };
    } else if (res === "KUNING") {
        config = { color: "text-yellow-600", bg: "bg-yellow-100", icon: "fa-exclamation-triangle", btn: "bg-yellow-500", label: "Puskesmas Terdekat" };
    } else {
        config = { color: "text-green-600", bg: "bg-green-100", icon: "fa-check-circle", btn: "bg-green-600", label: "Temukan Apotek Terdekat" };
    }

    container.innerHTML = `
        <div class="page-fade-in text-center">
            <div class="bg-white border-2 border-slate-50 rounded-[2.5rem] p-10 mb-8 shadow-sm text-slate-800">
                <h2 class="text-xl font-black uppercase tracking-tight">Hasil Analisis</h2>
            </div>
            <div class="mb-8 flex justify-center">
                <div class="w-32 h-32 rounded-full ${config.bg} flex items-center justify-center">
                    <i class="fas ${config.icon} text-6xl ${config.color}"></i>
                </div>
            </div>
            <h3 class="text-2xl font-black text-slate-800 mb-4 tracking-tight">Status ${res}</h3>
            <div class="bg-slate-50 p-6 rounded-3xl mb-10 border border-slate-100 shadow-inner">
                <p class="text-sm text-slate-500 leading-relaxed font-medium italic">"${data.ai_analysis ? data.ai_analysis.reason : 'Analisis selesai.'}"</p>
            </div>
            <div class="space-y-4">
                <button class="w-full ${config.btn} text-white font-bold py-5 rounded-2xl shadow-lg text-lg">${config.label}</button>
                <button onclick="location.reload()" class="w-full border-2 border-slate-100 text-slate-400 font-bold py-4 rounded-2xl text-lg">Kembali</button>
            </div>
        </div>
    `;
}

window.onload = renderInputPage;