import React from 'react';
import iconGreen from '../../assets/icons/status-green.png';
import iconYellow from '../../assets/icons/status-yellow.png';
import iconRed from '../../assets/icons/status-red.png';

const ResultStatus = ({ result }) => {
  const configs = {
    MERAH: {
      icon: iconRed,
      color: "text-red-600",
      bg: "bg-red-50",
      label: "DARURAT (IGD)",
      desc: "Segera pergi ke Rumah Sakit terdekat!"
    },
    KUNING: {
      icon: iconYellow,
      color: "text-yellow-600",
      bg: "bg-yellow-50",
      label: "PERLU EVALUASI",
      desc: "Segera konsultasi ke Dokter atau Puskesmas."
    },
    HIJAU: {
      icon: iconGreen,
      color: "text-green-600",
      bg: "bg-green-50",
      label: "GEJALA RINGAN",
      desc: "Dapat dilakukan perawatan mandiri di rumah."
    }
  };

  const current = configs[result] || configs.HIJAU;

  return (
    <div className={`w-full ${current.bg} rounded-[40px] p-8 flex flex-col items-center text-center shadow-inner`}>
      <img src={current.icon} alt={result} className="w-24 h-24 mb-4 drop-shadow-md" />
      <h1 className={`text-2xl font-black ${current.color} tracking-tight`}>{current.label}</h1>
      <p className="text-gray-500 text-sm mt-2">{current.desc}</p>
    </div>
  );
};

export default ResultStatus;