import React from 'react';

const Loading = ({ message = "Menganalisis data medis..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-10 space-y-4">
      <div className="relative w-20 h-20">
        <div className="absolute inset-0 border-4 border-blue-100 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
      </div>
      <p className="text-gray-500 font-medium animate-pulse">{message}</p>
    </div>
  );
};

export default Loading;