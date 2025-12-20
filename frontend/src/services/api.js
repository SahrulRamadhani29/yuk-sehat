// src/services/api.js
import axios from 'axios';

// GANTI URL INI jika sudah dideploy (misal ke Render/Railways)
// Jika masih tahap koding di laptop, biarkan localhost
const API_BASE_URL = 'https://yuk-sehat.onrender.com'; 
//const API_BASE_URL = 'http://127.0.0.1:8000'; 

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 1. CEK NIK KE BACKEND
 * Memastikan NIK valid dan mengambil data lama jika ada
 */
export const checkNik = async (nik) => {
  try {
    const response = await api.get(`/check-nik/${nik}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || "Gagal menghubungi server";
  }
};

/**
 * 2. KIRIM TRIASE / KELUHAN
 * Mengirim input pasien ke sistem AI Mistral & Rule Engine
 */
export const postTriage = async (payload) => {
  try {
    // Payload berisi: nik, age, complaint, duration_hours, pregnant, comorbidity, danger_sign
    const response = await api.post('/triage', payload);
    return response.data;
  } catch (error) {
    throw error.response?.data || "Gagal memproses analisis";
  }
};

/**
 * 3. AMBIL RIWAYAT
 * Menampilkan catatan kesehatan pasien di masa lalu
 */
export const getUserHistory = async (nik) => {
  try {
    const response = await api.get(`/user-history/${nik}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || "Gagal mengambil riwayat";
  }
};

export default api;