import React, { useEffect } from 'react';
import Container from '../components/layout/Container';
import Footer from '../components/layout/Footer';
import Badge from '../components/ui/Badge';
import Card from '../components/ui/Card';
import Loading from '../components/ui/Loading';
import { useHistory } from '../hooks/useHistory';
import { getActiveUser } from '../utils/storage';
import { formatDate } from '../utils/formatter';
import { ClipboardList, ChevronRight, SearchX } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const HistoryPage = () => {
  const navigate = useNavigate();
  const user = getActiveUser();
  const { historyData, loading, error, fetchHistory } = useHistory();

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }
    fetchHistory(user.nik); // Ambil riwayat berdasarkan NIK aktif
  }, [user?.nik]);

  const getStatusVariant = (result) => {
    if (result === 'MERAH') return 'danger';
    if (result === 'KUNING') return 'warning';
    return 'success';
  };

  return (
    <Container className="pb-32 bg-[#F8F9FA]">
      {/* Header Statis Riwayat */}
      <div className="p-6 bg-white rounded-b-[40px] shadow-sm mb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-blue-50 rounded-2xl text-blue-600">
            <ClipboardList size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">Riwayat Medis</h1>
            <p className="text-xs text-gray-400">Pasien: {user?.nickname}</p>
          </div>
        </div>
      </div>

      <div className="px-6">
        {loading ? (
          <Loading message="Mengambil catatan medis..." />
        ) : error ? (
          <div className="p-6 text-center bg-red-50 rounded-3xl text-red-500 text-sm">
            {error}
          </div>
        ) : historyData.length > 0 ? (
          <div className="space-y-4">
            {historyData.map((log) => (
              <Card key={log.id} className="hover:border-blue-200 transition-all border-l-4 border-l-blue-500">
                <div className="flex justify-between items-start mb-3">
                  <span className="text-[10px] font-bold text-gray-400 uppercase">
                    {formatDate(log.date)} {/* */}
                  </span>
                  <Badge variant={getStatusVariant(log.result)}>
                    {log.result}
                  </Badge>
                </div>
                
                <h4 className="font-bold text-gray-800 mb-1 line-clamp-1 italic">
                  "{log.complaint.substring(0, 50)}..."
                </h4>
                
                <div className="flex justify-between items-center mt-4 pt-3 border-t border-gray-50">
                  <span className="text-[11px] text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-lg uppercase">
                    {log.category || 'UMUM'}
                  </span>
                  <button className="flex items-center text-xs text-gray-400 font-medium">
                    Detail <ChevronRight size={14} />
                  </button>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-20 text-gray-400">
            <SearchX size={48} className="mb-4 opacity-20" />
            <p className="text-sm font-medium">Belum ada riwayat pemeriksaan.</p>
          </div>
        )}
      </div>

      <Footer /> {/* Navigasi bawah */}
    </Container>
  );
};

export default HistoryPage;