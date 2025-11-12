import { Smile, Paperclip, Mic } from 'lucide-react';

/**
 * MessageInput - SMS message input interface
 * 
 * This component mimics the message composition bar found in
 * modern messaging apps. Currently serves as a visual placeholder
 * for the SMS simulation interface.
 * 
 * In future versions, this could be made functional to allow
 * users to respond to messages as part of the training.
 */
const MessageInput = () => {
  return (
    <div className="border-t border-gray-700 bg-gray-800/90 backdrop-blur-sm px-4 py-3">
      <div className="flex items-center gap-3">
        {/* Attachment Button */}
        <button 
          className="text-gray-400 hover:text-gray-300 transition-colors p-1"
          disabled
        >
          <Paperclip className="w-5 h-5" />
        </button>
        
        {/* Message Input Field */}
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder="Message (input disabled for training)"
            disabled
            className="w-full bg-gray-700/50 text-gray-400 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 border border-gray-600 cursor-not-allowed"
          />
          
          {/* Emoji Button */}
          <button 
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-300 transition-colors"
            disabled
          >
            <Smile className="w-5 h-5" />
          </button>
        </div>
        
        {/* Voice Message Button */}
        <button 
          className="text-gray-400 hover:text-gray-300 transition-colors p-1"
          disabled
        >
          <Mic className="w-5 h-5" />
        </button>
      </div>
      
      {/* Info Text */}
      <p className="text-xs text-gray-500 mt-2 text-center">
        Read-only mode: Focus on identifying suspicious messages
      </p>
    </div>
  );
};

export default MessageInput;
