import React from 'react';
import { Home, History, ShieldAlert } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';

const Footer = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { icon: Home, label: 'Home', path: '/home' },
    { icon: History, label: 'Riwayat', path: '/history' },
    { icon: ShieldAlert, label: 'Bantuan', path: '/help' },
  ];

  return (
    <div className="fixed bottom-0 w-full max-w-[480px] bg-white border-t border-gray-100 px-8 py-4 flex justify-between items-center z-50">
      {navItems.map((item) => {
        const isActive = location.pathname === item.path;
        return (
          <button
            key={item.label}
            onClick={() => navigate(item.path)}
            className={`flex flex-col items-center gap-1 transition-all ${
              isActive ? 'text-blue-600 scale-110' : 'text-gray-400 hover:text-gray-600'
            }`}
          >
            <item.icon size={24} variant={isActive ? 'fill' : 'outline'} />
            <span className="text-[10px] font-medium">{item.label}</span>
          </button>
        );
      })}
    </div>
  );
};

export default Footer;