import { FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import ChatListPage from './pages/ChatListPage';
import Homepage from './pages/Homepage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import ActiveUsersPage from './pages/ActiveUsersPage';
import MainLayout from './layouts/MainLayout';

import { AuthProvider } from './contexts/AuthContext';
import { ChatProvider } from './contexts/ChatContext';

const App: FC = () => {
  return (
    <AuthProvider>
      <ChatProvider>
        <Router>
          <MainLayout>
            <Routes>
              <Route path="/" element={<Homepage />} />
              <Route path="/chats" element={<ChatListPage />} />
              <Route path="/chats/:chatId" element={<ChatPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/active_users" element={<ActiveUsersPage />} />
            </Routes>
          </MainLayout>
        </Router>
      </ChatProvider>
    </AuthProvider>
  );
};

export default App;
