import React, { useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import ChatBubble from '../components/chat/ChatBubble';
import ChatInput from '../components/chat/ChatInput';
import TypingIndicator from '../components/chat/TypingIndicator';
import { useTriage } from '../hooks/useTriage';
import { ArrowLeft } from 'lucide-react';

const ChatPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const scrollRef = useRef(null);
  
  // Mengambil data awal dari HomePage
  const initialData = location.state;
  
  const { 
    messages, 
    loading, 
    isComplete, 
    result, 
    processTriage 
  } = useTriage();

  // Jalankan analisis pertama kali saat halaman dibuka
  useEffect(() => {
    if (!initialData) {
      navigate('/home');
      return;
    }
    processTriage(initialData.complaint, initialData);
  }, []);

  // Auto-scroll ke bawah saat ada pesan baru
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Jika sudah COMPLETE, pindah ke halaman hasil
  useEffect(() => {
    if (isComplete && result) {
      navigate('/result', { state: result });
    }
  }, [isComplete, result, navigate]);

  return (
    <Container className="flex flex-col h-screen bg-white">
      {/* Header Chat Ringkas */}
      <div className="p-4 border-b border-gray-100 flex items-center gap-4 bg-white sticky top-0 z-10">
        <button onClick={() => navigate('/home')} className="p-2 hover:bg-gray-50 rounded-full">
          <ArrowLeft size={24} className="text-gray-600" />
        </button>
        <div>
          <h2 className="font-bold text-gray-800">Investigasi Gejala</h2>
          <p className="text-[10px] text-green-500 font-bold uppercase tracking-widest">AI Dokter Aktif</p>
        </div>
      </div>

      {/* Area Pesan Chat */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, index) => (
          <ChatBubble key={index} message={msg.text} isAi={msg.isAi} />
        ))}
        
        {loading && <TypingIndicator />}
        <div ref={scrollRef} />
      </div>

      {/* Input Jawaban */}
      <div className="p-2">
        <ChatInput 
          onSend={(text) => processTriage(text, initialData)} 
          disabled={loading || isComplete} 
        />
      </div>
    </Container>
  );
};

export default ChatPage;