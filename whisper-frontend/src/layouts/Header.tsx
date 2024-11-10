import { FC, ReactNode } from 'react';

const Header: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <header className="h-16 p-4 border-background dark:border-background-dark border-b-2 bg-white dark:bg-gray-100 text-text dark:text-white text-xl flex items-center">
      {children}
    </header>
  );
};

export default Header;
