import { FC, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import { MdChat } from 'react-icons/md'; // Importing chat icon
import { FaUser } from 'react-icons/fa'; // Importing user icon
import { MdDashboard, MdClose } from 'react-icons/md';
import { Logo } from '../components';
import { SidebarLinkPropType } from '../interfaces';
import Header from './Header';

import { useAuth } from '../contexts';
import avatarImg from '../assets/images/logo192.png';

const SidebarLink: FC<SidebarLinkPropType> = ({ to, text, isActive, Icon }) => {
  return (
    <Link
      to={to}
      className={`p-2 rounded transition-colors duration-200 ${
        isActive ? 'bg-gray-700 text-white' : 'hover:bg-accent'
      }`}
      onClick={(e) => isActive && e.preventDefault()} // Prevent navigation if it's active
    >
      <div className="flex gap-4 items-center text-base">
        <Icon />
        {text}
      </div>
    </Link>
  );
};

const Sidebar: FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const { logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <aside className="h-full bg-secondary border-secondary text-white flex flex-col border-r-2">
      {/* Header Section */}
      <div className="border-secondary border-b-2">
        <Header>
          <Logo />
        </Header>
      </div>

      {/* Sidebar Links Section (This will take the remaining height) */}
      <nav className="flex-grow flex flex-col justify-between bg-background">
        <div className="flex flex-col gap-4 px-5 py-8">
          <SidebarLink
            to="/chats"
            text="Chats"
            isActive={location.pathname === '/chats'}
            Icon={MdChat}
          />
          <SidebarLink
            to="/profile"
            text="Profile"
            isActive={location.pathname === '/profile'}
            Icon={FaUser}
          />
        </div>

        {/* Add any other content that should be at the bottom here */}
        <div className="px-5 py-4 flex items-center gap-4">
          <img
            src={avatarImg} // Update this to the path for the user's avatar
            alt="User avatar"
            className="w-10 h-10 rounded-full"
          />
          <div className="flex flex-col">
            <span className="text-lg">{user?.username}</span>
            <button
              onClick={handleLogout}
              className="text-sm text-red-500 hover:text-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>
    </aside>
  );
};

export default Sidebar;
