import React from 'react';
import { MessageSquareQuote } from 'lucide-react';

const AiReason = ({ reason }) => {
  return (
    <div className="mt-6 bg-blue-50/50 p-5 rounded-3xl border border-blue-100/50">
      <div className="flex items-center gap-2 mb-3">
        <MessageSquareQuote className="text-blue-500" size={20} />
        <h4 className="text-blue-800 font-bold text-sm">Analisis Dokter AI</h4>
      </div>
      <p className="text-blue-700/80 text-sm leading-relaxed italic">
        "{reason}"
      </p>
    </div>
  );
};

export default AiReason;