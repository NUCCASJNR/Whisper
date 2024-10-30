import { ReactNode } from 'react';

export interface Message {
  content: string;
  sender: string;
  // recipient: string;
  // is_read: boolean;
}

export interface Chat {
  id: string;
  name: string;
  messages: Message[];
}

export interface ChatContextType {
  chats: Chat[];
  addChat: (name: string, messages: Message[]) => Chat;
  getChatById: (id: string | undefined) => Chat | undefined;
}
export interface ChatProviderProps {
  children: ReactNode;
}

export interface ChatBoxProps {
  onSendMessage: (message: string) => void;
}

export interface MessageProps {
  key: string | number;
  message: Message;
}

export interface NewChatModalProps {
  closeModal: () => void;
}
