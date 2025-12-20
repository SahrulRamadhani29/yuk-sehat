import React from 'react';

/**
 * Komponen Button Global
 * @param {string} variant - 'primary' (biru), 'danger' (merah), 'outline' (putih)
 * @param {boolean} fullWidth - Jika true, tombol akan selebar container
 * @param {boolean} loading - Jika true, menampilkan status loading
 */
const Button = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  type = 'button', 
  fullWidth = false, 
  disabled = false,
  loading = false,
  className = '' 
}) => {
  
  // Penentuan warna berdasarkan variant sesuai desain prototype
  const baseStyles = "py-3 px-6 rounded-2xl font-semibold transition-all duration-200 active:scale-95 flex items-center justify-center gap-2";
  
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 shadow-md",
    danger: "bg-red-500 text-white hover:bg-red-600 shadow-md",
    outline: "border-2 border-blue-600 text-blue-600 bg-transparent hover:bg-blue-50",
    secondary: "bg-white text-gray-700 border border-gray-200 shadow-sm"
  };

  const widthStyle = fullWidth ? "w-full" : "w-auto";
  const disabledStyle = (disabled || loading) ? "opacity-50 cursor-not-allowed" : "cursor-pointer";

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseStyles} ${variants[variant]} ${widthStyle} ${disabledStyle} ${className}`}
    >
      {loading ? (
        <>
          <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>Memproses...</span>
        </>
      ) : children}
    </button>
  );
};

export default Button;