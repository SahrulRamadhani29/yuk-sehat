import { useState } from 'react';
import { submitTriage } from '../services/triageService';

export const useTriage = () => {
  const [messages, setMessages] = useState([]); 
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); 
  const [isComplete, setIsComplete] = useState(false);

  const processTriage = async (userInput, userData, currentHistory) => {
    setLoading(true);

    try {
      // MODIFIKASI: Gunakan label "Investigasi:" agar sinkron dengan count_investigation_turns di main.py
      const formattedHistory = currentHistory.map(m => (
        m.isAi ? `Investigasi: ${m.text}` : `Jawaban Pasien: ${m.text}`
      )).join("\n");

      const finalComplaint = formattedHistory 
        ? `${formattedHistory}\nJawaban Pasien: ${userInput}` 
        : `Jawaban Pasien: ${userInput}`;

      const payload = {
        nik: userData.nik,
        age: parseInt(userData.age) || 0,
        complaint: finalComplaint,
        duration_hours: userData.duration_hours || 0,
        pregnant: userData.pregnant || false,
        comorbidity: userData.comorbidity || false,
        danger_sign: userData.danger_sign || false
      };

      const data = await submitTriage(payload);

      if (data.status === "COMPLETE") {
        setResult(data);
        setIsComplete(true);
      } else {
        // Tambahkan pesan AI baru ke state messages dengan label Investigasi untuk turn berikutnya
        const aiQuestion = data.follow_up_questions[0]?.q || "Bisa jelaskan lebih lanjut?";
        setMessages(prev => [...prev, { text: userInput, isAi: false }, { text: aiQuestion, isAi: true }]);
      }
    } catch (error) {
      console.error("Triage Error:", error);
      setMessages(prev => [...prev, { text: userInput, isAi: false }, { text: "Maaf, kendala koneksi.", isAi: true }]);
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