import { FC } from 'react';
import Sidebar from './Sidebar';
import { LayoutProps } from '../interfaces';
import { useAuth } from '../contexts';

const Layout: FC<LayoutProps> = ({ children }) => {
  const { user } = useAuth();

  return (
    <>
      {user ? (
        <div className="flex h-screen overflow-y-visible bg-background">
          <div className="w-64">
            <Sidebar />
          </div>
          <div className="flex flex-col flex-grow">{children}</div>
        </div>
      ) : (
        <>{children}</>
      )}
    </>
  );
  // return (
  //   <div className="flex h-screen">
  //     <div className="w-1/4">
  //       <Sidebar />
  //     </div>
  //     <div className="flex flex-col ">{children}</div>
  //   </div>
  // );
};

export default Layout;
