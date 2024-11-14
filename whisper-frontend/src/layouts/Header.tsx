import { FC, ReactNode } from 'react';

const Header: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <header className="h-16 p-4 border-background dark:border-gray-100 border-b-2 bg-white dark:bg-background-dark text-text dark:text-text-dark text-xl flex items-center">
      {children}
    </header>
  );
};

export default Header;
