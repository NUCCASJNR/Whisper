import { useState, FC, FormEvent } from 'react';
import { useChat } from '../../contexts/ChatContext';
import { useNavigate } from 'react-router-dom';
import { NewChatModalProps } from '../../interfaces/ChatInterfaces';

const NewChatModal: FC<NewChatModalProps> = ({ closeModal }) => {
  const [chatName, setChatName] = useState('');
  const [message, setMessage] = useState('');
  const { addChat } = useChat();
  const navigate = useNavigate();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (chatName.trim() === '' || message.trim() === '') return;

    // Add new chat
    const newChat = addChat(chatName, [message]);

    // Close the modal
    closeModal();

    // Navigate to the new chat page
    navigate(`/chat/${newChat.id}`);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded shadow-lg">
        <h2 className="text-xl font-bold mb-4">New Chat</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Chat Name"
            value={chatName}
            onChange={(e) => setChatName(e.target.value)}
            className="p-2 border rounded"
          />
          <textarea
            placeholder="Message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="p-2 border rounded"
          />
          <div className="flex justify-end gap-4">
            <button
              type="button"
              onClick={closeModal}
              className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
            >
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewChatModal;
