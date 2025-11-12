import { AlertTriangle, Trash2, Mail, Clock, User } from 'lucide-react';
import { Button } from '../Button';
import { Card } from '../Card';

/**
 * EmailDetailPane - Displays the full content of a selected email
 * 
 * This component renders the complete email with sender info, subject,
 * timestamp, and full HTML content. It includes action buttons for
 * reporting phishing and deleting emails.
 * 
 * SECURITY NOTE: This component uses dangerouslySetInnerHTML to render
 * email content with HTML formatting. This is ONLY safe in our controlled
 * simulation environment where:
 * 1. All content comes from our trusted backend API
 * 2. Content is AI-generated, not user-submitted
 * 3. There is no risk of XSS attacks in this training context
 * 
 * In a production email client, you would need proper HTML sanitization!
 * 
 * @param {Object} email - The selected email object to display
 * @param {Function} onReportPhishing - Callback when "Report Phishing" is clicked
 * @param {Function} onDelete - Callback when "Delete" is clicked
 */
const EmailDetailPane = ({ email, onReportPhishing, onDelete }) => {
  
  // Empty State - No email selected
  if (!email) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-8">
        <div className="w-24 h-24 bg-gray-800/30 rounded-full flex items-center justify-center mb-4">
          <Mail className="w-12 h-12 text-gray-600" />
        </div>
        <h3 className="text-xl font-semibold text-gray-400 mb-2">No Email Selected</h3>
        <p className="text-sm text-gray-500 text-center max-w-sm">
          Select an email from the inbox to read its contents and analyze for phishing indicators
        </p>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Email Header */}
      <div className="flex-shrink-0 border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm p-6">
        <div className="max-w-4xl mx-auto">
          {/* Subject */}
          <h2 className="text-2xl font-bold text-white mb-4">
            {email.subject}
          </h2>

          {/* Metadata Row */}
          <div className="flex items-start justify-between gap-4 mb-4">
            {/* Sender Info */}
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-full flex items-center justify-center flex-shrink-0">
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="text-sm font-medium text-white">{email.sender}</p>
                <div className="flex items-center gap-2 mt-1">
                  <Clock className="w-3 h-3 text-gray-500" />
                  <p className="text-xs text-gray-500">{email.timestamp}</p>
                </div>
              </div>
            </div>

            {/* Difficulty Badge */}
            <div className={`
              px-3 py-1 rounded-lg font-medium text-sm
              ${email.difficulty === 'easy' && 'bg-green-500/10 text-green-400 border border-green-500/20'}
              ${email.difficulty === 'medium' && 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20'}
              ${email.difficulty === 'hard' && 'bg-red-500/10 text-red-400 border border-red-500/20'}
            `}>
              {email.difficulty.charAt(0).toUpperCase() + email.difficulty.slice(1)} Difficulty
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            <Button 
              variant="danger" 
              size="sm"
              onClick={onReportPhishing}
              className="flex items-center gap-2"
            >
              <AlertTriangle className="w-4 h-4" />
              Report Phishing
            </Button>
            <Button 
              variant="outline" 
              size="sm"
              onClick={onDelete}
              className="flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Delete
            </Button>
          </div>
        </div>
      </div>

      {/* Email Body */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          <Card className="border-gray-800">
            <div className="p-6">
              {/* 
                CRITICAL SECURITY NOTE:
                ========================
                We use dangerouslySetInnerHTML here to render HTML-formatted email content.
                
                WHY THIS IS SAFE IN OUR CONTEXT:
                - All content comes from our controlled backend API
                - Content is AI-generated based on predefined scenarios
                - No user-submitted content is rendered
                - This is a training simulation, not a real email client
                - No external scripts or resources are included
                
                IN A REAL PRODUCTION EMAIL CLIENT:
                - You MUST sanitize HTML using libraries like DOMPurify
                - Strip dangerous tags (script, iframe, object, embed)
                - Remove event handlers (onclick, onerror, etc.)
                - Validate and sanitize URLs
                - Use Content Security Policy (CSP) headers
                - Implement sandboxing for email content
                
                This controlled environment mimics real phishing emails
                while maintaining security in our simulation.
              */}
              <div 
                className="email-content text-gray-300 leading-relaxed"
                dangerouslySetInnerHTML={{ __html: email.content }}
              />
            </div>
          </Card>

          {/* Analysis Hint Card */}
          <Card className="mt-6 border-primary-500/20 bg-primary-500/5">
            <div className="p-6">
              <div className="flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 text-primary-400 mt-0.5 flex-shrink-0" />
                <div>
                  <h3 className="text-sm font-semibold text-primary-400 mb-2">
                    Phishing Indicators to Look For:
                  </h3>
                  <ul className="text-xs text-gray-400 space-y-1 list-disc list-inside">
                    <li>Urgent or threatening language</li>
                    <li>Requests for personal or financial information</li>
                    <li>Suspicious sender email addresses</li>
                    <li>Poor grammar or spelling errors</li>
                    <li>Suspicious links (hover to preview URL)</li>
                    <li>Generic greetings like "Dear Customer"</li>
                    <li>Unexpected attachments</li>
                  </ul>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default EmailDetailPane;
