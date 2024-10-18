import { FC } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import { MainLayoutProps } from '../interfaces/LayoutInterfaces';
// import Footer from './Footer';

const MainLayout: FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="flex h-fit">
      <Sidebar />
      <div className="flex flex-col flex-grow">
        <Header />
        <main className="flex-grow p-4 bg-gray-100">{children}</main>
      </div>
      {/* <Footer /> */}
    </div>
  );
};

export default MainLayout;
