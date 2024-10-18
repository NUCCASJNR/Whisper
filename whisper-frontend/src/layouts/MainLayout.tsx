import { FC } from 'react';
import Header from './Header';
import { MainLayoutProps } from '../interfaces';

const MainLayout: FC<MainLayoutProps> = ({
  firstChild,
  firstChildHeader,
  secondChild,
  secondChildHeader,
}) => {
  return (
    <main className="h-full border-secondary border-r-2 flex overflow-hidden">
      <div className="w-[40%] bg-background border-secondary border-r-2">
        <div className="border-secondary border-b-2">{firstChildHeader}</div>
        {firstChild}
      </div>
      <div className="flex-grow  border-secondary border-r-2">
        <div className="border-secondary border-b-2">{secondChildHeader}</div>
        {secondChild}
      </div>
    </main>
  );
};

export default MainLayout;
