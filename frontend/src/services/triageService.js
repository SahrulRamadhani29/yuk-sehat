import api from './api';

export const submitTriage = async (payload) => {
  try {
    const response = await api.post('/triage', payload);
    return response.data;
  } catch (error) {
    console.error("Triage Service Error:", error);
    throw error;
  }
};