import { useState, FC, FormEvent } from 'react';
import { SignupFormProps } from '../../interfaces';

const SignUpForm: FC<SignupFormProps> = ({ onSubmit }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPrivateKey] = useState<string>('');

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(username, password);
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 bg-white p-8 shadow-lg rounded-md"
      >
        <h1 className="text-xl font-bold">Signup</h1>
        <input
          type="text"
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
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
          className="bg-primary text-white p-2 rounded hover:bg-accent"
        >
          Signup
        </button>
      </form>
    </div>
  );
};

export default SignUpForm;
