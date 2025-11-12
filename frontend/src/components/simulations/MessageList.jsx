import { useRef, useEffect } from 'react';
import ChatBubble from './ChatBubble';

/**
 * MessageList - Displays the conversation thread
 * 
 * This component renders a scrollable list of chat messages,
 * automatically scrolling to the latest message. It creates
 * a realistic messaging interface by displaying messages in
 * chronological order.
 * 
 * @param {Array} messages - Array of message objects with text, sender, and timestamp
 */
const MessageList = ({ messages }) => {
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  if (!messages || messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-gray-500 text-sm">No messages yet</p>
      </div>
    );
  }
  
  return (
    <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
      {messages.map((message, index) => (
        <ChatBubble
          key={index}
          text={message.text}
          sender={message.sender}
          timestamp={message.timestamp}
        />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
