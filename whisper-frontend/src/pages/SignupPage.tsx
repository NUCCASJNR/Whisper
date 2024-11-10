import { FC } from 'react';
import { useApi } from '../contexts';
// import { useNavigate } from 'react-router-dom';
import { AppHeader, SignUpForm } from '../components';

const SignupPage: FC = () => {
  const { signup } = useApi();
  // const navigate = useNavigate();

  const handleSubmit = async (username: string, password: string) => {
    await signup(username, password);

    // navigate('/login');
  };

  return (
    <div className="h-screen bg-background dark:bg-background-dark">
      <AppHeader />
      <div className="mt-12 md:mt-24 flex items-center justify-center">
        <SignUpForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
};

export default SignupPage;
