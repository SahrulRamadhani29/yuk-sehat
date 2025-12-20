import React from 'react';
import iconPanic from '../../assets/icons/icon-panic.png';

const PanicButton = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="w-full bg-red-50 p-6 rounded-[32px] border-2 border-red-100 flex items-center gap-4 hover:bg-red-100 transition-all active:scale-95 group"
    >
      <div className="w-16 h-16 bg-red-500 rounded-2xl flex items-center justify-center shadow-lg shadow-red-200 group-hover:rotate-12 transition-transform">
        <img src={iconPanic} alt="Emergency" className="w-10 h-10 invert" />
      </div>
      <div className="text-left">
        <h3 className="text-red-600 font-bold text-lg">Keadaan Darurat?</h3>
        <p className="text-red-400 text-sm">Klik jika butuh bantuan medis segera</p>
      </div>
    </button>
  );
};

export default PanicButton;