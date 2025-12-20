import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import ChatBubble from '../components/chat/ChatBubble';
import ChatInput from '../components/chat/ChatInput';
import TypingIndicator from '../components/chat/TypingIndicator';
import { useTriage } from '../hooks/useTriage';
import { checkNik } from '../services/api'; 
import { ArrowLeft, RefreshCw } from 'lucide-react';

const ChatPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const scrollRef = useRef(null);
  const activeProfile = location.state?.profile;

  const [currentStep, setCurrentStep] = useState('ASK_COMPLAINT');
  const [isCheckingDb, setIsCheckingDb] = useState(true);
  const [collectedData, setCollectedData] = useState({
    nik: activeProfile?.nik || '',
    age: 0,
    duration_hours: 0,
    pregnant: false,
    comorbidity: false,
    complaint: ''
  });

  const [chatHistory, setChatHistory] = useState([
    { text: `Halo ${activeProfile?.nickname || 'Pasien'}, Saya Asisten AI Yuk Sehat.`, isAi: true },
    { text: "Apa keluhan yang Anda rasakan saat ini?", isAi: true }
  ]);

  const { messages: aiMessages, loading: aiLoading, isComplete, result, processTriage } = useTriage();
  const allMessages = [...chatHistory, ...aiMessages];

  useEffect(() => {
    const syncUserAge = async () => {
      if (!activeProfile?.nik) return;
      try {
        const dbData = await checkNik(activeProfile.nik);
        if (dbData.exists && dbData.age > 0) {
          setCollectedData(prev => ({ ...prev, age: dbData.age }));
        }
      } catch (err) { console.warn("Sync usia gagal."); }
      finally { setIsCheckingDb(false); }
    };
    syncUserAge();
  }, [activeProfile]);

  useEffect(() => {
    if (!activeProfile) navigate('/');
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [allMessages, aiLoading, activeProfile, navigate]);

  useEffect(() => {
    if (isComplete && result) navigate('/result', { state: result });
  }, [isComplete, result, navigate]);

  const handleUserReply = async (text) => {
    if (aiLoading || isCheckingDb) return;

    // MODIFIKASI: Pengecekan step untuk menghindari duplikasi chat user
    if (currentStep === 'ASK_COMPLAINT') {
      setChatHistory(prev => [...prev, { text, isAi: false }]);
      const updatedData = { ...collectedData, complaint: text };
      setCollectedData(updatedData);
      
      const hasDuration = /(jam|hari|minggu|bulan)/i.test(text);
      if (!hasDuration) {
        setCurrentStep('ASK_DURATION');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Sudah berapa lama keluhan ini dirasakan?", isAi: true }]), 600);
      } else if (collectedData.age === 0) {
        setCurrentStep('ASK_AGE');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Berapa Usia Anda saat ini?", isAi: true }]), 600);
      } else {
        setCurrentStep('ASK_CONDITION');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan? (Ya/Tidak)", isAi: true }]), 600);
      }
    }
    else if (currentStep === 'ASK_DURATION') {
      setChatHistory(prev => [...prev, { text, isAi: false }]);
      if (collectedData.age === 0) {
        setCurrentStep('ASK_AGE');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Berapa Usia Anda saat ini?", isAi: true }]), 600);
      } else {
        setCurrentStep('ASK_CONDITION');
        setTimeout(() => setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan? (Ya/Tidak)", isAi: true }]), 600);
      }
    }
    else if (currentStep === 'ASK_AGE') {
      setChatHistory(prev => [...prev, { text, isAi: false }]);
      const numAge = parseInt(text.replace(/[^0-9]/g, '')) || 0;
      setCollectedData(prev => ({ ...prev, age: numAge }));
      setCurrentStep('ASK_CONDITION');
      setTimeout(() => setChatHistory(prev => [...prev, { text: "Apakah Anda sedang hamil atau memiliki penyakit bawaan? (Ya/Tidak)", isAi: true }]), 600);
    } 
    else if (currentStep === 'ASK_CONDITION') {
      // MODIFIKASI: Step ini dan selanjutnya tidak pakai setChatHistory lokal lagi karena ditangani hook
      const isSpec = text.toLowerCase().includes('ya');
      const finalData = { ...collectedData, pregnant: isSpec, comorbidity: isSpec };
      setCollectedData(finalData);
      setCurrentStep('AI_INVESTIGATION');
      processTriage(text, finalData, []); 
    }
    else {
      processTriage(text, collectedData, aiMessages);
    }
  };

  return (
    <Container className="flex flex-col h-screen bg-white">
      <div className="p-4 border-b flex items-center justify-between sticky top-0 bg-white z-10">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/home')} className="p-2"><ArrowLeft size={24} /></button>
          <div>
            <h2 className="font-bold text-gray-800">Konsultasi</h2>
            <p className="text-[10px] text-blue-500 font-bold uppercase">Pasien: {activeProfile?.nickname}</p>
          </div>
        </div>
        {(aiLoading || isCheckingDb) && <RefreshCw size={18} className="text-blue-500 animate-spin" />}
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {allMessages.map((msg, i) => <ChatBubble key={i} message={msg.text} isAi={msg.isAi} />)}
        {aiLoading && <TypingIndicator />}
        <div ref={scrollRef} />
      </div>
      <div className="p-4 bg-gray-50/50">
        <ChatInput onSend={handleUserReply} disabled={aiLoading || isComplete || isCheckingDb} placeholder="Ketik jawaban..." />
      </div>
    </Container>
  );
};

export default ChatPage;