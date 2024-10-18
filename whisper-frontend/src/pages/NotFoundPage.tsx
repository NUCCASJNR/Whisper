// src/pages/NotFoundPage.tsx

import { FC } from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage: FC = () => {
  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gray-100 text-center">
      <h1 className="text-4xl font-bold mb-4 text-gray-800">
        404 - Page Not Found
      </h1>
      <p className="mb-6 text-gray-600">
        Oops! The page you are looking for does not exist.
      </p>
      <Link to="/" className="text-blue-500 hover:underline">
        Go Back to Homepage
      </Link>
    </div>
  );
};

export default NotFoundPage;
