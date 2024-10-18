import { FC } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';
import { HeaderLinkPropType } from '../interfaces/LayoutInterfaces';

const HeaderLink: FC<HeaderLinkPropType> = ({ to, text }) => {
  return (
    <Link to={to} className="hover:bg-gray-700 p-2 rounded">
      {text}
    </Link>
  );
};

const Header: FC = () => {
  return (
    <header className="bg-primary text-white p-4">
      <div className="flex justify-between items-center">
        <div className="md:opacity-0">
          <Logo />
        </div>
        <nav className="flex gap-4">
          <HeaderLink to="/login" text="Login" />
          <HeaderLink to="/signup" text="Signup" />
        </nav>
      </div>
    </header>
  );
};

export default Header;
