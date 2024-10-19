// UsersContext.tsx
import { createContext, FC, useContext, useState, useEffect } from 'react';
import {
  ActiveUser,
  UsersContextType,
  UsersProviderProps,
} from '../interfaces';
import data from '../services/data.json'; // Assuming dummy data is stored here

const UsersContext = createContext<UsersContextType | undefined>(undefined);

export const UsersProvider: FC<UsersProviderProps> = ({ children }) => {
  const [users, setUsers] = useState<ActiveUser[]>([]);

  // Load initial user data from a JSON file (or this could come from an API)
  useEffect(() => {
    setUsers(data.users); // `data.users` contains an array of users
  }, []);

  // Function to add a new user
  const addUser = (user: ActiveUser) => {
    setUsers((prevUsers) => [...prevUsers, user]);
  };

  // Function to find a user by their ID
  const getUserById = (id: string | undefined): ActiveUser | undefined => {
    return users.find((user) => user.id === id);
  };

  // Function to set the active state of a user
  const setUserActive = (id: string, isActive: boolean) => {
    setUsers((prevUsers) =>
      prevUsers.map((user) => (user.id === id ? { ...user, isActive } : user)),
    );
  };

  return (
    <UsersContext.Provider
      value={{ users, addUser, getUserById, setUserActive }}
    >
      {children}
    </UsersContext.Provider>
  );
};

// Custom hook to use the UsersContext
export const useUsers = () => {
  const context = useContext(UsersContext);
  if (!context) {
    throw new Error('useUsers must be used within a UsersProvider');
  }
  return context;
};
