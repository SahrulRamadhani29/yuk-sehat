import React from 'react';
import { Bell } from 'lucide-react';
import iconUser from '../../assets/icons/icon-user-default.png';

const Header = ({ nickname, onProfileClick }) => {
  return (
    <div className="w-full p-6 flex justify-between items-center bg-white rounded-b-[40px] shadow-sm mb-6">
      <div className="flex items-center gap-4" onClick={onProfileClick} style={{ cursor: 'pointer' }}>
        <div className="w-14 h-14 rounded-full overflow-hidden border-2 border-gray-100 bg-gray-50 flex items-center justify-center">
          <img 
            src={iconUser} 
            alt="Profile" 
            className="w-10 h-10 object-contain"
          />
        </div>
        <div>
          <p className="text-gray-500 text-sm">Halo,</p>
          <h2 className="text-xl font-bold text-gray-800">{nickname || 'Rama'}!</h2>
        </div>
      </div>
      
      <button className="p-3 bg-gray-50 rounded-2xl text-gray-400 hover:text-blue-500 transition-colors">
        <Bell size={24} />
      </button>
    </div>
  );
};

export default Header;