import { FC, useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useApi } from '../contexts';
import { ChatDetails, ScrollBar } from '../components';
import { Header, DoubleLayout, MainLayout } from '../layouts';
import avatarImg from '../assets/images/logo192.png';
import {
  FiEdit,
  FiSearch,
  FiCamera,
  FiPhone,
  FiMoreHorizontal,
  FiArrowLeft,
} from 'react-icons/fi';
import { Chat } from '../interfaces';

// ChatListItem Component
const ChatListItem: FC<{ chat: Chat; onChatClick: () => void }> = ({
  chat,
  onChatClick,
}) => {
  const navigate = useNavigate();
  const handleChatClick = (chatId: string) => {
    navigate(`/chats/${chatId}`);
    onChatClick(); // Trigger mobile view change
  };

  return (
    <div
      key={chat.id}
      className="p-4 w-full mb-2 rounded hover:bg-gray-300 cursor-pointer flex items-center"
      onClick={() => handleChatClick(chat.id)}
    >
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

// ChatList Component
const ChatList: FC<{ chats: Chat[]; onChatClick: () => void }> = ({
  chats,
  onChatClick,
}) => {
  // const { chats } = useChat(); // Assuming useChat provides a list of chats

  return (
    <div className="flex flex-col h-full">
      <ScrollBar>
        {chats.length > 0 ? (
          <div className="flex flex-wrap gap-1 w-full">
            {chats.map((chat) => (
              <ChatListItem
                key={chat.id}
                chat={chat}
                onChatClick={onChatClick}
              />
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full ">
            <p className="text-gray-500 mb-4">No chats found.</p>
            <Link
              className="bg-primary text-white text-sm sm:text-base p-2 sm:p-3 rounded hover:bg-opacity-80 transition"
              to="/active_users"
            >
              Start Whispering
            </Link>
          </div>
        )}
      </ScrollBar>
    </div>
  );
};

// ChatHeader Component
const ChatHeader: FC = () => {
  return (
    <Header>
      <div className="flex justify-between w-full">
        <div>
          <h2 className="text-xl text-primary font-bold">Chats</h2>
        </div>
        <div className="text-md flex gap-2">
          <span className="rounded-full bg-background h-8 w-8 flex items-center justify-center text-gray-400 hover:text-gray-600">
            <FiEdit size={16} />
          </span>
          <span className="rounded-full bg-background h-8 w-8 flex items-center justify-center text-gray-400 hover:text-gray-600">
            <FiSearch size={16} />
          </span>
        </div>
      </div>
    </Header>
  );
};

// SecondChatHeader Component with Back button for mobile
const SecondChatHeader: FC<{ onBackToList: () => void }> = ({
  onBackToList,
}) => {
  return (
    <Header>
      <div className="flex justify-between w-full">
        <div className="flex items-center space-x-4">
          {/* Back button for mobile */}
          <button
            onClick={onBackToList}
            className="sm:hidden text-gray-500 hover:text-gray-700"
          >
            <FiArrowLeft size={20} />
          </button>
          <img
            src={avatarImg}
            alt="Avatar"
            className="rounded-full h-10 w-10"
          />
          <div className="flex flex-col">
            <span className="font-bold text-lg">John Doe</span>
            <span className="text-sm text-accent">Last message</span>
          </div>
        </div>
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

// ChatListPage Component with mobile responsiveness
const ChatListPage: FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const [showSecondChild, setShowSecondChild] = useState(!!chatId);
  // const { getChatById } = useChat(??);
  const { fetchConversations } = useApi();
  const [chats, setChats] = useState<Chat[]>([]);

  useEffect(() => {
    (async () => {
      const data = await fetchConversations();
      setChats(data.conversations);
    })();
  }, []);

  const handleBackToList = () => {
    setShowSecondChild(false); // Show chat list on mobile
  };

  const handleChatClick = () => {
    setShowSecondChild(true); // Show chat details on mobile
  };

  if (chatId) {
    const chat = chats.find((chat) => chat.id === chatId);

    return (
      <MainLayout>
        <DoubleLayout
          firstChild={
            // <div
            //   className={`${
            //     showSecondChild ? 'hidden sm:flex' : 'flex'
            //   } h-full`}
            // >
            <ChatList chats={chats} onChatClick={handleChatClick} />
            // </div>
          }
          firstChildHeader={
            <div className={`${showSecondChild ? 'hidden sm:block' : 'block'}`}>
              <ChatHeader />
            </div>
          }
          secondChild={<ChatDetails chat={chat} />}
          secondChildHeader={
            <SecondChatHeader onBackToList={handleBackToList} />
          }
          showSecondChild={showSecondChild}
        />
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <DoubleLayout
        firstChild={
          // <div
          //   className={`${showSecondChild ? 'hidden sm:flex' : 'flex'} h-full`}
          // >
          <ChatList onChatClick={handleChatClick} chats={chats} />
          // </div>/
        }
        firstChildHeader={
          <div className={`${showSecondChild ? 'hidden sm:block' : 'block'}`}>
            <ChatHeader />
          </div>
        }
        secondChild={
          <div className="p-4">
            <h2 className="text-lg">No chat</h2>
          </div>
        }
        secondChildHeader={
          <Header>
            <h2 className="text-lg font-bold text-primary">No Chat</h2>
          </Header>
        }
        showSecondChild={showSecondChild}
      />
    </MainLayout>
  );
};

export default ChatListPage;
