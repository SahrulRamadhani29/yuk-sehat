import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import ResultStatus from '../components/triage/ResultStatus';
import MedicineList from '../components/triage/MedicineList';
import AiReason from '../components/triage/AiReason';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import { Share2, Home, AlertTriangle, MapPin, Phone } from 'lucide-react';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Mengambil data hasil dari ChatPage
  const data = location.state;

  if (!data) {
    navigate('/home');
    return null;
  }

  // Tentukan varian badge berdasarkan tingkat urgensi AI
  const getBadgeVariant = (urgency) => {
    if (urgency === 'HIGH') return 'danger';
    if (urgency === 'MEDIUM') return 'warning';
    return 'default';
  };

  const openMapSearch = (query) => {
    window.open(`https://www.google.com/maps/search/${encodeURIComponent(query)}`, '_blank');
  };

  return (
    <Container className="pb-10 bg-white">
      {/* 1. Header & Kategori */}
      <div className="p-6 flex flex-col items-center">
        <div className="flex justify-between w-full items-center mb-6">
          <button onClick={() => navigate('/home')} className="p-2 bg-gray-50 rounded-full text-gray-400">
            <Home size={20} />
          </button>
          <Badge variant={getBadgeVariant(data.ai_analysis?.urgency)}>
            Kategori: {data.category?.replace(/_/g, ' ').toUpperCase()}
          </Badge>
          <button className="p-2 bg-gray-50 rounded-full text-gray-400">
            <Share2 size={20} />
          </button>
        </div>

        {/* 2. Status Visual Utama */}
        <ResultStatus result={data.triage_result} />
      </div>

      <div className="px-6 space-y-2">
        {/* 3. Penjelasan AI */}
        <AiReason reason={data.ai_analysis?.reason} />

        {/* 4. Rekomendasi Obat (Hanya jika bukan MERAH) */}
        {data.triage_result !== 'MERAH' ? (
          <MedicineList medicines={data.recommendation} />
        ) : (
          <div className="mt-6 p-5 bg-red-600 rounded-[32px] text-white shadow-lg shadow-red-200">
            <div className="flex items-center gap-3 mb-2">
              <AlertTriangle size={24} />
              <h3 className="font-bold">Tindakan Segera:</h3>
            </div>
            <p className="text-sm opacity-90 leading-relaxed">
              Kondisi Anda memerlukan penanganan medis profesional segera. Mohon segera hubungi layanan darurat atau menuju Puskesmas terdekat.
            </p>

            <div className="mt-4 space-y-3">
              <Button
                fullWidth
                variant="danger"
                onClick={() => window.open('tel:119')}
              >
                <Phone size={16} className="mr-2" />
                Hubungi 119
              </Button>

              <Button
                fullWidth
                variant="outline"
                onClick={() => openMapSearch('puskesmas terdekat')}
              >
                <MapPin size={16} className="mr-2" />
                Puskesmas Terdekat
              </Button>
            </div>
          </div>
        )}

        {/* 5. Tombol Aksi Tambahan Berdasarkan Status */}
        {data.triage_result === 'HIJAU' && (
          <div className="pt-6">
            <Button
              fullWidth
              variant="outline"
              onClick={() => openMapSearch('apotek terdekat')}
            >
              <MapPin size={16} className="mr-2" />
              Apotek Terdekat
            </Button>
          </div>
        )}

        {data.triage_result === 'KUNING' && (
          <div className="pt-6 space-y-3">
            <Button
              fullWidth
              variant="outline"
              onClick={() => openMapSearch('puskesmas terdekat')}
            >
              <MapPin size={16} className="mr-2" />
              Puskesmas Terdekat
            </Button>

            <Button
              fullWidth
              variant="outline"
              onClick={() => openMapSearch('apotek terdekat')}
            >
              <MapPin size={16} className="mr-2" />
              Apotek Terdekat
            </Button>

            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-xl text-sm text-yellow-800 leading-relaxed">
              <strong>Perhatian:</strong> Anda harus memantau dan menyampaikan kondisi kesehatan Anda selama 24 jam ke depan.
            </div>
          </div>
        )}

        {/* 6. Tombol Aksi Akhir */}
        <div className="pt-8 pb-4">
          <Button variant="outline" fullWidth onClick={() => navigate('/home')}>
            Selesai & Kembali ke Home
          </Button>
          <p className="text-[10px] text-gray-400 text-center mt-4 px-4 leading-tight italic">
            *Hasil ini bersifat informatif berdasarkan data yang Anda berikan. 
            Jangan menunda pemeriksaan fisik jika gejala memhuruk.
          </p>
        </div>
      </div>
    </Container>
  );
};

export default ResultPage;
