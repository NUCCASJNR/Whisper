import { FC } from 'react';
import Logo from './Logo';
import { Link } from 'react-router-dom';

const AppHeader: FC = () => {
  return (
    <div className="flex justify-between h-16 p-6 bg-white shadow-lg">
      <div className="text-2xl">
        <Logo />
      </div>
      <div className="flex justify-between gap-4 text-primary">
        <Link to="/login">Login</Link>
        <Link to="/signup">Sign Up</Link>
      </div>
    </div>
  );
};

export default AppHeader;
