import { FC } from 'react';
import { FaMoon, FaSun } from 'react-icons/fa';
import useDarkMode from '../contexts/DarkMode'; // Import the hook

const DarkModeToggle: FC = () => {
  const [isDarkMode, toggleDarkMode] = useDarkMode(); // Use the hook

  return (
    <div className="flex justify-center">
      <button
        onClick={toggleDarkMode}
        className="relative flex items-center justify-between w-16 h-8 p-1 rounded-full bg-secondary dark:bg-secondary-dark transition duration-300"
      >
        {/* Sun and Moon icons */}
        <FaMoon
          className={`absolute left-1 text-white transition-all duration-300 ${
            isDarkMode ? 'opacity-100' : 'opacity-0'
          }`}
        />
        <FaSun
          className={`absolute right-1 text-text transition-all duration-300 ${
            isDarkMode ? 'opacity-0' : 'opacity-100'
          }`}
        />
        <div
          className={`w-6 h-6 bg-text dark:bg-text-dark rounded-full transition-all duration-300 ${
            isDarkMode ? 'transform translate-x-8' : ''
          }`}
        />
      </button>
    </div>
  );
};

export default DarkModeToggle;
