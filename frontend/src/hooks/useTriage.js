import { useState } from 'react';
import { postTriage } from '../services/api';

export const useTriage = () => {
  const [messages, setMessages] = useState([]); 
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null); 
  const [isComplete, setIsComplete] = useState(false);

// src/hooks/useTriage.js -> processTriage
  const processTriage = async (userInput, userData, currentHistory) => {
    setLoading(true);
    try {
      // MODIFIKASI: Pastikan baris pertama 100% murni tanpa label apapun
      let finalComplaint = currentHistory.length === 0 
        ? userInput 
        : currentHistory.map(m => (m.isAi ? `Investigasi: ${m.text}` : `Jawaban Pasien: ${m.text}`)).join("\n") + `\nJawaban Pasien: ${userInput}`;

      const payload = {
        nik: userData.nik,
        age: parseInt(userData.age) || 0,
        complaint: finalComplaint,
        duration_hours: userData.duration_hours || 0,
        pregnant: userData.pregnant || false,
        comorbidity: userData.comorbidity || false,
        danger_sign: userData.danger_sign || false
      };
      // ... sisanya tetap

      const data = await postTriage(payload);

      if (data.status === "COMPLETE") {
        setResult(data);
        setIsComplete(true);
      } else {
        const aiQuestion = data.follow_up_questions[0]?.q || "Bisa jelaskan lebih lanjut?";
        // MODIFIKASI: Hanya tambahkan pertanyaan AI, pesan user sudah ditambahkan di atas
        setMessages(prev => [...prev, { text: aiQuestion, isAi: true }]);
      }
    } catch (error) {
      console.error("Triage Error:", error);
      setMessages(prev => [...prev, { text: "Gagal memproses analisis.", isAi: true }]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, result, isComplete, processTriage };
};