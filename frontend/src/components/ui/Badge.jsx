import React from 'react';

/**
 * Komponen Badge untuk Label Kategori
 * @param {string} children - Teks label (contoh: "Pernapasan")
 * @param {string} variant - 'default', 'success', 'warning', 'danger'
 */
const Badge = ({ children, variant = 'default', className = '' }) => {
  const baseStyles = "px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider shadow-sm border";
  
  const variants = {
    // Warna Biru (Standar Kategori)
    default: "bg-blue-50 text-blue-600 border-blue-100",
    // Warna Hijau (Hasil Aman/Rekomendasi)
    success: "bg-green-50 text-green-600 border-green-100",
    // Warna Kuning (Waspada/Moderate)
    warning: "bg-yellow-50 text-yellow-600 border-yellow-100",
    // Warna Merah (Bahaya/Darurat)
    danger: "bg-red-50 text-red-600 border-red-100",
    // Warna Abu (Lainnya)
    neutral: "bg-gray-50 text-gray-500 border-gray-100"
  };

  return (
    <span className={`${baseStyles} ${variants[variant]} ${className}`}>
      {children}
    </span>
  );
};

export default Badge;