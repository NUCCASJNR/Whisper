import { FC } from 'react';
import { SingleLayoutProps } from '../interfaces';
// import Header from './Header';

const SingleLayout: FC<SingleLayoutProps> = ({ children }) => {
  return (
    <div className="bg-background dark:bg-background-dark text-text h-[800px]">
      {children}
    </div>
  );
};

export default SingleLayout;
