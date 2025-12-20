import React, { useState } from 'react';
import Input from '../ui/Input';
import Button from '../ui/Button';
import { User, CreditCard, X } from 'lucide-react';

const AddProfileForm = ({ onSave, onCancel, loading }) => {
  const [nickname, setNickname] = useState('');
  const [nik, setNik] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (nickname && nik) {
      onSave(nickname, nik);
    }
  };

  return (
    <div className="bg-white p-6 rounded-t-[40px] shadow-2xl border-t border-gray-100">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-800">Tambah Pasien Baru</h2>
        <button onClick={onCancel} className="p-2 bg-gray-50 rounded-full text-gray-400">
          <X size={20} />
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <Input 
          label="Nama Panggilan" 
          placeholder="Contoh: Ayah / Adik" 
          icon={User}
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          required
        />
        <Input 
          label="NIK (Nomor Induk Kependudukan)" 
          placeholder="16 digit NIK" 
          type="number"
          icon={CreditCard}
          value={nik}
          onChange={(e) => setNik(e.target.value)}
          required
        />
        
        <div className="mt-6">
          <Button type="submit" fullWidth loading={loading}>
            Simpan Profil
          </Button>
        </div>
      </form>
    </div>
  );
};

export default AddProfileForm;