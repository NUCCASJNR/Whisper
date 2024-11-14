import { FC /*useState*/ } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';

import { MdChat } from 'react-icons/md'; // Importing chat icon
import { FaUser } from 'react-icons/fa'; // Importing user icon
import { MdPeople } from 'react-icons/md';
import { Logo } from '../components';
import { SidebarLinkPropType } from '../interfaces';
import Header from './Header';

import { useApi } from '../contexts';
import avatarImg from '../assets/avatar.png';

import DarkModeToggle from '../components/DarkModeToggle';

const SidebarLink: FC<SidebarLinkPropType> = ({ to, text, isActive, Icon }) => {
  return (
    <Link
      to={to}
      className={`p-2 rounded-xl transition-colors text-text dark:text-text-dark duration-200 ${
        isActive
          ? 'bg-primary dark:bg-primary-dark dark:text-white text-white'
          : 'hover:bg-secondary'
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
  // const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const { logout, user } = useApi();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // const toggleSidebar = () => {
  //   setIsOpen(!isOpen);
  // };

  return (
    <aside className="h-full w-64 border-transparent text-white flex flex-col border-r-2">
      {/* Header Section */}
      <Header>
        <Logo />
      </Header>

      {/* Sidebar Links Section (This will take the remaining height) */}
      <nav className="flex-grow flex flex-col justify-between bg-white dark:bg-background-dark dark:text-text-dark border-transparent">
        <div className="flex flex-col gap-4 px-5 py-8">
          <SidebarLink
            to="/chats"
            text="Chats"
            isActive={location.pathname.startsWith('/chats')}
            Icon={MdChat}
          />

          <SidebarLink
            to="/active_users"
            text="Active Users"
            isActive={location.pathname === '/active_users'}
            Icon={MdPeople}
          />
          <SidebarLink
            to="/profile"
            text="Profile"
            isActive={location.pathname === '/profile'}
            Icon={FaUser}
          />
        </div>
        <div>
          {/* <DarkModeToggle /> */}
          <div className="px-5 py-4 flex items-center gap-4">
            <img
              src={avatarImg} // Update this to the path for the user's avatar
              alt="User avatar"
              className="w-10 h-10 rounded-full"
            />
            <div className="flex flex-col">
              <span className="text-lg text-text dark:text-text-dark">
                {user?.username}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-text dark:text-text-dark hover:text-red-700"
              >
                Logout
              </button>
            </div>
            <DarkModeToggle />
          </div>
        </div>
        {/* Add any other content that should be at the bottom here */}
      </nav>
    </aside>
  );
};

export default Sidebar;
