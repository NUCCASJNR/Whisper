import { FC, createContext, useContext, useState, useEffect } from 'react';
import data from '../services/data.json';
import {
  Message,
  Chat,
  ChatContextType,
  ChatProviderProps,
} from '../interfaces/ChatInterfaces';

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: FC<ChatProviderProps> = ({ children }) => {
  const [chats, setChats] = useState<Chat[]>([]);

  useEffect(() => {
    setChats(data.chats);
  }, []);

  const addChat = (name: string, messages: Message[]): Chat => {
    const newChat = { id: String(chats.length + 1), messages, name };
    setChats((prevChats) => [...prevChats, newChat]);
    return newChat;
  };

  const getChatById = (id: string | undefined): Chat | undefined => {
    return chats.find((chat) => chat.id === id);
  };

  return (
    <ChatContext.Provider value={{ chats, addChat, getChatById }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
