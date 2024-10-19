import { FC /*useState*/ } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useChat } from '../contexts';
import { Chat } from '../interfaces';
import { ChatDetails, ScrollBar } from '../components';
import { Header, DoubleLayout, MainLayout } from '../layouts';
import avatarImg from '../assets/images/logo192.png';
import {
  FiEdit,
  FiSearch,
  FiCamera,
  FiPhone,
  FiMoreHorizontal,
} from 'react-icons/fi';

const ChatListItem: FC<{ chat: Chat }> = ({ chat }) => {
  const navigate = useNavigate();
  const handleChatClick = (chatId: string) => {
    navigate(`/chats/${chatId}`); // Navigate to individual chat
  };
  return (
    <div
      key={chat.id}
      className="p-4 w-full mb-2 rounded hover:bg-gray-300 cursor-pointer flex items-center"
      onClick={() => handleChatClick(chat.id)}
    >
      {/* Avatar and online status */}
      <div className="relative">
        <img
          src={avatarImg}
          alt={chat.name}
          className="w-10 h-10 rounded-full"
        />
        {true && (
          <span className="absolute bottom-0 right-0 block h-2 w-2 rounded-full bg-green-500 ring-2 ring-white"></span>
        )}
      </div>

      {/* Chat details */}
      <div className="flex justify-between ml-4 flex-1">
        <div className="flex flex-col justify-center items-start">
          <span className="font-bold">{chat.name}</span>
          <span className="text-sm text-gray-600 truncate">Hey buddy</span>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className="text-sm text-gray-500">8:00pm</span>
          {1 > 0 && (
            <span className="flex items-center justify-center text-xs w-4 h-4 text-white bg-red-600 font-semibold rounded-full">
              1
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

const ChatList: FC = () => {
  const { chats } = useChat(); // Assuming useChat provides a list of chats

  return (
    <div className="flex flex-col h-full">
      <ScrollBar>
        <div className="flex flex-wrap gap-1 w-full">
          {chats.map((chat) => (
            <ChatListItem key={chat.id} chat={chat} />
          ))}
        </div>
      </ScrollBar>
    </div>
  );
};

const ChatHeader: FC = () => {
  return (
    <Header>
      <div className="flex justify-between w-full">
        <div>
          <h2 className="text-xl text-primary font-bold">Chats</h2>
        </div>
        <div className="text-md flex gap-2">
          {/* Edit Icon */}
          <span className="rounded-full bg-background h-8 w-8 flex items-center justify-center text-gray-400 hover:text-gray-600">
            <FiEdit size={16} />
          </span>

          {/* Search Icon */}
          <span className="rounded-full bg-background h-8 w-8 flex items-center justify-center text-gray-400 hover:text-gray-600">
            <FiSearch size={16} />
          </span>
        </div>
      </div>
    </Header>
  );
};

const SecondChatHeader: FC = () => {
  return (
    <Header>
      <div className="flex justify-between w-full p-4">
        {/* Left Section: Avatar, Name, and Text */}
        <div className="flex items-center space-x-4">
          {/* Avatar */}
          <img
            src={avatarImg} // Replace with actual avatar source
            alt="Avatar"
            className="rounded-full h-10 w-10"
          />
          {/* Name and Text */}
          <div className="flex flex-col">
            <span className="font-bold text-lg">John Doe</span>
            <span className="text-sm text-accent">Last message</span>
          </div>
        </div>

        {/* Right Section: Icons */}
        <div className="flex items-center space-x-4">
          <button className="text-gray-500 hover:text-gray-700">
            <FiCamera size={20} />
          </button>
          <button className="text-gray-500 hover:text-gray-700">
            <FiPhone size={20} />
          </button>
          <button className="text-gray-500 hover:text-gray-700">
            <FiMoreHorizontal size={20} />
          </button>
        </div>
      </div>
    </Header>
  );
};

const ChatListPage: FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const { getChatById } = useChat();

  if (chatId) {
    const chat = getChatById(chatId);

    return (
      <MainLayout>
        <DoubleLayout
          firstChild={<ChatList />}
          firstChildHeader={<ChatHeader />}
          secondChild={chat ? <ChatDetails chat={chat} /> : null} // Conditional rendering to handle undefined chat
          secondChildHeader={<SecondChatHeader />}
        />
      </MainLayout>
    );
  }
  return (
    <MainLayout>
      <DoubleLayout
        firstChild={<ChatList />}
        firstChildHeader={<ChatHeader />}
        secondChild={<div>No chat</div>} // This component should handle chat details
        secondChildHeader={
          <Header>
            <h2 className="text-lg font-bold">No Chat</h2>
          </Header>
        }
      />
    </MainLayout>
  );
};

export default ChatListPage;
