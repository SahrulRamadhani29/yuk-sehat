import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import ProfileCard from '../components/profile/ProfileCard';
import AddProfileForm from '../components/profile/AddProfileForm';
import Button from '../components/ui/Button';
import { useProfile } from '../hooks/useProfile';
import logo from '../assets/images/logo.png';
// Import illustration dihapus karena tidak dipakai lagi
import { Plus } from 'lucide-react';

const WelcomePage = () => {
  const navigate = useNavigate();
  const { profiles, addProfile, selectProfile, removeProfile, loading } = useProfile();
  const [showAddForm, setShowAddForm] = useState(false);

  const handleSelect = (profile) => {
    selectProfile(profile);
    navigate('/home'); 
  };

  const handleSaveProfile = async (nickname, nik) => {
    const success = await addProfile(nickname, nik);
    if (success) setShowAddForm(false);
  };

  return (
    <Container className="p-6">
      {/* --- BAGIAN BRANDING (Hanya Logo Tunggal) --- */}
      <div className="flex flex-col items-center mt-16 mb-12">
        <img 
          src={logo} 
          alt="Yuk Sehat" 
          className="w-45 h-auto mb-9 object-contain" 
        />
        
        <h1 className="text-2xl font-black text-gray-800 text-center">
          Selamat Datang di <span className="text-black-600">Yuk Sehat</span>
        </h1>
        <p className="text-gray-500 text-center mt-2 px-4 text-sm leading-relaxed">
          Pilih profil pasien atau tambah anggota keluarga untuk mulai triase medis mandiri.
        </p>
      </div>

      {/* --- DAFTAR PROFIL --- */}
      <div className="flex-1 overflow-y-auto mb-20 px-1">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-gray-700">Daftar Profil</h3>
          <span className="text-[10px] text-blue-500 font-bold uppercase tracking-widest bg-blue-50 px-2 py-1 rounded-lg">
            {profiles.length} Tersimpan
          </span>
        </div>

        {profiles.length > 0 ? (
          profiles.map((p) => (
            <ProfileCard 
              key={p.nik} 
              nickname={p.nickname} 
              nik={p.nik} 
              onSelect={handleSelect}
              onDelete={removeProfile}
            />
          ))
        ) : (
          <div className="text-center p-10 border-2 border-dashed border-gray-100 rounded-[32px] text-gray-400 text-sm">
            Belum ada profil terdaftar.<br/>Klik tombol di bawah untuk menambah.
          </div>
        )}
      </div>

      {/* --- TOMBOL AKSI --- */}
      {!showAddForm && (
        <div className="fixed bottom-8 w-full max-w-[432px] left-1/2 -translate-x-1/2 px-6">
          <Button fullWidth onClick={() => setShowAddForm(true)}>
            <Plus size={20} className="mr-2" />
            Tambah Profil Baru
          </Button>
        </div>
      )}

      {/* --- OVERLAY FORM --- */}
      {showAddForm && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex flex-col justify-end">
          <div className="animate-slide-up">
            <AddProfileForm 
              onSave={handleSaveProfile} 
              onCancel={() => setShowAddForm(false)}
              loading={loading}
            />
          </div>
        </div>
      )}
    </Container>
  );
};

export default WelcomePage;