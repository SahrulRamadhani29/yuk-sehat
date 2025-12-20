import React from 'react';

const Card = ({ children, className = '', onClick }) => {
  return (
    <div 
      onClick={onClick}
      className={`bg-white rounded-[32px] p-6 shadow-sm border border-gray-50 ${className} ${onClick ? 'cursor-pointer active:scale-[0.98] transition-all' : ''}`}
    >
      {children}
    </div>
  );
};

export default Card;