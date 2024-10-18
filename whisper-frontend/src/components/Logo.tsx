import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Logo: FC = () => {
  const { userKeys } = useAuth();
  const navigate = useNavigate();

  const handleWhisperClick = () => {
    if (userKeys) {
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
