import React, { useState } from 'react';
import Button from '../ui/Button';
import Input from '../ui/Input';
import { User, CreditCard, X } from 'lucide-react';

const AddProfileForm = ({ onSave, onCancel, loading }) => {
  const [nickname, setNickname] = useState('');
  const [nik, setNik] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault(); // Mencegah reload halaman
    if (!nickname || !nik) {
      alert("Harap isi Nama Panggilan dan NIK!");
      return;
    }
    // Mengirim data ke fungsi onSave yang ada di WelcomePage
    onSave(nickname, nik);
  };

  return (
    <div className="bg-white rounded-t-[40px] p-8 shadow-2xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-800">Profil Baru</h2>
        <button onClick={onCancel} className="p-2 bg-gray-50 rounded-full">
          <X size={20} className="text-gray-400" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          label="Nama Panggilan" 
          placeholder="Contoh: Ayah / Budi" 
          icon={User}
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
        />
        <Input 
          label="NIK (16 Digit)" 
          type="number"
          placeholder="3201xxxxxxxxxxxx" 
          icon={CreditCard}
          value={nik}
          onChange={(e) => setNik(e.target.value)}
        />

        <div className="pt-4">
          {/* PASTIKAN type="submit" ADA DI SINI AGAR handleSubmit JALAN */}
          <Button fullWidth type="submit" loading={loading}>
            Simpan Profil
          </Button>
        </div>
      </form>
    </div>
  );
};

export default AddProfileForm;