import React from 'react';

const TextArea = ({ label, value, onChange, placeholder, rows = 5, ...props }) => {
  return (
    <div className="w-full mb-4">
      {label && <label className="block text-gray-700 text-sm font-bold mb-2 ml-1">{label}</label>}
      <textarea
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
        className="w-full p-5 bg-white border border-gray-100 rounded-3xl shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-700 placeholder:text-gray-400 resize-none"
        {...props}
      />
    </div>
  );
};

export default TextArea;