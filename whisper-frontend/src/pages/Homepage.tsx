import { FC } from 'react';
import { Link } from 'react-router-dom';

const Homepage: FC = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 text-center">
      <h1 className="text-5xl font-bold mb-6">Welcome to Whisper</h1>
      <p className="text-lg mb-8">
        A secure platform for private conversations using public and private
        keys.
      </p>

      <div className="flex gap-4">
        <Link
          to="/signup"
          className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
        >
          Sign Up
        </Link>
        <Link
          to="/login"
          className="bg-gray-500 text-white py-2 px-4 rounded-md hover:bg-gray-600"
        >
          Log In
        </Link>
      </div>
    </div>
  );
};

export default Homepage;
