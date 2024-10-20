import { FC, useEffect, useRef, useState } from 'react';
// import { useParams } from 'react-router-dom';
// import { useChat } from '../../contexts';
import { ChatBox, Message, ScrollBar } from '../../components';
import { Chat, Message as MessageType } from '../../interfaces';

const ChatDetails: FC<{ chat: Chat }> = ({ chat }) => {
  const [messages, setMessages] = useState<MessageType[]>([]);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // Scroll to bottom whenever a new message is added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!chat) {
    return <p>Chat not found.</p>;
  }

  const handleSendMessage = (msgText: string) => {
    const message = {
      content: msgText,
      sender: 'me',
      recipient: chat.name,
      is_read: false,
    };
    setMessages([...messages, message]);
  };

  return (
    <div className="h-full">
      <div className="flex flex-col h-[450px] p-2">
        {/* Message container with scroll */}
        <ScrollBar>
          <div className="flex flex-col gap-2">
            {chat.messages.map((msg, index) => (
              <Message key={index} message={msg} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        </ScrollBar>

        {/* ChatBox always at the bottom */}
      </div>
      <div className="flex items-center p-4 bg-white w-full">
        <ChatBox onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
};

export default ChatDetails;
