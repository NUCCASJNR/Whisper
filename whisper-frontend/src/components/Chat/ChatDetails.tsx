import { FC, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useChat } from '../../contexts';
import { ChatBox, Message } from '..';
import { Chat } from '../../interfaces';

const ChatDetails: FC<{ chat: Chat }> = ({ chat }) => {
  const [messages, setMessages] = useState();
  if (!chat) {
    return <p>Chat not found.</p>;
  }

  const handleSendMessage = (message: string) => {
    setMessages([...messages, message]);
  };

  return (
    <div className="overflow-y-scroll h-full bg-accent bg-opacity-25 p-4">
      <div className="flex flex-col">
        {chat.messages.map((msg, index) => (
          <Message key={index} message={msg} />
        ))}
      </div>
      <ChatBox onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatDetails;
