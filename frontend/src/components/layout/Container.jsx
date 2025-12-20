import React from 'react';

/**
 * Container Utama
 * Menjaga lebar konten maksimal 480px (Ukuran standar Mobile App)
 * agar rapi di tengah layar laptop/desktop.
 */
const Container = ({ children, className = '' }) => {
  return (
    <div className="min-h-screen bg-gray-50 flex justify-center items-start">
      <div 
        className={`w-full max-w-[480px] min-h-screen bg-[#F8F9FA] shadow-xl flex flex-col relative ${className}`}
      >
        {children}
      </div>
    </div>
  );
};

export default Container;