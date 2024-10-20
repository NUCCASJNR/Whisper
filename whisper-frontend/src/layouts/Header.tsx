import { FC, ReactNode } from 'react';

const Header: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <header className="h-16 p-4 border-secondary border-b-2 bg-white text-text text-xl flex items-center">
      {children}
    </header>
  );
};

export default Header;
