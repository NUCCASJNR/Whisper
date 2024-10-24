import { createContext, useState, useContext, FC, useEffect } from 'react';
import axios from 'axios';
import { AuthContextType, AuthProviderProps, User } from '../interfaces';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const BaseURL = 'http://127.0.0.1:8000';
export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  // Effect to load user session from localStorage on app start
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      // Decode token to get user info (if needed)
      const userData = JSON.parse(atob(token.split('.')[1])); // Extract user data from token
      setUser({
        username: userData.username,
        readyToChat: true,
        isLoggedIn: true,
        bio: userData.bio,
        id: userData.user_id,
      });
    }
  }, []);

  const login = async (username: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${BaseURL}/auth/login`, {
        username,
        password,
      });

      if (response.status === 200) {
        const { access_token, refresh_token } = response.data;

        // Store tokens in localStorage
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        // Optionally decode the token to get user info
        const userData = JSON.parse(atob(access_token.split('.')[1]));

        setUser({
          username: userData.username, // Adjust according to your token structure
          bio: userData.bio, // Adjust according to your token structure
          id: userData.user_id, // Adjust according to your token structure
          readyToChat: true,
          isLoggedIn: true,
        });
        navigate('/chats');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed.');
    } finally {
      setLoading(false);
    }
  };

  const signup = async (username: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${BaseURL}/auth/signup`, {
        username,
        password,
      });

      if (response.status === 200) {
        navigate('/login');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Signup failed.');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // Clear user data and tokens
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  const profile = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('No access token found.');

      const response = await axios.get(`${BaseURL}/auth/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.status === 200) {
        const userData = response.data; // Assuming the response contains user data
        setUser({
          username: userData.username,
          readyToChat: true,
          isLoggedIn: true,
          id: userData.user_id,
          bio: userData.bio,
        });
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch profile.');
    }
  };

  const updateUserStatus = (updatedUser: User) => {
    setUser(updatedUser);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        signup,
        logout,
        updateUserStatus,
        profile,
        error,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
