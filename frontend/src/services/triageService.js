// src/services/triageService.js
import api from './api';

export const submitTriage = async (payload) => {
  try {
    // Payload sesuai TriageInput di backend
    const response = await api.post('/triage', payload);
    return response.data; // Mengembalikan TriageResponse
  } catch (error) {
    console.error("Triage Service Error:", error);
    throw error;
  }
};