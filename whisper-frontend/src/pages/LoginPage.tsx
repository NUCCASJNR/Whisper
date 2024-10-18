import { FC } from 'react';
import LoginForm from '../components/Auth/LoginForm';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LoginPage: FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (username: string, password: string) => {
    login(username, password);
    navigate('/chats');
  };
  return <LoginForm onSubmit={handleSubmit} />;
};

export default LoginPage;
