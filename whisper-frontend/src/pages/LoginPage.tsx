import { FC } from 'react';
import { AppHeader, LoginForm } from '../components';
// import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts';

const LoginPage: FC = () => {
  const { login } = useAuth();
  // const navigate = useNavigate();

  const handleSubmit = async (username: string, password: string) => {
    await login(username, password);
    // navigate('/chats');
  };
  return (
    <div className="h-screen bg-background">
      <AppHeader />
      <div className="mt-12 md:mt-24 flex items-center justify-center">
        <LoginForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
};

export default LoginPage;
