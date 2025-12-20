import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import PanicButton from '../components/ui/PanicButton';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { getActiveUser } from '../utils/storage';
import { Activity, MessageSquare } from 'lucide-react';

const HomePage = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const active = getActiveUser();
    if (!active) navigate('/'); 
    setUser(active);
  }, [navigate]);

  // Sekarang hanya melempar profil aktif, data medis diambil di ChatPage
  const handleStartConsultation = () => {
    navigate('/chat', { state: { profile: user } });
  };

  const handlePanic = () => {
    navigate('/chat', { 
      state: { 
        profile: user,
        isPanic: true 
      } 
    });
  };

  return (
    <Container className="pb-32">
      <Header nickname={user?.nickname} onProfileClick={() => navigate('/')} />
      
      <div className="px-6 space-y-6">
        {/* Tombol Panic tetap ada untuk keselamatan */}
        <PanicButton onClick={handlePanic} />

        <Card className="text-center p-8">
          <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-4">
            <Activity className="text-blue-600" size={32} />
          </div>
          
          <h3 className="text-xl font-bold text-gray-800 mb-2">
            Mulai Pemeriksaan Mandiri
          </h3>
          <p className="text-sm text-gray-500 mb-8 leading-relaxed">
            Ceritakan keluhan Anda kepada AI Dokter. Kami akan membantu menganalisis tingkat keparahan gejala Anda.
          </p>
          
          {/* Tombol utama sekarang langsung menuju chat */}
          <Button fullWidth onClick={handleStartConsultation} className="py-4 shadow-lg shadow-blue-100">
            <MessageSquare size={20} className="mr-2" />
            Mulai Konsultasi Chat
          </Button>
        </Card>

        {/* Info Box tetap dipertahankan untuk edukasi */}
        <div className="p-4 bg-blue-50 rounded-2xl border border-blue-100">
          <p className="text-[11px] text-blue-700 leading-relaxed text-center italic">
            "Sesi konsultasi dilakukan melalui chat interaktif untuk hasil yang lebih akurat dan personal."
          </p>
        </div>
      </div>

      <Footer />
    </Container>
  );
};

export default HomePage;