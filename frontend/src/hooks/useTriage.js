// src/hooks/useTriage.js
import { useState } from 'react';
import { submitTriage } from '../services/triageService';

export const useTriage = () => {
  const [messages, setMessages] = useState([]); // Daftar percakapan chat
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); // Hasil akhir (MERAH/KUNING/HIJAU)
  const [isComplete, setIsComplete] = useState(false);

  /**
   * FUNGSI UTAMA: MENGIRIM KELUHAN/JAWABAN
   * Digunakan baik untuk input awal maupun saat chat investigasi
   */
  const processTriage = async (userInput, userData) => {
    setLoading(true);
    
    // 1. Tambahkan pesan user ke daftar chat di UI
    const newUserMessage = { text: userInput, isAi: false };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      // 2. Siapkan Payload untuk Backend
      // Kita gabungkan chat sebelumnya agar AI tidak lupa konteks
      const chatHistory = messages.map(m => (m.isAi ? `Investigasi: ${m.text}` : `Jawaban: ${m.text}`)).join("\n");
      const fullComplaint = chatHistory ? `${chatHistory}\nJawaban: ${userInput}` : userInput;

      const payload = {
        nik: userData.nik,
        age: userData.age || 0,
        complaint: fullComplaint,
        duration_hours: userData.duration_hours || 0,
        pregnant: userData.pregnant || false,
        comorbidity: userData.comorbidity || false,
        danger_sign: userData.danger_sign || false
      };

      // 3. Tembak API /triage
      const data = await submitTriage(payload);

      if (data.status === "INCOMPLETE") {
        // AI masih bertanya
        const aiQuestion = data.follow_up_questions[0]?.q || "Bisa jelaskan lebih lanjut?";
        setMessages(prev => [...prev, { text: aiQuestion, isAi: true }]);
      } else {
        // AI sudah selesai menganalisis (COMPLETE)
        setResult(data);
        setIsComplete(true);
      }
    } catch (error) {
      console.error("Triage Error:", error);
      setMessages(prev => [...prev, { text: "Maaf, terjadi kendala teknis. Mohon coba lagi.", isAi: true }]);
    } finally {
      setLoading(false);
    }
  };

  const resetTriage = () => {
    setMessages([]);
    setResult(null);
    setIsComplete(false);
  };

  return { messages, loading, result, isComplete, processTriage, resetTriage };
};