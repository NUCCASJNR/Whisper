/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#0147FF', // Dark Blue
        secondary: '#F8F8F8', // Purple
        accent: '#25CB6B', // Yellow
        background: '#F6F8FC', // Light Gray
        text: '#181616', // Dark Gray
      },
    },
  },
  plugins: [],
};
