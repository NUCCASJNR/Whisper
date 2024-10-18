import { FC, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useChat } from '../contexts/';
import { ChatBox, Message } from '../components';

const ChatPage: FC = () => {
  const { chatId } = useParams<{ chatId: string }>();
  const { getChatById } = useChat();
  const [messages, setMessages] = useState<string[]>([]);

  const chat = getChatById(chatId);

  if (!chat) {
    return <p>Chat not found.</p>;
  }

  const handleSendMessage = (message: string) => {
    setMessages([...messages, message]);
  };

  return (
    <div className="flex flex-col h-full">
      {chat.messages.map((msg, index) => (
        <Message key={index} message={msg} />
      ))}
      <ChatBox onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatPage;
