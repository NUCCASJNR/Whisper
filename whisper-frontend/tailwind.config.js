/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#1E3A8A', // Dark Blue
        secondary: '#9333EA', // Purple
        accent: '#FBBF24', // Yellow
        background: '#F3F4F6', // Light Gray
        text: '#111827', // Dark Gray
      },
    },
  },
  plugins: [],
};
