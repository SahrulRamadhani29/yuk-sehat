// src/hooks/useHistory.js
import { useState } from 'react';
import { getUserHistory } from '../services/historyService';

export const useHistory = () => {
  const [historyData, setHistoryData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = async (nik) => {
    if (!nik) return;
    setLoading(true);
    try {
      const data = await getUserHistory(nik); //
      setHistoryData(data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return { historyData, loading, error, fetchHistory };
};