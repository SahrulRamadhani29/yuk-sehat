import React from 'react';

const Input = ({ label, type = 'text', value, onChange, placeholder, icon: Icon, ...props }) => {
  return (
    <div className="w-full mb-4">
      {label && <label className="block text-gray-700 text-sm font-bold mb-2 ml-1">{label}</label>}
      <div className="relative flex items-center">
        {Icon && (
          <div className="absolute left-4 text-gray-400">
            <Icon size={20} />
          </div>
        )}
        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className={`w-full py-4 ${Icon ? 'pl-12' : 'px-5'} pr-5 bg-white border border-gray-100 rounded-2xl shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-700 placeholder:text-gray-400`}
          {...props}
        />
      </div>
    </div>
  );
};

export default Input;