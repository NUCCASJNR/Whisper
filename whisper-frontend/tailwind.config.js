/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#e22661', // Dark Blue
        secondary: '#5732f3', // Purple
        accent: '#6e2246', // Yellow
        background: '#1f0437', // Light Gray
        text: '#d9d0c7', // Dark Gray
      },
    },
  },
  plugins: [],
};
