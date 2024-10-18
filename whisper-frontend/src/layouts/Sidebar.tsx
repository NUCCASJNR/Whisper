import { FC, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

import { MdChat } from 'react-icons/md'; // Importing chat icon
import { FaUser } from 'react-icons/fa'; // Importing user icon
import { MdDashboard, MdClose } from 'react-icons/md';
import Logo from '../components/Logo';
import { SidebarLinkPropType } from '../interfaces/LayoutInterfaces';

const SidebarLink: FC<SidebarLinkPropType> = ({ to, text, isActive, Icon }) => {
  return (
    <Link
      to={to}
      className={`p-2 rounded transition-colors duration-200 ${
        isActive ? 'bg-gray-700 text-white' : 'hover:bg-accent'
      }`}
      onClick={(e) => isActive && e.preventDefault()} // Prevent navigation if it's active
    >
      <div className="flex gap-1 text-xl">
        <Icon />
        {text}
      </div>
    </Link>
  );
};
const Sidebar: FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="bg-secondary text-white md:w-64 z-40">
      <div>
        <button
          className="p-4 text-white bg-accent md:hidden"
          onClick={toggleSidebar}
        >
          {isOpen ? <MdClose /> : <MdDashboard />}
        </button>
      </div>
      <aside
        className={`h-full transform transition-transform duration-300 ${
          isOpen ? 'block' : 'hidden'
        } md:block`}
      >
        <div className="hidden md:block p-6 bg-primary">
          <Logo />
        </div>

        <nav className="flex flex-col gap-4 mt-4">
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
        </nav>
      </aside>
    </div>
  );
};

export default Sidebar;
