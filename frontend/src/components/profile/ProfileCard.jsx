import React from 'react';
import { Trash2 } from 'lucide-react';
import iconUser from '../../assets/icons/icon-user-default.png';

const ProfileCard = ({ nickname, nik, onSelect, onDelete }) => {
  return (
    <div className="w-full bg-white p-4 rounded-3xl shadow-sm border border-gray-100 flex items-center justify-between mb-3 hover:border-blue-300 transition-all active:scale-95 cursor-pointer">
      <div className="flex items-center gap-4" onClick={() => onSelect({ nickname, nik })}>
        <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center overflow-hidden">
          <img src={iconUser} alt="Avatar" className="w-8 h-8 object-contain" />
        </div>
        <div>
          <h3 className="font-bold text-gray-800 text-lg">{nickname}</h3>
          <p className="text-gray-400 text-sm">{nik.substring(0, 4)}**********</p>
        </div>
      </div>
      
      {/* Tombol Hapus Profil dari HP/Laptop ini */}
      <button 
        onClick={(e) => {
          e.stopPropagation(); // Biar tidak ketrigger onSelect-nya
          onDelete(nik);
        }}
        className="p-2 text-gray-300 hover:text-red-500 transition-colors"
      >
        <Trash2 size={20} />
      </button>
    </div>
  );
};

export default ProfileCard;