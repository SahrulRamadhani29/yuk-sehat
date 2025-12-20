// src/hooks/useProfile.js
import { useState, useEffect } from 'react';
import * as storage from '../utils/storage';
import { validateNik } from '../services/authService';

export const useProfile = () => {
  const [profiles, setProfiles] = useState([]);
  const [activeUser, setActiveUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setProfiles(storage.getProfiles());
    setActiveUser(storage.getActiveUser());
  }, []);

// Di dalam src/hooks/useProfile.js
// Cuplikan perbaikan logika di useProfile.js
const addProfile = async (nickname, nik) => {
  setLoading(true);
  try {
    const response = await validateNik(nik); 
    const ageFromDb = response.age || 0; // MODIFIKASI: Ambil usia dari backend
    storage.saveProfile(nickname, nik, ageFromDb); // MODIFIKASI: Simpan usia ke profil lokal
    setProfiles(storage.getProfiles());
    return true;
  } catch (err) {
    setError("Gagal validasi");
    return false;
  } finally {
    setLoading(false);
  }
};

  const selectProfile = (profile) => {
    storage.setActiveUser(profile);
    setActiveUser(profile);
  };

  const removeProfile = (nik) => {
    storage.deleteProfile(nik);
    setProfiles(storage.getProfiles());
    if (activeUser?.nik === nik) {
      setActiveUser(null);
    }
  };

  return {
    profiles,
    activeUser,
    loading,
    error,
    addProfile,
    selectProfile,
    removeProfile
  };
};