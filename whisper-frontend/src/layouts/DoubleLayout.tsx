import { FC } from 'react';
import { DoubleLayoutProps } from '../interfaces';

const DoubleLayout: FC<DoubleLayoutProps> = ({
  firstChild,
  firstChildHeader,
  secondChild,
  secondChildHeader,
}) => {
  return (
    <>
      <div className="w-[40%] border-transparent border-r-2">
        {firstChildHeader}
        <div className="p-4 h-[525px] bg-white">{firstChild}</div>
      </div>
      <div className="flex-grow">
        {secondChildHeader}
        <div className="h-[525px]">{secondChild}</div>
      </div>
    </>
  );
};

export default DoubleLayout;
