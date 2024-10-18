import { useState, FC } from 'react';
import { ChatBoxProps } from '../../interfaces';

const ChatBox: FC<ChatBoxProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState<string>('');

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage(''); // Clear input field
    }
  };

  return (
    <div className="flex items-center p-4 bg-gray-200">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="flex-grow p-2 rounded-l-md border-2 border-gray-400"
        placeholder="Type your message..."
      />
      <button
        onClick={handleSend}
        className="p-2 bg-accent text-white rounded-r-md"
      >
        Send
      </button>
    </div>
  );
};

export default ChatBox;
