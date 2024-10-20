import { ReactNode } from 'react';

export interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => void;
  signup: (username: string, password: string) => void;
  logout: () => void;
  updateUserStatus: (updatedUser: User) => void;
}

export interface AuthProviderProps {
  children: ReactNode;
}

export interface LoginFormProps {
  onSubmit: (username: string, password: string) => void;
}
export interface SignupFormProps {
  onSubmit: (username: string, password: string) => void;
}

export interface User {
  username: string;
  publicKey: string;

  readyToChat: boolean;
  isLoggedIn: boolean;

  id: string;
}

export interface ModalProps {
  onClose: () => void;
  onSubmit: (newPassword: string) => void;
}
