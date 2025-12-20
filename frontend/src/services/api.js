import axios from 'axios';

const API_BASE_URL = 'https://yuk-sehat.onrender.com'; 

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

export const checkNik = async (nik) => {
  const response = await api.get(`/check-nik/${nik}`);
  return response.data;
};

export const postTriage = async (payload) => {
  const response = await api.post('/triage', payload);
  return response.data;
};

export const getUserHistory = async (nik) => {
  const response = await api.get(`/user-history/${nik}`);
  return response.data;
};

export default api;