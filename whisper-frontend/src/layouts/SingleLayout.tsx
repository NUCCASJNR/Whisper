import { FC } from 'react';
import { SingleLayoutProps } from '../interfaces';
import Header from './Header';

const SingleLayout: FC<SingleLayoutProps> = ({ children }) => {
  return (
    <div className="bg-background text-text h-[625px]">
      <Header>
        <h1>Single Layout</h1>
      </Header>
      <div className="p-4">{children}</div>
    </div>
  );
};

export default SingleLayout;
