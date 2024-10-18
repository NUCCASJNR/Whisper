import { FC } from 'react';
import { MessageProps } from '../../interfaces/ChatInterfaces';

const Message: FC<MessageProps> = ({ message }) => {
  return (
    <div
      className={`w-fit my-2 p-4 rounded-lg ${
        message.sender === 'user'
          ? 'bg-primary text-white self-end'
          : 'bg-secondary text-white self-start'
      }`}
    >
      {message.content}
    </div>
  );
};

export default Message;
