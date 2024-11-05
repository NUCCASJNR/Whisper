import { createContext, useState, useContext, FC, useEffect } from 'react';
import axios from 'axios';
import { ApiContextType, ApiProviderProps, User } from '../interfaces';
import { useNavigate } from 'react-router-dom';

const ApiContext = createContext<ApiContextType | undefined>(undefined);

const BaseURL = import.meta.env.VITE_API_URL;

export const ApiProvider: FC<ApiProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  // Effect to load user session from localStorage on app start
  useEffect(() => {
    (async () => {
      await profile();
    })();
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

        await profile();
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

      console.log(response);

      if (response.status === 201) {
        navigate('/login');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Signup failed.');
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    // Clear user data and tokens
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('access_token');
      const refresh_token = localStorage.getItem('refresh_token');
      if (!token) throw new Error('No access token found.');

      const response = await axios.post(
        `${BaseURL}/auth/logout`,
        { refresh_token },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      // [{id: ''
      // bio: ''}, {id: ''
      //   bio: ''} ]

      if (response.status === 200) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
        navigate('/login');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Logout failed.');
    } finally {
      setLoading(false);
    }
  };

  const profile = async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('No access token found.');

      const response = await axios.get(`${BaseURL}/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const userId = JSON.parse(atob(token.split('.')[1])).user_id;

      if (response.status === 200) {
        const userData = response.data;
        setUser({
          username: userData.username,
          bio: userData.bio,
          readyToChat: userData.ready_to_chat,
          id: userId,
        });
        console.log(user);
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to fetch profile.');
    }
  };

  const fetchActiveUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const access_token = localStorage.getItem('access_token');
      const refresh_token = localStorage.getItem('refresh_token');
      if (!access_token || !refresh_token)
        throw new Error('No access or refresh token found.');

      const response = await axios.get(`${BaseURL}/active-users`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      console.log(response.data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error fetching active users');
    } finally {
      setLoading(false);
    }
  };

  const fetchConversations = async () => {
    setLoading(true);
    setError(null);
    try {
      const access_token = localStorage.getItem('access_token');
      const refresh_token = localStorage.getItem('refresh_token');
      if (!access_token || !refresh_token)
        throw new Error('No access or refresh token found.');

      const response = await axios.get(`${BaseURL}/conversations`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      console.log(response.data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error fetching conversations');
    } finally {
      setLoading(false);
    }
  };

  const initiateConversation = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) throw new Error('No access token found.');

      const response = await axios.post(
        `${BaseURL}/whisper`,
        { id },
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        },
      );
      console.log(response.data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error fetching conversations');
    } finally {
      setLoading(false);
    }
  };

  const updateProfile = async (data: User) => {
    setLoading(true);
    setError(null);
    try {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) throw new Error('No access token found.');

      const response = await axios.post(`${BaseURL}/update-profile`, data, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      console.log(response.data);
      return response.data;
    } catch (err: any) {
      setError(err.response?.data?.message || 'Error updating profile');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ApiContext.Provider
      value={{
        user,
        login,
        signup,
        logout,
        profile,
        error,
        loading,
        fetchActiveUsers,
        fetchConversations,
        initiateConversation,
        updateProfile,
      }}
    >
      {children}
    </ApiContext.Provider>
  );
};

// Custom hook to use the ApiContext
export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error('useApi must be used within an ApiProvider');
  }
  return context;
};
