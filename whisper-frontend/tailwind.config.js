/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#0147FF', // Dark Blue
        secondary: '#F8F8F8', // Purple
        accent: '#25CB6B', // Yellow
        background: '#F6F8FC', // Light Gray
        text: '#181616', // Dark Gray

        // Dark Mode Colors
        'primary-dark': '#7D5FFF', // Dark Purple
        'secondary-dark': '#8E8DA6', // Muted Gray-Purple
        'accent-dark': '#D88AFF', // Pink-Purple Accent
        'background-dark': '#1E1B2E', // Dark Background
        'text-dark': '#E0E0E0', // Light text on dark
      },
    },
  },
  plugins: [],
};
