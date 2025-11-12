import { cn } from '../../lib/utils';

/**
 * ChatBubble - Individual message bubble component
 * 
 * This component renders a single message in the chat interface,
 * styled to look like a real SMS message bubble. The appearance
 * changes based on whether it's from the user or the contact.
 * 
 * @param {String} text - The message content
 * @param {String} sender - 'user' or 'contact' to determine styling
 * @param {String} timestamp - Optional timestamp for the message
 */
const ChatBubble = ({ text, sender = 'contact', timestamp }) => {
  const isUser = sender === 'user';
  
  return (
    <div className={cn(
      "flex w-full mb-3",
      isUser ? "justify-end" : "justify-start"
    )}>
      <div className={cn(
        "max-w-[75%] rounded-2xl px-4 py-2 shadow-sm",
        isUser 
          ? "bg-primary-600 text-white rounded-br-md" 
          : "bg-gray-700 text-gray-100 rounded-bl-md"
      )}>
        <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
          {text}
        </p>
        {timestamp && (
          <p className={cn(
            "text-xs mt-1",
            isUser ? "text-primary-200" : "text-gray-400"
          )}>
            {timestamp}
          </p>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;
