import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts';

const Logo: FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleWhisperClick = () => {
    if (user) {
      navigate('/chats'); // If logged in, go to chat page
    } else {
      navigate('/'); // If not logged in, go to homepage
    }
  };

  return (
    <h1
      className="text-xl font-bold cursor-pointer"
      onClick={handleWhisperClick}
    >
      Whisper
    </h1>
  );
};

export default Logo;
