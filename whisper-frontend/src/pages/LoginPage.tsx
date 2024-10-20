import { FC } from 'react';
import { AppHeader, LoginForm } from '../components';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts';

const LoginPage: FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (username: string, password: string) => {
    login(username, password);
    navigate('/chats');
  };
  return (
    <div>
      <AppHeader />
      <LoginForm onSubmit={handleSubmit} />;
    </div>
  );
};

export default LoginPage;
