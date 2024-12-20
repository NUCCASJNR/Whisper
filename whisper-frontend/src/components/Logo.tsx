import { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApi } from '../contexts';

const Logo: FC = () => {
  const { user } = useApi();
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
      className="font-bold cursor-pointer text-primary"
      onClick={handleWhisperClick}
    >
      Whisper
    </h1>
  );
};

export default Logo;
