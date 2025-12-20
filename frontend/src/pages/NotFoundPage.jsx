import React from 'react';
import { useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import Button from '../components/ui/Button';
import { Search } from 'lucide-react';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <Container className="flex flex-col items-center justify-center p-10 text-center">
      <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
        <Search size={48} className="text-gray-400" />
      </div>
      
      <h1 className="text-4xl font-black text-gray-800 mb-2">404</h1>
      <h2 className="text-xl font-bold text-gray-700 mb-4">Halaman Tidak Ditemukan</h2>
      
      <p className="text-gray-500 mb-10 leading-relaxed">
        Maaf, halaman yang Anda cari tidak tersedia atau telah dipindahkan.
      </p>

      <Button fullWidth onClick={() => navigate('/')}>
        Kembali ke Beranda
      </Button>
    </Container>
  );
};

export default NotFound;