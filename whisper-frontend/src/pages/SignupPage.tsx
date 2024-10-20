import { FC } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import SignUpForm from '../components/Auth/SignUpForm';

const SignupPage: FC = () => {
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = (username: string, password: string) => {
    signup(username, password);

    navigate('/login');
  };

  return <SignUpForm onSubmit={handleSubmit} />;
};

export default SignupPage;
