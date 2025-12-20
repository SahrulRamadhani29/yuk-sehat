import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Import Pages yang sudah kita buat
import WelcomePage from './pages/WelcomePage';
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import ResultPage from './pages/ResultPage';
import HistoryPage from './pages/HistoryPage';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Router>
      <Routes>
        {/* Rute Awal: Pilih Profil */}
        <Route path="/" element={<WelcomePage />} />
        
        {/* Rute Dashboard & Input Keluhan */}
        <Route path="/home" element={<HomePage />} />
        
        {/* Rute Investigasi AI (Chat) */}
        <Route path="/chat" element={<ChatPage />} />
        
        {/* Rute Hasil Analisis & Obat */}
        <Route path="/result" element={<ResultPage />} />
        
        {/* Rute Riwayat Medis */}
        <Route path="/history" element={<HistoryPage />} />
        
        {/* Penanganan Halaman Tidak Ditemukan */}
        <Route path="/404" element={<NotFound />} />
        <Route path="*" element={<Navigate to="/404" />} />
      </Routes>
    </Router>
  );
}

export default App;