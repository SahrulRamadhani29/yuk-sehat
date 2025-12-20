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

  const addProfile = async (nickname, nik) => {
    setLoading(true);
    setError(null);
    try {
      // 1. Simpan ke HP DULUAN agar user tidak merasa error
      storage.saveProfile(nickname, nik);
      
      // 2. Coba sinkronisasi dengan Backend Render secara "silent"
      // Jika server lambat, data sudah aman di HP user
      try {
        const response = await validateNik(nik);
        if (response && response.age) {
          // Update usia jika di database backend ternyata sudah ada data lama
          storage.saveProfile(nickname, nik, response.age); 
        }
      } catch (silentErr) {
        console.warn("Backend Render lambat, menggunakan data lokal.");
      }
      
      // 3. Update tampilan daftar profil
      setProfiles(storage.getProfiles());
      return true;
    } catch (err) {
      setError("Gagal menyimpan profil.");
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