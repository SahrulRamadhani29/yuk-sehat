// src/utils/formatter.js

/**
 * Memformat tanggal dari database menjadi format Indonesia
 * Contoh: 2025-12-20T... -> 20 Des 2025
 */
export const formatDate = (dateString) => {
  if (!dateString) return "";
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(date);
};

/**
 * Memformat durasi jam menjadi teks yang mudah dibaca
 * Contoh: 48 -> 2 Hari
 */
export const formatDuration = (hours) => {
  if (!hours || hours <= 0) return "Baru saja";
  if (hours < 24) return `${hours} Jam`;
  const days = Math.floor(hours / 24);
  return `${days} Hari`;
};