import { useState, FC, FormEvent } from 'react';
import { LoginFormProps } from '../../interfaces';
import { useApi } from '../../contexts';

const LoginForm: FC<LoginFormProps> = ({ onSubmit }) => {
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
        className="flex flex-col gap-4 bg-white p-8 shadow-lg rounded-md"
      >
        <h1 className="text-xl font-bold text-primary">Login</h1>
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
          className="bg-primary text-white p-2 rounded hover:bg-opacity-80"
        >
          {loading ? 'Logging In' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
