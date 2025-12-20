import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import ProfileCard from '../components/profile/ProfileCard';
import AddProfileForm from '../components/profile/AddProfileForm';
import Button from '../components/ui/Button';
import { useProfile } from '../hooks/useProfile';
import logo from '../assets/images/logo.png';
import illustration from '../assets/images/illustration-welcome.png';
import { Plus } from 'lucide-react';

const WelcomePage = () => {
  const navigate = useNavigate();
  const { profiles, addProfile, selectProfile, removeProfile, loading } = useProfile();
  const [showAddForm, setShowAddForm] = useState(false);

  const handleSelect = (profile) => {
    selectProfile(profile);
    navigate('/home'); // Pindah ke Dashboard setelah pilih profil
  };

  const handleSaveProfile = async (nickname, nik) => {
    const success = await addProfile(nickname, nik);
    if (success) setShowAddForm(false);
  };

  return (
    <Container className="p-6">
      {/* Bagian Atas: Branding sesuai desain */}
      <div className="flex flex-col items-center mt-10 mb-8">
        <img src={logo} alt="Yuk Sehat" className="h-12 mb-4" />
        <img src={illustration} alt="Health illustration" className="w-64 mb-6" />
        <h1 className="text-2xl font-black text-gray-800 text-center">
          Selamat Datang di <span className="text-blue-600">Yuk Sehat</span>
        </h1>
        <p className="text-gray-500 text-center mt-2 px-4">
          Pilih profil pasien atau tambah anggota keluarga untuk mulai triase.
        </p>
      </div>

      {/* Daftar Profil */}
      <div className="flex-1 overflow-y-auto mb-20">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-gray-700">Daftar Profil</h3>
          <span className="text-xs text-blue-500 font-bold uppercase tracking-widest bg-blue-50 px-2 py-1 rounded-lg">
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
          <div className="text-center p-8 border-2 border-dashed border-gray-100 rounded-[32px] text-gray-400 text-sm">
            Belum ada profil terdaftar di perangkat ini.
          </div>
        )}
      </div>

      {/* Tombol Tambah Profil */}
      {!showAddForm && (
        <div className="fixed bottom-8 w-full max-w-[432px] left-1/2 -translate-x-1/2 px-6">
          <Button fullWidth onClick={() => setShowAddForm(true)}>
            <Plus size={20} />
            Tambah Profil Baru
          </Button>
        </div>
      )}

      {/* Form Overlay (Bottom Sheet Effect) */}
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