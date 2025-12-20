import React, { useState } from 'react';
import { SendHorizontal } from 'lucide-react';

const ChatInput = ({ onSend, disabled }) => {
  const [text, setText] = useState('');

  const handleSend = () => {
    if (text.trim() && !disabled) {
      onSend(text);
      setText('');
    }
  };

  return (
    <div className="p-4 bg-white border-t border-gray-100 flex items-center gap-3">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Ketik jawaban Anda..."
        disabled={disabled}
        className="flex-1 py-3 px-5 bg-gray-50 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all text-sm"
      />
      <button
        onClick={handleSend}
        disabled={disabled || !text.trim()}
        className={`p-3 rounded-2xl transition-all ${
          text.trim() && !disabled ? 'bg-blue-600 text-white shadow-md active:scale-95' : 'bg-gray-100 text-gray-400 cursor-not-allowed'
        }`}
      >
        <SendHorizontal size={20} />
      </button>
    </div>
  );
};

export default ChatInput;