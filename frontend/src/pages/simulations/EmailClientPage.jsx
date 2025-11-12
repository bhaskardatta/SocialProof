import { useState, useEffect } from 'react';
import { Shield, Inbox, AlertTriangle } from 'lucide-react';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { scenarioAPI } from '../../services/api';
import InboxPane from '../../components/simulations/InboxPane';
import EmailDetailPane from '../../components/simulations/EmailDetailPane';

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * EmailClientPage - Main component for the Email Phishing Simulation
 * 
 * This component manages the state and layout for the email client interface.
 * It fetches AI-generated phishing scenarios from the backend and presents them
 * in a realistic three-pane email client layout.
 */
const EmailClientPage = () => {
  // State Management
  const [scenarios, setScenarios] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Hardcoded player_id for now (will be dynamic in later parts)
  const playerId = 1;

  /**
   * Fetch all scenarios for the current player from the backend
   */
  useEffect(() => {
    const fetchScenarios = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await scenarioAPI.getPlayerScenarios(playerId);
        
        // Transform scenarios into email format
        const emails = response.data.map((scenario, index) => ({
          id: scenario.id,
          sender: extractSender(scenario.content),
          subject: extractSubject(scenario.content),
          snippet: extractSnippet(scenario.content),
          content: scenario.content,
          timestamp: new Date(scenario.created_at).toLocaleString(),
          isPhishing: scenario.scenario_type === 'phishing',
          difficulty: scenario.difficulty_level,
          isRead: false
        }));
        
        setScenarios(emails);
      } catch (err) {
        console.error('Error fetching scenarios:', err);
        setError('Failed to load emails. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchScenarios();
  }, [playerId]);

  /**
   * Extract sender from email content
   * Looks for common email patterns
   */
  const extractSender = (content) => {
    const fromMatch = content.match(/From:\s*(.+?)(?:\n|<br>)/i);
    if (fromMatch) return fromMatch[1].trim();
    
    const emailMatch = content.match(/[\w.-]+@[\w.-]+\.\w+/);
    if (emailMatch) return emailMatch[0];
    
    return 'Unknown Sender';
  };

  /**
   * Extract subject line from email content
   */
  const extractSubject = (content) => {
    const subjectMatch = content.match(/Subject:\s*(.+?)(?:\n|<br>)/i);
    if (subjectMatch) return subjectMatch[1].trim();
    
    // Fallback: use first line of content
    const firstLine = content.split('\n')[0].replace(/<[^>]*>/g, '').trim();
    return firstLine.substring(0, 50) + (firstLine.length > 50 ? '...' : '');
  };

  /**
   * Extract preview snippet from email body
   */
  const extractSnippet = (content) => {
    // Remove HTML tags and get plain text
    const plainText = content.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
    
    // Skip header lines (From:, Subject:, etc.)
    const lines = plainText.split('\n').filter(line => 
      !line.match(/^(From|To|Subject|Date):/i)
    );
    
    const bodyText = lines.join(' ').trim();
    return bodyText.substring(0, 100) + (bodyText.length > 100 ? '...' : '');
  };

  /**
   * Handle email selection
   */
  const handleSelectEmail = (email) => {
    setSelectedEmail(email);
    
    // Mark email as read
    setScenarios(prevScenarios =>
      prevScenarios.map(s =>
        s.id === email.id ? { ...s, isRead: true } : s
      )
    );
  };

  /**
   * Handle email action (Report Phishing or Delete)
   * This is the core interactive gameplay function
   */
  const handleEmailAction = async (scenarioId, action) => {
    try {
      // Call the resolve endpoint
      const response = await scenarioAPI.resolveScenario(scenarioId, action);
      const result = response.data;
      
      // Display toast notification based on result
      if (result.correct) {
        toast.success(
          <div>
            <div className="font-semibold">{result.message}</div>
            <div className="text-sm mt-1">
              Score: +{result.score_change} points | New Rating: {result.new_skill_rating.toFixed(1)}
            </div>
          </div>,
          { duration: 5000 }
        );
      } else {
        toast.error(
          <div>
            <div className="font-semibold">{result.message}</div>
            <div className="text-sm mt-1">
              Score: {result.score_change} points | New Rating: {result.new_skill_rating.toFixed(1)}
            </div>
          </div>,
          { duration: 5000 }
        );
      }
      
      // Remove the email from the list (it's been resolved)
      setScenarios(prevScenarios => 
        prevScenarios.filter(s => s.id !== scenarioId)
      );
      
      // Clear selected email if it was the resolved one
      if (selectedEmail?.id === scenarioId) {
        setSelectedEmail(null);
      }
      
    } catch (err) {
      console.error('Error resolving scenario:', err);
      toast.error('Failed to process action. Please try again.');
    }
  };

  /**
   * Handle phishing report action
   */
  const handleReportPhishing = () => {
    if (selectedEmail) {
      handleEmailAction(selectedEmail.id, 'reported_phish');
    }
  };

  /**
   * Handle delete action
   */
  const handleDelete = () => {
    if (selectedEmail) {
      handleEmailAction(selectedEmail.id, 'deleted_safe');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <motion.div 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.4 }}
        className="border-b border-gray-800 bg-gray-900/80 backdrop-blur-sm sticky top-0 z-10"
      >
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg shadow-lg shadow-primary-500/20">
                <Inbox className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Email Client</h1>
                <p className="text-sm text-gray-400">Phishing Simulation Training</p>
              </div>
            </div>
            
            {/* Status Badge */}
            <motion.div 
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600/10 border border-primary-500/20 rounded-lg"
            >
              <Shield className="w-4 h-4 text-primary-400" />
              <span className="text-sm font-medium text-primary-400">Training Mode</span>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="h-[calc(100vh-89px)] flex">
        {/* Sidebar */}
        <motion.div 
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="w-64 border-r border-gray-800 bg-gray-900/50 backdrop-blur-sm p-4"
        >
          <div className="space-y-2">
            <motion.button 
              whileHover={{ scale: 1.02, x: 4 }}
              whileTap={{ scale: 0.98 }}
              className="w-full flex items-center gap-3 px-4 py-3 bg-primary-600/20 border border-primary-500/30 text-primary-400 rounded-lg hover:bg-primary-600/30 transition-colors"
            >
              <Inbox className="w-5 h-5" />
              <span className="font-medium">Inbox</span>
              <span className="ml-auto text-xs bg-primary-600 text-white px-2 py-1 rounded-full">
                {scenarios.filter(s => !s.isRead).length}
              </span>
            </motion.button>
            
            <motion.button 
              whileHover={{ scale: 1.02, x: 4 }}
              whileTap={{ scale: 0.98 }}
              className="w-full flex items-center gap-3 px-4 py-3 text-gray-400 rounded-lg hover:bg-gray-800/50 transition-colors"
            >
              <AlertTriangle className="w-5 h-5" />
              <span className="font-medium">Reported</span>
              <span className="ml-auto text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded-full">
                0
              </span>
            </motion.button>
          </div>

          {/* Info Box */}
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-6 p-4 bg-gray-800/30 border border-gray-700/50 rounded-lg"
          >
            <div className="flex items-start gap-2">
              <Shield className="w-5 h-5 text-primary-400 mt-0.5 flex-shrink-0" />
              <div>
                <h3 className="text-sm font-semibold text-white mb-1">Training Tips</h3>
                <p className="text-xs text-gray-400 leading-relaxed">
                  Look for suspicious sender addresses, urgent language, and requests for personal information.
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>

        {/* Email List Pane */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="w-96 border-r border-gray-800 bg-gray-900/30 backdrop-blur-sm overflow-y-auto"
        >
          <InboxPane
            emails={scenarios}
            selectedEmail={selectedEmail}
            onSelectEmail={handleSelectEmail}
            loading={loading}
            error={error}
          />
        </motion.div>

        {/* Email Detail Pane */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="flex-1 bg-gray-900/20 backdrop-blur-sm overflow-y-auto"
        >
          <EmailDetailPane
            email={selectedEmail}
            onReportPhishing={handleReportPhishing}
            onDelete={handleDelete}
          />
        </motion.div>
      </div>
    </div>
  );
};

export default EmailClientPage;
