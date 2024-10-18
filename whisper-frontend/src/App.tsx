import { FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {
  ChatPage,
  ChatListPage,
  HomePage,
  ProfilePage,
  LoginPage,
  SignupPage,
  ActiveUsersPage,
  NotFoundPage,
} from './pages';
import { MainLayout } from './layouts';

import { AuthProvider, ChatProvider } from './contexts';

const App: FC = () => {
  return (
    <AuthProvider>
      <ChatProvider>
        <Router>
          <MainLayout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/chats" element={<ChatListPage />} />
              <Route path="/chats/:chatId" element={<ChatPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/signup" element={<SignupPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/active_users" element={<ActiveUsersPage />} />

              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </MainLayout>
        </Router>
      </ChatProvider>
    </AuthProvider>
  );
};

export default App;
