import { useState } from 'react';
import { postTriage } from '../services/api';

export const useTriage = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [isComplete, setIsComplete] = useState(false);

  const processTriage = async (userInput, userData, currentHistory) => {
    setLoading(true);
    try {
      const finalComplaint =
        currentHistory.length === 0
          ? userInput
          : currentHistory
              .map(m =>
                m.isAi
                  ? `Investigasi: ${m.text}`
                  : `Jawaban Pasien: ${m.text}`
              )
              .join('\n') + `\nJawaban Pasien: ${userInput}`;

      const payload = {
        nik: userData.nik,
        age: parseInt(userData.age) || 0,
        complaint: finalComplaint,
        duration_hours: userData.duration_hours || 0,
        pregnant: userData.pregnant || false,
        comorbidity: userData.comorbidity || false,
        danger_sign: userData.danger_sign || false
      };

      const data = await postTriage(payload);

      if (data.status === "COMPLETE") {
        setResult(data);
        setIsComplete(true);
        return null;
      } else {
        const q = data.follow_up_questions?.[0]?.q;
        if (q) {
          setMessages(prev => [...prev, { text: q, isAi: true }]);
          return q; // 🔥 MODIFIKASI: kembalikan pertanyaan AI
        }
      }
    } catch (error) {
      console.error("Triage Error:", error);
      setMessages(prev => [...prev, { text: "Gagal memproses analisis.", isAi: true }]);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, result, isComplete, processTriage };
};
