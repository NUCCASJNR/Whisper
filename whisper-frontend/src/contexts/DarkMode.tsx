import { useEffect, useState } from 'react';

function useDarkMode() {
  // Initialize dark mode state based on localStorage or default to false
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const storedPreference = localStorage.getItem('darkMode');
    return storedPreference ? JSON.parse(storedPreference) : false;
  });

  // Effect to apply the dark class to the html element based on isDarkMode
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('darkMode', JSON.stringify(true));
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('darkMode', JSON.stringify(false));
    }
  }, [isDarkMode]);

  // Toggle function to switch dark mode on or off
  const toggleDarkMode = () => setIsDarkMode((prev: any) => !prev);

  return [isDarkMode, toggleDarkMode];
}

export default useDarkMode;
