import { FC, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useChat } from '../contexts';
import { Chat } from '../interfaces';
import { ChatDetails } from '../components';
import { Header, MainLayout } from '../layouts';

const ChatListItem: FC<{ chat: Chat }> = ({ chat }) => {
  const navigate = useNavigate();
  const handleChatClick = (chatId: string) => {
    navigate(`/chats/${chatId}`); // Navigate to individual chat
  };
  return (
    <div
      key={chat.id}
      className="p-4 w-full mb-2 bg-gray-200 rounded hover:bg-gray-300 cursor-pointer"
      onClick={() => handleChatClick(chat.id)}
    >
      {chat.name}
    </div>
  );
};

const ChatList: FC = () => {
  const { chats } = useChat(); // Assuming useChat provides a list of chats

  return (
    <div className="flex flex-col h-screen p-4">
      <h1 className="text-2xl font-bold mb-4 text-text">Chats</h1>
      <div className="flex flex-wrap gap-4 w-full">
        {chats.map((chat) => (
          <ChatListItem key={chat.id} chat={chat} />
        ))}
      </div>
    </div>
  );
};

const ChatListPage: FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const { getChatById } = useChat();

  if (chatId) {
    const chat = getChatById(chatId);

    return (
      <MainLayout
        firstChild={<ChatList />}
        firstChildHeader={
          <Header>
            <h2 className="text-lg font-bold">Chat List</h2>
          </Header>
        }
        secondChild={<ChatDetails chat={chat} />} // This component should handle chat details
        secondChildHeader={
          <Header>
            <h2 className="text-lg font-bold">Chat Details</h2>
          </Header>
        }
      />
    );
  }
  return (
    <MainLayout
      firstChild={<ChatList />}
      firstChildHeader={
        <Header>
          <h2 className="text-lg font-bold">Chat List</h2>
        </Header>
      }
      secondChild={<div>No chat</div>} // This component should handle chat details
      secondChildHeader={
        <Header>
          <h2 className="text-lg font-bold">No Chat</h2>
        </Header>
      }
    />
  );
};

export default ChatListPage;
