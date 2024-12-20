import { FC } from 'react';
import { SingleLayoutProps } from '../interfaces';
// import Header from './Header';

const SingleLayout: FC<SingleLayoutProps> = ({ children }) => {
  return <div className="bg-background text-text h-[625px]">{children}</div>;
};

export default SingleLayout;
