import { FC } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import { LayoutProps } from '../interfaces';
import { useAuth } from '../contexts';
import MainLayout from './MainLayout';

const Layout: FC<LayoutProps> = ({ children }) => {
  const { user } = useAuth();

  // return (
  //   <>
  //     {user ? (
  //       <div className="flex h-screen">
  //         <div className="w-1/4">
  //           <Sidebar />
  //         </div>
  //         <div className="flex flex-col overflow-hidden">{children}</div>
  //       </div>
  //     ) : (
  //       <>{children}</>
  //     )}
  //   </>
  // );
  return (
    <div className="flex h-screen">
      <div className="w-1/4">
        <Sidebar />
      </div>
      <div className="flex flex-col ">{children}</div>
    </div>
  );
};

export default Layout;
