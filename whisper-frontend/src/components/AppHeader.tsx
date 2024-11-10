import { FC } from 'react';
import Logo from './Logo';
import { Link } from 'react-router-dom';
import DarkModeToggle from './DarkModeToggle';

const AppHeader: FC = () => {
  return (
    <div className="flex justify-between items-center h-16 p-6 bg-white shadow-lg dark:bg-gray-500">
      <div className="text-2xl">
        <Logo />
      </div>
      <div className="flex justify-between items-center gap-4 text-primary dark:text-white">
        <Link to="/login">Login</Link>
        <Link to="/signup">Sign Up</Link>
        {/* Dark Mode Toggle */}
        <DarkModeToggle />
      </div>
    </div>
  );
};

export default AppHeader;
