// src/utils/storage.js

// Kunci unik untuk penyimpanan di browser
const PROFILES_KEY = 'yuksehat_profiles';      
const ACTIVE_USER_KEY = 'yuksehat_active_user'; 

/**
 * MENGAMBIL DAFTAR SEMUA PROFIL
 * Mengambil array [{ nickname, nik }, ...] dari localStorage
 */
export const getProfiles = () => {
  try {
    const data = localStorage.getItem(PROFILES_KEY);
    return data ? JSON.parse(data) : [];
  } catch (error) {
    console.error("Gagal mengambil daftar profil:", error);
    return [];
  }
};

/**
 * MENYIMPAN PROFIL BARU ATAU UPDATE NAMA
 * Menyimpan pasangan Nama Panggilan dan NIK di lokal browser
 */
export const saveProfile = (nickname, nik) => {
  try {
    const profiles = getProfiles();
    
    // Cek apakah NIK ini sudah pernah didaftarkan di HP ini?
    const existingIndex = profiles.findIndex((p) => p.nik === nik);
    
    if (existingIndex >= 0) {
      // Jika NIK sudah ada, kita update nama panggilannya saja
      profiles[existingIndex].nickname = nickname;
    } else {
      // Jika NIK baru, kita tambahkan ke daftar
      profiles.push({ nickname, nik });
    }

    localStorage.setItem(PROFILES_KEY, JSON.stringify(profiles));
    return true;
  } catch (error) {
    console.error("Gagal menyimpan profil ke storage:", error);
    return false;
  }
};

/**
 * MENETAPKAN USER YANG SEDANG AKTIF (LOGIN)
 * Digunakan saat user memilih salah satu profil di halaman awal
 */
export const setActiveUser = (profile) => {
  try {
    localStorage.setItem(ACTIVE_USER_KEY, JSON.stringify(profile));
  } catch (error) {
    console.error("Gagal menetapkan user aktif:", error);
  }
};

/**
 * MENGAMBIL DATA USER YANG SEDANG AKTIF
 * Digunakan oleh Header dan API Request untuk tahu NIK siapa yang dikirim
 */
export const getActiveUser = () => {
  try {
    const data = localStorage.getItem(ACTIVE_USER_KEY);
    return data ? JSON.parse(data) : null;
  } catch (error) {
    return null;
  }
};

/**
 * KELUAR / GANTI PROFIL
 * Menghapus sesi aktif agar user kembali ke halaman "Pilih Profil"
 */
export const removeActiveUser = () => {
  localStorage.removeItem(ACTIVE_USER_KEY);
};

/**
 * MENGHAPUS PROFIL DARI DAFTAR (DELETE)
 * Jika user ingin menghapus salah satu list profil di HP tersebut
 */
export const deleteProfile = (nik) => {
  try {
    const profiles = getProfiles();
    const updatedProfiles = profiles.filter((p) => p.nik !== nik);
    localStorage.setItem(PROFILES_KEY, JSON.stringify(updatedProfiles));
    
    // Jika profil yang dihapus adalah yang sedang aktif, logout sekalian
    const active = getActiveUser();
    if (active && active.nik === nik) {
      removeActiveUser();
    }
  } catch (error) {
    console.error("Gagal menghapus profil:", error);
  }
};