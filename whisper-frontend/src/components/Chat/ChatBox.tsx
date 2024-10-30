import { useState, FC } from 'react';
import { ChatBoxProps } from '../../interfaces';
import { FiImage, FiSmile, FiMapPin, FiSend } from 'react-icons/fi';

const ChatBox: FC<ChatBoxProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState<string>('');

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage(''); // Clear input field
    }
  };

  const iconButtons = [
    { icon: FiImage, action: () => console.log('Open gallery') }, // Gallery icon
    { icon: FiSmile, action: () => console.log('Open emoji picker') }, // Emoji icon
    { icon: FiMapPin, action: () => console.log('Share location') }, // Location icon
  ];

  return (
    <div className="bg-background rounded-xl py-1 px-2 flex justify-between w-full">
      {/* Input section */}
      <div className="text-gray-400 flex-grow">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="w-full flex-grow p-2 bg-transparent text-text border-transparent focus:outline-none"
          placeholder="Type your message..."
        />
      </div>

      {/* Icons section */}
      <div className="flex items-center space-x-2">
        {iconButtons.map(({ icon: Icon, action }, index) => (
          <button
            key={index}
            onClick={action}
            className="hidden md:block p-2 text-gray-400 hover:text-gray-600"
          >
            <Icon size={20} />
          </button>
        ))}

        {/* Send Icon */}
        <button
          onClick={handleSend}
          className="p-2 text-gray-400 hover:text-gray-600"
        >
          <FiSend size={20} />
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
