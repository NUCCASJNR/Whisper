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
    <div className="flex max-h-screen">
      {' '}
      {/* Use h-screen for full height */}
      <div
        className={`flex flex-col h-full md:w-[40%] border-transparent border-r-2 ${
          showSecondChild ? 'hidden' : ''
        } md:block`}
      >
        {/* Header for first child */}
        <div className="h-16">
          {' '}
          {/* Set a specific height for the header */}
          {firstChildHeader}
        </div>
        <div className="flex-grow p-4 bg-white">
          {' '}
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
        <div className="h-16">
          {' '}
          {/* Set a specific height for the header */}
          {secondChildHeader}
        </div>
        <div className="flex-grow p-4">{secondChild}</div>{' '}
        {/* Use flex-grow to fill remaining space */}
      </div>
      {/* Back button for mobile */}
      {/* {showSecondChild && (
        <button
          className="fixed top-0 right-0 md:hidden p-2 mt-2 bg-blue-500 text-white"
          onClick={onBackToList}
        >
          Back
        </button>
      )} */}
    </div>
  );
};

export default DoubleLayout;
