import { FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useChat } from '../contexts';
import {NewChatModal} from '../components';
import { Chat } from '../interfaces';

const ChatListItem: FC<{ chat: Chat }> = ({ chat }) => {
  const navigate = useNavigate();
  const handleChatClick = (chatId: string) => {
    navigate(`/chats/${chatId}`); // Navigate to individual chat
  };
  return (
    <div
      key={chat.id}
      className="p-4 w-[45%] mb-2 bg-gray-200 rounded hover:bg-gray-300 cursor-pointer"
      onClick={() => handleChatClick(chat.id)}
    >
      {chat.name}
    </div>
  );
};

const ChatListPage: FC = () => {
  const { chats } = useChat();

  const [showModal, setShowModal] = useState(false);

  const openModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };

  return (
    <div className="flex flex-col h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Chats</h1>
      <div className="flex flex-wrap gap-4 w-full">
        {chats.map((chat) => (
          <ChatListItem key={chat.id} chat={chat} />
        ))}
      </div>

      {/* Floating Plus Button */}
      <button
        onClick={openModal}
        className="bg-blue-500 text-white p-4 rounded-full fixed bottom-4 right-4 shadow-lg hover:bg-blue-600"
      >
        +
      </button>

      {/* New Chat Modal */}
      {showModal && <NewChatModal closeModal={closeModal} />}
    </div>
  );
};

export default ChatListPage;
