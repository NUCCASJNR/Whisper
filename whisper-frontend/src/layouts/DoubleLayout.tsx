import { FC } from 'react';
import { DoubleLayoutProps } from '../interfaces';

const DoubleLayout: FC<DoubleLayoutProps> = ({
  firstChild,
  firstChildHeader,
  secondChild,
  secondChildHeader,
  showSecondChild,
}) => {
  return (
    <div className="flex max-h-screen w-full">
      {/* Use h-screen for full height */}
      <div
        className={`flex w-full flex-col h-full md:w-[40%] border-transparent md:border-r-2 ${
          showSecondChild ? 'hidden' : ''
        } md:block`}
      >
        {/* Header for first child */}
        <div className="">
          {/* Set a specific height for the header */}
          {firstChildHeader}
        </div>
        <div className="flex-grow p-4 bg-white h-[calc(100vh-7rem)] md:h-[calc(100vh-4rem)]">
          {/* Use flex-grow to fill remaining space */}
          {firstChild}
        </div>
      </div>
      <div
        className={`flex-grow flex flex-col h-full ${
          !showSecondChild ? 'hidden' : ''
        } md:block`}
      >
        {/* Header for second child */}
        <div className="">
          {/* Set a specific height for the header */}
          {secondChildHeader}
        </div>
        <div className="flex-grow h-[calc(100vh-7rem)] md:h-[calc(100vh-4rem)]">
          {secondChild}
        </div>
        {/* Use flex-grow to fill remaining space */}
      </div>
    </div>
  );
};

export default DoubleLayout;
