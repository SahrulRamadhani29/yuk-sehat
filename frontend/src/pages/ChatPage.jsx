import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import ChatBubble from '../components/chat/ChatBubble';
import ChatInput from '../components/chat/ChatInput';
import TypingIndicator from '../components/chat/TypingIndicator';
import { useTriage } from '../hooks/useTriage';
import { ArrowLeft, RefreshCw } from 'lucide-react';

const ChatPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const scrollRef = useRef(null);
  
  const activeProfile = location.state?.profile;
  
  const [currentStep, setCurrentStep] = useState('ASK_AGE');
  const [collectedData, setCollectedData] = useState({
    nik: activeProfile?.nik || '',
    age: '',
    duration_hours: 0, // Inisialisasi 0 agar backend bisa mengekstrak dari teks jika perlu
    pregnant: false,
    comorbidity: false,
    complaint: ''
  });

// State pesan lokal dengan bubble terpisah dan baris baru
const [chatHistory, setChatHistory] = useState([
  { 
    text: `Halo ${activeProfile?.nickname || 'Pasien'}, Saya Asisten AI Yuk Sehat.\nMari kita mulai pemeriksaan.`, 
    isAi: true 
  },
  { 
    text: "Berapa Usia Anda?", 
    isAi: true 
  }
]);

  const { 
    messages: aiMessages, 
    loading: aiLoading, 
    isComplete, 
    result, 
    processTriage 
  } = useTriage();

  const allMessages = [...chatHistory, ...aiMessages];

  useEffect(() => {
    if (!activeProfile) {
      navigate('/');
      return;
    }
  }, [activeProfile, navigate]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [allMessages, aiLoading]);

  useEffect(() => {
    if (isComplete && result) {
      navigate('/result', { state: result });
    }
  }, [isComplete, result, navigate]);

  const handleUserReply = async (text) => {
    setChatHistory(prev => [...prev, { text, isAi: false }]);

    if (currentStep === 'ASK_AGE') {
      // Backend akan memproses string ini melalui Regex
      setCollectedData(prev => ({ ...prev, age: text })); 
      setTimeout(() => {
        setChatHistory(prev => [...prev, { text: "Sudah berapa lama Anda merasakan keluhan ini?", isAi: true }]);
        setCurrentStep('ASK_DURATION');
      }, 800);
    } 
    else if (currentStep === 'ASK_DURATION') {
      // Kita kirim string teks apa adanya agar diekstrak oleh extract_duration_from_text di Backend
      setCollectedData(prev => ({ ...prev, duration_hours: text })); 
      setTimeout(() => {
        setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan lahir?", isAi: true }]);
        setCurrentStep('ASK_CONDITION');
      }, 800);
    }
    else if (currentStep === 'ASK_CONDITION') {
      const isSpecial = text.toLowerCase().includes('ya');
      setCollectedData(prev => ({ ...prev, pregnant: isSpecial, comorbidity: isSpecial }));
      setTimeout(() => {
        setChatHistory(prev => [...prev, { text: "Terakhir, ceritakan detail keluhan yang Anda rasakan saat ini.", isAi: true }]);
        setCurrentStep('ASK_COMPLAINT');
      }, 800);
    }
    else if (currentStep === 'ASK_COMPLAINT') {
      const finalPayload = { ...collectedData, complaint: text };
      setCurrentStep('AI_PROCESSING');
      processTriage(text, finalPayload); 
    }
    else {
      processTriage(text, collectedData);
    }
  };

  return (
    <Container className="flex flex-col h-screen bg-white">
      <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-white sticky top-0 z-10">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/home')} className="p-2 hover:bg-gray-50 rounded-full">
            <ArrowLeft size={24} className="text-gray-600" />
          </button>
          <div>
            <h2 className="font-bold text-gray-800 text-lg">Sesi Konsultasi</h2>
            <p className="text-[10px] text-blue-500 font-bold uppercase tracking-widest">
              Pasien: {activeProfile?.nickname}
            </p>
          </div>
        </div>
        {currentStep === 'AI_PROCESSING' && (
          <RefreshCw size={18} className="text-blue-500 animate-spin" />
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {allMessages.map((msg, index) => (
          <ChatBubble key={index} message={msg.text} isAi={msg.isAi} />
        ))}
        {(aiLoading || currentStep === 'AI_PROCESSING') && <TypingIndicator />}
        <div ref={scrollRef} />
      </div>

      <div className="p-4 bg-gray-50/50">
        {/* PROPS inputType DIPAKSA 'text' AGAR USER BISA MENGETIK SATUAN */}
        <ChatInput 
          onSend={handleUserReply} 
          disabled={aiLoading || isComplete}
          inputType="text" 
          placeholder={
            currentStep === 'ASK_AGE' ? "Contoh: 14 tahun..." :
            currentStep === 'ASK_DURATION' ? "Contoh: 2 hari..." :
            "Ketik jawaban di sini..."
          }
        />
      </div>
    </Container>
  );
};

export default ChatPage;