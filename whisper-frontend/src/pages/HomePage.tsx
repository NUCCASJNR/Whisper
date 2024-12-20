import { FC } from 'react';
import { Link } from 'react-router-dom';
import { AppHeader } from '../components';
import whisperImg from '../assets/images/whisperers.png';
import { Footer } from '../layouts';

const HomePage: FC = () => {
  return (
    <div className="min-h-screen bg-background text-text">
      <AppHeader />

      {/* Content */}
      <div className="flex flex-col md:flex-row p-8 items-center justify-center gap-4 md:gap-8">
        {/* Text Section */}
        <div className="md:w-1/2 space-y-6 flex flex-col items-center md:items-start">
          <div className="text-center md:text-left">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              The Ultimate Anonymous Platform
            </h1>
            <p className="text-lg md:text-xl leading-relaxed">
              From strangers to friends. Made for meeting new people.
            </p>
          </div>
          <div className="space-x-4">
            <Link to="/signup">
              <button className="bg-primary text-white py-2 px-6 rounded-md hover:bg-opacity-80 transition duration-300">
                Sign up
              </button>
            </Link>
            <Link to="/login">
              <button className="bg-transparent border border-primary text-text py-2 px-6 rounded-md hover:bg-primary hover:text-white hover:bg-opacity-80 transition duration-300">
                Login
              </button>
            </Link>
          </div>
        </div>

        {/* Image Section */}
        <div className="mt-8 md:mt-0 md:w-1/2 flex justify-center">
          <img
            src={whisperImg}
            alt="Whisperers"
            className="w-full h-auto rounded-lg "
          />
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default HomePage;
