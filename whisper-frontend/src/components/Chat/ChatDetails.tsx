import { FC, useEffect, useRef, useState } from 'react';
// import { useParams } from 'react-router-dom';
// import { useChat } from '../../contexts';
import { ChatBox, Message, ScrollBar } from '../../components';
import { Chat, Message as MessageType } from '../../interfaces';
import { useApi } from '../../contexts';

const ChatDetails: FC<{ chat: Chat | undefined }> = ({ chat }) => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [sender, setSender] = useState<string>('');
  const [recipient, setRecipient] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const { user } = useApi();

  // Scroll to bottom whenever a new message is added
  useEffect(() => {
    if (chat && user) {
      const [first, second] = chat.participants;
      setSender(user.username);
      setRecipient(user.username === first ? second : first);

      setMessages(chat.messages);
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chat]);

  if (!chat) {
    return <p>Chat not found.</p>;
  }

  const handleSendMessage = (msgText: string) => {
    const message: MessageType = {
      content: msgText,
      sender,
      recipient,
      id: 'someIdFromEndpoint', // Replace with actual ID logic
      // is_read: false,
    };
    setMessages([...messages, message]);
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex flex-col p-4 h-[calc(100%-4rem)]">
        {/* Message container with scroll */}
        <ScrollBar>
          <div className="flex flex-col gap-2">
            {messages.map((msg) => (
              <Message key={msg.id} message={msg} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        </ScrollBar>
      </div>
      {/* ChatBox always at the bottom */}
      <div className="flex items-center p-4 bg-white h-16 w-full">
        <ChatBox onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
};

export default ChatDetails;
