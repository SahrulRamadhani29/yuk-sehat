import React from 'react';
import { Pill, AlertCircle } from 'lucide-react';

const MedicineList = ({ medicines }) => {
  if (!medicines || medicines.length === 0) return null;

  return (
    <div className="mt-6 space-y-4">
      <div className="flex items-center gap-2 mb-2">
        <Pill className="text-blue-600" size={20} />
        <h3 className="font-bold text-gray-800">Saran Perawatan & Obat</h3>
      </div>
      
      <div className="space-y-2">
        {medicines.map((item, index) => (
          <div 
            key={index} 
            className={`p-4 rounded-2xl text-sm ${item.includes('---') ? 'bg-orange-50 text-orange-700 border border-orange-100' : 'bg-white border border-gray-100 text-gray-700 shadow-sm'}`}
          >
            {item.includes('---') ? (
              <div className="flex gap-2 font-bold">
                <AlertCircle size={18} className="flex-shrink-0" />
                <span>{item.replace(/---/g, '')}</span>
              </div>
            ) : (
              <p>• {item}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default MedicineList;