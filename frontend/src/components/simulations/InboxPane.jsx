import { Mail, MailOpen, AlertCircle, Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

/**
 * InboxPane - Displays the list of emails in the inbox
 * 
 * This component renders a scrollable list of email items, showing
 * sender, subject, snippet, and visual indicators for read/unread status.
 * 
 * @param {Array} emails - Array of email objects to display
 * @param {Object} selectedEmail - Currently selected email object
 * @param {Function} onSelectEmail - Callback function when an email is clicked
 * @param {Boolean} loading - Loading state indicator
 * @param {String} error - Error message if any
 */
const InboxPane = ({ emails, selectedEmail, onSelectEmail, loading, error }) => {
  
  // Loading State
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8">
        <Loader2 className="w-8 h-8 text-primary-400 animate-spin mb-3" />
        <p className="text-gray-400 text-sm">Loading emails...</p>
      </div>
    );
  }

  // Error State
  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8">
        <AlertCircle className="w-12 h-12 text-red-400 mb-3" />
        <p className="text-red-400 text-sm text-center">{error}</p>
      </div>
    );
  }

  // Empty State
  if (emails.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8">
        <Mail className="w-12 h-12 text-gray-600 mb-3" />
        <p className="text-gray-400 text-sm text-center">Your inbox is empty</p>
        <p className="text-gray-500 text-xs mt-2">No scenarios found for this player</p>
      </div>
    );
  }

  return (
    <div className="divide-y divide-gray-800">
      {emails.map((email) => (
        <EmailItem
          key={email.id}
          email={email}
          isSelected={selectedEmail?.id === email.id}
          onClick={() => onSelectEmail(email)}
        />
      ))}
    </div>
  );
};

/**
 * EmailItem - Individual email list item component
 * 
 * Displays a single email in the inbox list with sender, subject,
 * snippet preview, and visual indicators.
 */
const EmailItem = ({ email, isSelected, onClick }) => {
  return (
    <div
      onClick={onClick}
      className={cn(
        "p-4 cursor-pointer transition-all hover:bg-gray-800/50",
        isSelected && "bg-gray-800/70 border-l-4 border-primary-500",
        !email.isRead && "bg-gray-800/20"
      )}
    >
      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className={cn(
          "mt-1 flex-shrink-0",
          email.isRead ? "text-gray-500" : "text-primary-400"
        )}>
          {email.isRead ? (
            <MailOpen className="w-5 h-5" />
          ) : (
            <Mail className="w-5 h-5" />
          )}
        </div>

        {/* Email Content */}
        <div className="flex-1 min-w-0">
          {/* Sender */}
          <div className="flex items-center justify-between gap-2 mb-1">
            <p className={cn(
              "text-sm truncate",
              email.isRead ? "text-gray-400 font-normal" : "text-white font-semibold"
            )}>
              {email.sender}
            </p>
            {!email.isRead && (
              <span className="flex-shrink-0 w-2 h-2 bg-primary-500 rounded-full"></span>
            )}
          </div>

          {/* Subject */}
          <h3 className={cn(
            "text-sm truncate mb-1",
            email.isRead ? "text-gray-300 font-normal" : "text-white font-medium"
          )}>
            {email.subject}
          </h3>

          {/* Snippet */}
          <p className="text-xs text-gray-500 line-clamp-2 mb-2">
            {email.snippet}
          </p>

          {/* Metadata */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-gray-600">
              {email.timestamp}
            </span>
            
            {/* Difficulty Badge */}
            <span className={cn(
              "text-xs px-2 py-0.5 rounded-full font-medium",
              email.difficulty === 'easy' && "bg-green-500/10 text-green-400",
              email.difficulty === 'medium' && "bg-yellow-500/10 text-yellow-400",
              email.difficulty === 'hard' && "bg-red-500/10 text-red-400"
            )}>
              {email.difficulty}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InboxPane;
