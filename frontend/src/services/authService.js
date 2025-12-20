// src/services/authService.js
import api from './api';

export const validateNik = async (nik) => {
  try {
    const response = await api.get(`/check-nik/${nik}`);
    return response.data; // Mengembalikan { exists: true/false, age: ... }
  } catch (error) {
    console.error("Auth Service Error:", error);
    throw error;
  }
};