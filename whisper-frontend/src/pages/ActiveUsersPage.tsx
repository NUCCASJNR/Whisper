import { FC, useState } from 'react';
// import { useNavigate, useParams } from 'react-router-dom';
import { useUsers, useChat, /*useAuth*/ } from '../contexts';
import { ActiveUser, Chat } from '../interfaces';
import { ChatDetails, ScrollBar } from '../components';
import { Header, DoubleLayout, MainLayout } from '../layouts';

const ActiveUserCard: FC<{
  user: ActiveUser;
  onChat: (userId: string) => void;
}> = ({ user, onChat }) => {
  return (
    <div className="p-4 w-full bg-gray-200 rounded-lg shadow-md flex flex-col items-center">
      <img
        src={user.avatar}
        alt={`${user.username}'s profile`}
        className="w-16 h-16 rounded-full mb-2"
      />
      <p className="text-base mb-2">{user.username}</p>
      <button
        className="bg-primary text-accent px-4 py-2 rounded"
        onClick={() => onChat(user.id)}
      >
        Whisper
      </button>
    </div>
  );
};

const ActiveUsersList: FC<{ onChat: (userId: string) => void }> = ({
  onChat,
}) => {
  const { users: activeUsers } = useUsers(); // Assuming useUsers provides a list of active users

  return (
    <div className="flex flex-col h-full">
      <ScrollBar>
        <div className="flex flex-wrap justify-around gap-4">
          {activeUsers.map((user) => (
            <div className="w-32">
              <ActiveUserCard key={user.id} user={user} onChat={onChat} />
            </div>
          ))}
        </div>
      </ScrollBar>
    </div>
  );
};

const ActiveUsersPage: FC = () => {
  // const { chatId } = useParams<{ chatId: string }>();
  const { addChat /*getChatById*/ } = useChat();
  // const { user } = useAuth();
  const [selectedChat, setSelectedChat] = useState<Chat | null>(null);

  const handleStartChat = () => {
    const chat = addChat('new chat', []); // Create a new chat with the selected user
    setSelectedChat(chat);
  };

  return (
    <MainLayout>
      <DoubleLayout
        firstChild={<ActiveUsersList onChat={handleStartChat} />}
        firstChildHeader={
          <Header>
            <h2 className="text-lg font-bold">Active Users</h2>
          </Header>
        }
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
            <h2 className="text-lg font-bold">
              {selectedChat ? 'Chat' : 'No Active Chat'}
            </h2>
          </Header>
        }
      />
    </MainLayout>
  );
};

export default ActiveUsersPage;
