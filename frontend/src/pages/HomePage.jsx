import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import PanicButton from '../components/ui/PanicButton';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import TextArea from '../components/ui/TextArea';
import Button from '../components/ui/Button';
import { getActiveUser } from '../utils/storage';
import { Clock, UserCircle, Activity } from 'lucide-react';

const HomePage = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  
  // State Input sesuai TriageInput di Backend
  const [formData, setFormData] = useState({
    age: '',
    duration_hours: '',
    complaint: '',
    pregnant: false,
    comorbidity: false
  });

  useEffect(() => {
    const active = getActiveUser();
    if (!active) navigate('/'); // Tendang ke welcome jika belum pilih profil
    setUser(active);
  }, [navigate]);

  const handleStartTriage = () => {
    if (!formData.complaint || !formData.age) {
      alert("Mohon isi usia dan keluhan Anda.");
      return;
    }
    // Kirim data ke halaman Chat untuk investigasi AI
    navigate('/chat', { state: { ...formData, nik: user.nik } });
  };

  const handlePanic = () => {
    // Mode Darurat Langsung
    navigate('/chat', { 
      state: { 
        ...formData, 
        nik: user.nik, 
        danger_sign: true, 
        complaint: "DARURAT: Pasien menekan tombol panic." 
      } 
    });
  };

  return (
    <Container className="pb-32">
      <Header nickname={user?.nickname} onProfileClick={() => navigate('/')} />
      
      <div className="px-6 space-y-6">
        {/* Tombol Panic sesuai Konsep Safety */}
        <PanicButton onClick={handlePanic} />

        <Card>
          <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
            <Activity className="text-blue-600" size={20} />
            Data Pemeriksaan
          </h3>
          
          <div className="grid grid-cols-2 gap-4">
            <Input 
              label="Usia (Tahun)" 
              type="number" 
              placeholder="30"
              icon={UserCircle}
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: e.target.value })}
            />
            <Input 
              label="Durasi (Jam)" 
              type="number" 
              placeholder="12"
              icon={Clock}
              value={formData.duration_hours}
              onChange={(e) => setFormData({ ...formData, duration_hours: e.target.value })}
            />
          </div>

          <div className="flex gap-6 mb-4 px-1">
            <label className="flex items-center gap-2 cursor-pointer">
              <input 
                type="checkbox" 
                className="w-5 h-5 rounded-lg border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={formData.pregnant}
                onChange={(e) => setFormData({ ...formData, pregnant: e.target.checked })}
              />
              <span className="text-sm text-gray-600">Hamil?</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input 
                type="checkbox" 
                className="w-5 h-5 rounded-lg border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={formData.comorbidity}
                onChange={(e) => setFormData({ ...formData, comorbidity: e.target.checked })}
              />
              <span className="text-sm text-gray-600">Komorbid?</span>
            </label>
          </div>

          <TextArea 
            label="Apa yang Anda rasakan?" 
            placeholder="Ceritakan keluhan Anda secara detail di sini..."
            value={formData.complaint}
            onChange={(e) => setFormData({ ...formData, complaint: e.target.value })}
          />

          <Button fullWidth onClick={handleStartTriage} className="mt-2">
            Mulai Analisis AI
          </Button>
        </Card>

        <div className="p-4 bg-blue-50 rounded-2xl border border-blue-100">
          <p className="text-xs text-blue-700 leading-relaxed text-center italic">
            "Sistem AI akan menanyakan beberapa pertanyaan tambahan untuk memastikan diagnosis yang akurat."
          </p>
        </div>
      </div>

      <Footer />
    </Container>
  );
};

export default HomePage;