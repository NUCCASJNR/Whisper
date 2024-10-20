import { FC } from 'react';
import { useAuth } from '../contexts';
import { useNavigate } from 'react-router-dom';
import { AppHeader, SignUpForm } from '../components';

const SignupPage: FC = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (username: string, password: string) => {
    signup(username, password);

    navigate('/login');
  };

  return (
    <div>
      <AppHeader />
      <SignUpForm onSubmit={handleSubmit} />;
    </div>
  );
};

export default SignupPage;
