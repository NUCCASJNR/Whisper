import { FC, ReactNode } from 'react';

const ScrollBar: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="flex-1 overflow-y-auto p-4 scrollbar-hide">{children}</div>
  );
};

export default ScrollBar;
