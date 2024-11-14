import { FC, useState } from 'react';
import Sidebar from './Sidebar';
import { LayoutProps } from '../interfaces';
import { useApi } from '../contexts';
import { FaBars } from 'react-icons/fa'; // icon for mobile sidebar toggle
import { Logo } from '../components';

const Layout: FC<LayoutProps> = ({ children }) => {
  const { user } = useApi();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // manage sidebar open state

  return (
    <>
      {user ? (
        <div className="flex h-screen overflow-y-clip bg-background dark:bg-gray-100 relative">
          {/* Mobile Sidebar Toggle */}

          {/* Overlay */}
          {isSidebarOpen && (
            <div
              className="fixed inset-0 bg-black bg-opacity-50 z-10 md:hidden"
              onClick={() => setIsSidebarOpen(false)} // Collapse sidebar when overlay is clicked
            ></div>
          )}

          {/* Sidebar */}
          <div
            className={`fixed inset-0 z-20 w-64 transition-transform transform md:relative md:translate-x-0 ${
              isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
            }`}
          >
            <Sidebar />
          </div>

          {/* Main content */}
          <div className="flex flex-col flex-grow z-0">
            <div className="flex justify-between p-4 h-12 md:hidden">
              <button
                className=""
                onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              >
                <FaBars />
              </button>
              <div className="text-xl">
                <Logo />
              </div>
            </div>
            {children}
          </div>
        </div>
      ) : (
        <>{children}</>
      )}
    </>
  );
};

export default Layout;
