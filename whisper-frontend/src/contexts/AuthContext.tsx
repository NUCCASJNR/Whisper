import { createContext, useState, useContext, FC } from 'react';
import { AuthContextType, AuthProviderProps, User } from '../interfaces';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = (username: string, password: string) => {
    // setUserKeys({ publicKey, privateKey });
    console.log(username, password);
    setUser({
      username,
      publicKey: 'e9hoin2o308hfo3209hndo9e',
      readyToChat: true,
      isLoggedIn: true,
      id: '422',
    });
  };

  const signup = (username: string, password: string) => {
    //make call to api
    console.log(username, password);
  };

  const logout = () => {
    setUser(null);
  };

  const updateUserStatus = (updatedUser: User) => {
    setUser(updatedUser);
  };
  return (
    <AuthContext.Provider
      value={{ user, login, signup, logout, updateUserStatus }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
