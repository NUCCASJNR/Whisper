import { FC, useState } from 'react';
import { useUsers, useChat } from '../contexts';
import { ActiveUser, Chat } from '../interfaces';
import { ChatDetails, ScrollBar } from '../components';
import { Header, DoubleLayout, MainLayout } from '../layouts';
import { FiMessageCircle, FiArrowLeft } from 'react-icons/fi';

// ActiveUserCard Component
const ActiveUserCard: FC<{
  user: ActiveUser;
  onChat: (userId: string) => void;
}> = ({ user, onChat }) => {
  return (
    <div className="w-[11rem] bg-white rounded-lg border-secondary border-2 flex flex-col items-center transition">
      {/* User Avatar */}
      <div
        className="w-full h-48 rounded-t-lg bg-cover bg-center"
        style={{ backgroundImage: `url(${user.avatar})` }}
      />
      {/* Name and Bio */}
      <div className="w-full px-2 mt-2">
        <p className="text-base font-semibold text-text mb-1">
          {user.username}
        </p>
        <button
          className="w-full border-2 mb-2 border-secondary font-semibold text-primary text-base px-4 py-2 rounded flex items-center justify-center hover:bg-secondary  transition"
          onClick={() => onChat(user.id)}
        >
          <FiMessageCircle className="mr-2" /> Whisper
        </button>
      </div>
    </div>
  );
};

// ActiveUsersList Component
const ActiveUsersList: FC<{ onChat: (userId: string) => void }> = ({
  onChat,
}) => {
  const { users: activeUsers } = useUsers(); // useUsers provides a list of active users

  return (
    <div className="flex flex-col h-full">
      <ScrollBar>
        <div className="flex flex-wrap gap-4">
          {activeUsers.map((user) => (
            <ActiveUserCard key={user.id} user={user} onChat={onChat} />
          ))}
        </div>
      </ScrollBar>
    </div>
  );
};

// ActiveUsersPage Component
const ActiveUsersPage: FC = () => {
  const { addChat } = useChat();
  const [selectedChat, setSelectedChat] = useState<Chat | null>(null);
  const [showSecondChild, setShowSecondChild] = useState(false); // track which child to show on mobile

  // Handle starting a new chat
  const handleStartChat = (userId: string) => {
    console.log(userId);
    const chat = addChat('New Chat', []); // Add new chat
    setSelectedChat(chat);
    setShowSecondChild(true); // Switch to second child on mobile
  };

  // Back to first child (list view) on mobile
  const handleBackToList = () => {
    setShowSecondChild(false);
  };

  return (
    <MainLayout>
      <DoubleLayout
        // First Child (User List)
        firstChild={<ActiveUsersList onChat={handleStartChat} />}
        firstChildHeader={
          <Header>
            <h2 className="text-xl text-primary font-bold">Active Users</h2>
          </Header>
        }
        // Second Child (Chat Details)
        secondChild={
          selectedChat ? (
            <ChatDetails chat={selectedChat} />
          ) : (
            <div className="p-4">
              <h2 className="text-lg">Select a user to start chatting</h2>
            </div>
          )
        }
        secondChildHeader={
          <Header>
            <button
              onClick={handleBackToList}
              className="sm:hidden text-gray-500 hover:text-gray-700"
            >
              <FiArrowLeft size={20} />
            </button>
            <h2 className="text-lg font-bold">
              {selectedChat ? 'Chat' : 'No Active Chat'}
            </h2>
          </Header>
        }
        // Mobile Responsiveness Logic
        showSecondChild={showSecondChild}
      />
    </MainLayout>
  );
};

export default ActiveUsersPage;
