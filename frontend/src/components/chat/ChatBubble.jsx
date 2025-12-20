import React from 'react';
import doctorIcon from '../../assets/images/doctor-ai.png';

const ChatBubble = ({ message, isAi }) => {
  return (
    <div className={`flex w-full mb-4 ${isAi ? 'justify-start' : 'justify-end'}`}>
      {isAi && (
        <div className="w-10 h-10 rounded-full bg-blue-100 flex-shrink-0 mr-2 flex items-center justify-center overflow-hidden border border-blue-200">
          <img src={doctorIcon} alt="AI" className="w-8 h-8 object-contain" />
        </div>
      )}
      
      <div className={`max-w-[75%] p-4 rounded-3xl text-sm leading-relaxed shadow-sm ${
        isAi 
        ? 'bg-white text-gray-800 rounded-tl-none border border-gray-100' 
        : 'bg-blue-600 text-white rounded-tr-none'
      }`}>
        {message}
      </div>
    </div>
  );
};

export default ChatBubble;