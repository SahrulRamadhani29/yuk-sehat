// src/hooks/useProfile.js
import { useState, useEffect } from 'react';
import * as storage from '../utils/storage';
import { validateNik } from '../services/authService';

export const useProfile = () => {
  const [profiles, setProfiles] = useState([]);
  const [activeUser, setActiveUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load data profil saat pertama kali aplikasi dibuka
  useEffect(() => {
    setProfiles(storage.getProfiles());
    setActiveUser(storage.getActiveUser());
  }, []);

  // Fungsi untuk menambah profil baru setelah validasi NIK ke backend
  const addProfile = async (nickname, nik) => {
    setLoading(true);
    setError(null);
    try {
      // 1. Cek validasi NIK ke API Backend
      await validateNik(nik); 
      
      // 2. Jika valid, simpan ke localStorage
      storage.saveProfile(nickname, nik);
      
      // 3. Update state lokal
      const updatedProfiles = storage.getProfiles();
      setProfiles(updatedProfiles);
      return true;
    } catch (err) {
      setError(err?.message || "NIK tidak valid atau server bermasalah");
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Fungsi untuk memilih profil (Login)
  const selectProfile = (profile) => {
    storage.setActiveUser(profile);
    setActiveUser(profile);
  };

  // Fungsi untuk hapus profil
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