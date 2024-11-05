import { ReactNode } from 'react';

export interface ApiContextType {
  user: User | null;
  login: (username: string, password: string) => void;
  signup: (username: string, password: string) => void;
  logout: () => void;
  profile: () => void;
  error: string | null;
  loading: boolean;
  fetchActiveUsers: () => Promise<any>;
  fetchConversations: () => Promise<any>;
  initiateConversation: (id: string) => Promise<any>;
  updateProfile: (data: any) => void;
}

export interface ApiProviderProps {
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

  readyToChat: boolean;
  bio: string;

  id: string;
}

export interface ModalProps {
  onClose: () => void;
  onSubmit: (newPassword: string) => void;
}
