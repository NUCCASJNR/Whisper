import { FC, ReactNode } from 'react';

const ScrollBar: FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="h-full overflow-y-auto scrollbar-hide">{children}</div>
  );
};

export default ScrollBar;
