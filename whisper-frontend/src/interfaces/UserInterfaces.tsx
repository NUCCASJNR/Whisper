// interfaces.ts
export interface ActiveUser {
  id: string;
  username: string;
  avatar: string; // URL or path to the user's avatar image
}

export interface UsersContextType {
  users: ActiveUser[];
  addUser: (user: ActiveUser) => void;
  getUserById: (id: string | undefined) => ActiveUser | undefined;
  setUserActive: (id: string, isActive: boolean) => void;
}

export interface UsersProviderProps {
  children: React.ReactNode;
}
