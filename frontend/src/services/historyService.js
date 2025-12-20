// src/services/historyService.js
import api from './api';

/**
 * MENGAMBIL RIWAYAT TRIASE BERDASARKAN NIK
 * Mengakses endpoint GET /user-history/{nik} di backend
 */
export const getUserHistory = async (nik) => {
  try {
    if (!nik) throw new Error("NIK tidak boleh kosong");
    
    const response = await api.get(`/user-history/${nik}`);
    
    // Backend mengembalikan list of TriageLog
    // Kita pastikan data yang dikirim balik adalah array
    return response.data; 
  } catch (error) {
    console.error("Gagal mengambil riwayat medis:", error);
    throw error.response?.data?.detail || "Gagal memuat riwayat kesehatan.";
  }
};

/**
 * (Opsional) MENGAMBIL DETAIL TRIASE TERTENTU
 * Jika nanti ingin ada fitur klik satu riwayat untuk lihat detail lengkap
 */
export const getTriageDetail = async (triageId) => {
  try {
    const response = await api.get(`/triage-detail/${triageId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data?.detail || "Detail tidak ditemukan.";
  }
};