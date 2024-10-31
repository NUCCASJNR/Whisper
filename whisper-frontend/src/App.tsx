import { FC } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import {
  ChatListPage,
  HomePage,
  ProfilePage,
  LoginPage,
  SignupPage,
  ActiveUsersPage,
  NotFoundPage,
} from './pages';
import { Layout } from './layouts';

import { AuthProvider, ChatProvider, UsersProvider } from './contexts';

const App: FC = () => {
  return (
    <Router>
      <AuthProvider>
        <ChatProvider>
          <UsersProvider>
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                {/* <Route path="/chats" element={<ChatListPage />} /> */}
                <Route path="/chats" element={<ChatListPage />} />
                <Route path="/chats/:chatId" element={<ChatListPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/active_users" element={<ActiveUsersPage />} />

                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </Layout>
          </UsersProvider>
        </ChatProvider>
      </AuthProvider>
    </Router>
  );
};

export default App;
