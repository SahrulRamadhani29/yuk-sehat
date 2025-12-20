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

  // Logika Cek Usia (Sesuai Konsep Chat Client)
  const savedAge = activeProfile?.age;
  const hasExistingAge = savedAge && savedAge !== 0 && savedAge !== "";

  // MODIFIKASI: Mulai dari ASK_COMPLAINT sesuai permintaan
  const [currentStep, setCurrentStep] = useState('ASK_COMPLAINT');
  const [collectedData, setCollectedData] = useState({
    nik: activeProfile?.nik || '',
    age: savedAge || 0,
    duration_hours: 0,
    pregnant: false,
    comorbidity: false,
    complaint: ''
  });

  const [chatHistory, setChatHistory] = useState(() => {
    const msgs = [{ text: `Halo ${activeProfile?.nickname || 'Pasien'}, Saya Asisten AI Yuk Sehat.`, isAi: true }];
    // MODIFIKASI: Pesan awal menanyakan keluhan
    msgs.push({ text: "Apa keluhan yang Anda rasakan saat ini?", isAi: true });
    return msgs;
  });

  const { messages: aiMessages, loading: aiLoading, isComplete, result, processTriage } = useTriage();
  
  // Gabungkan chatHistory (step awal) dengan aiMessages (investigasi)
  const allMessages = [...chatHistory, ...aiMessages];

  useEffect(() => {
    if (!activeProfile) navigate('/');
  }, [activeProfile, navigate]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [allMessages, aiLoading]);

  useEffect(() => {
    if (isComplete && result) navigate('/result', { state: result });
  }, [isComplete, result, navigate]);

  // MODIFIKASI: Fungsi pembantu untuk menentukan langkah setelah Keluhan/Durasi
  const proceedToNextStepAfterComplaint = (complaintText, currentData) => {
    const hasDurationInText = /(jam|hari|minggu|bulan)/i.test(complaintText);
    
    if (!hasDurationInText) {
      setCurrentStep('ASK_DURATION');
      setTimeout(() => setChatHistory(prev => [...prev, { text: "Sudah berapa lama keluhan ini dirasakan? (Contoh: 12 jam atau 2 hari)", isAi: true }]), 600);
    } else if (!hasExistingAge) {
      setCurrentStep('ASK_AGE');
      setTimeout(() => setChatHistory(prev => [...prev, { text: "Berapa Usia Anda saat ini?", isAi: true }]), 600);
    } else {
      setCurrentStep('ASK_CONDITION');
      setTimeout(() => setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan lahir? (Ya/Tidak)", isAi: true }]), 600);
    }
  };

  const handleUserReply = async (text) => {
    if (aiLoading) return;

    // Masukkan ke UI Gelembung Chat
    setChatHistory(prev => [...prev, { text, isAi: false }]);

    // MODIFIKASI: Alur Logika Baru
    if (currentStep === 'ASK_COMPLAINT') {
      const updatedData = { ...collectedData, complaint: text };
      setCollectedData(updatedData);
      proceedToNextStepAfterComplaint(text, updatedData);
    }
    else if (currentStep === 'ASK_DURATION') {
      // Durasi akan diekstrak backend dari teks ini
      if (!hasExistingAge) {
        setCurrentStep('ASK_AGE');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Berapa Usia Anda saat ini?", isAi: true }]), 600);
      } else {
        setCurrentStep('ASK_CONDITION');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan lahir? (Ya/Tidak)", isAi: true }]), 600);
      }
    }
    else if (currentStep === 'ASK_AGE') {
      const numAge = parseInt(text.replace(/[^0-9]/g, '')) || 0;
      setCollectedData(prev => ({ ...prev, age: numAge }));
      setCurrentStep('ASK_CONDITION');
      setTimeout(() => setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan lahir? (Ya/Tidak)", isAi: true }]), 600);
    } 
    else if (currentStep === 'ASK_CONDITION') {
      const isSpec = text.toLowerCase().includes('ya');
      const finalData = { ...collectedData, pregnant: isSpec, comorbidity: isSpec };
      setCollectedData(finalData);
      setCurrentStep('AI_PROCESSING');
      // Kirim ke AI Investigasi
      processTriage(text, finalData, aiMessages);
    }
    else {
      processTriage(text, collectedData, aiMessages);
    }
  };

  return (
    <Container className="flex flex-col h-screen bg-white">
      <div className="p-4 border-b border-gray-100 flex items-center justify-between sticky top-0 bg-white z-10">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/home')} className="p-2 text-gray-600"><ArrowLeft size={24} /></button>
          <div>
            <h2 className="font-bold text-gray-800 text-lg">Konsultasi</h2>
            <p className="text-[10px] text-blue-500 font-bold uppercase tracking-widest">Pasien: {activeProfile?.nickname}</p>
          </div>
        </div>
        {(aiLoading || currentStep === 'AI_PROCESSING') && <RefreshCw size={18} className="text-blue-500 animate-spin" />}
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {allMessages.map((msg, i) => <ChatBubble key={i} message={msg.text} isAi={msg.isAi} />)}
        {(aiLoading || currentStep === 'AI_PROCESSING') && <TypingIndicator />}
        <div ref={scrollRef} />
      </div>
      <div className="p-4 bg-gray-50/50">
        <ChatInput onSend={handleUserReply} disabled={aiLoading || isComplete} placeholder="Ketik jawaban..." />
      </div>
    </Container>
  );
};

export default ChatPage;