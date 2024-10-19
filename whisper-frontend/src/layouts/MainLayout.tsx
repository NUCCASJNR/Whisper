import { FC } from 'react';
import { MainLayoutProps } from '../interfaces';

const MainLayout: FC<MainLayoutProps> = ({ children }) => {
  return (
    <main className="h-full border-secondary border-r-2 flex">{children}</main>
  );
};

export default MainLayout;
