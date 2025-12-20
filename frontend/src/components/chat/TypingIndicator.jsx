import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="flex justify-start mb-4 px-2">
      <div className="bg-gray-100 p-4 rounded-3xl rounded-tl-none flex gap-1">
        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
        <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
      </div>
    </div>
  );
};

export default TypingIndicator;