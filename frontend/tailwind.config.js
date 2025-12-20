/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Kita tambahkan sedikit custom warna sesuai logo Yuk Sehat
      colors: {
        health: {
          blue: '#2563eb',
          green: '#22c55e',
        }
      },
      animation: {
        'slide-up': 'slideUp 0.3s ease-out forwards',
      }
    },
  },
  plugins: [],
}