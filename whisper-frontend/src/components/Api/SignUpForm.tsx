import { useState, FC, FormEvent } from 'react';
import { SignupFormProps } from '../../interfaces';
import { useApi } from '../../contexts';

const SignUpForm: FC<SignupFormProps> = ({ onSubmit }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPrivateKey] = useState<string>('');
  const { loading } = useApi();

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(username, password);
  };

  return (
    <div className="flex justify-center items-center">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 bg-white dark:bg-gray-100 p-8 shadow-lg rounded-md"
      >
        <h1 className="text-xl font-bold text-primary dark:text-primary-dark">
          Signup
        </h1>
        <input
          type="text"
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value.trim())}
          className="p-2 border rounded"
        />
        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPrivateKey(e.target.value)}
          className="p-2 border rounded"
        />
        <button
          type="submit"
          className="bg-primary dark:bg-primary-dark text-white p-2 rounded hover:bg-opacity-80"
        >
          {loading ? 'Signing up' : 'Signup'}
        </button>
      </form>
    </div>
  );
};

export default SignUpForm;
