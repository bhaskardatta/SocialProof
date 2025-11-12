import { useState, useEffect } from 'react';
import { MessageSquare, Shield, AlertTriangle, Phone, Video, Info, ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { scenarioAPI } from '../../services/api';
import MessageList from '../../components/simulations/MessageList';
import MessageInput from '../../components/simulations/MessageInput';
import { Button } from '../../components/Button';

/**
 * SmishingClientPage - Main component for SMS Phishing Simulation
 * 
 * This component creates a realistic mobile messaging interface for
 * training users to identify smishing (SMS phishing) attacks. It fetches
 * AI-generated SMS scenarios and presents them in an authentic chat UI.
 */
const SmishingClientPage = () => {
  const navigate = useNavigate();
  
  // State Management
  const [scenarios, setScenarios] = useState([]);
  const [currentScenario, setCurrentScenario] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Hardcoded player_id for now (will be dynamic in later parts)
  const playerId = 1;

  /**
   * Fetch SMS scenarios from the backend
   * Filters to only show SMS-related scenario types
   */
  useEffect(() => {
    const fetchScenarios = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await scenarioAPI.getPlayerScenarios(playerId);
        
        // Filter for SMS-related scenarios only
        const smsScenarios = response.data.filter(scenario => {
          const type = scenario.scenario_type.toLowerCase();
          return type.includes('sms') || 
                 type.includes('text') || 
                 type.includes('smish') ||
                 type.includes('message');
        });
        
        if (smsScenarios.length === 0) {
          setError('No SMS scenarios found. Generate some from the Dashboard first!');
          setLoading(false);
          return;
        }
        
        setScenarios(smsScenarios);
        
        // Load the first scenario
        if (smsScenarios.length > 0) {
          loadScenario(smsScenarios[0]);
        }
        
      } catch (err) {
        console.error('Error fetching SMS scenarios:', err);
        setError('Failed to load messages. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchScenarios();
  }, [playerId]);

  /**
   * Parse scenario content into chat messages
   * Converts the AI-generated content into a conversation format
   */
  const loadScenario = (scenario) => {
    setCurrentScenario(scenario);
    
    // Parse the content into messages
    const parsedMessages = parseScenarioContent(scenario.content);
    setMessages(parsedMessages);
  };

  /**
   * Parse scenario content into chat message format
   * Handles different content structures from the AI
   */
  const parseScenarioContent = (content) => {
    const msgs = [];
    
    // Try to parse structured content
    const lines = content.split('\n').filter(line => line.trim());
    
    lines.forEach(line => {
      // Look for sender indicators
      if (line.match(/^(From|Sender|Contact):/i)) {
        // Skip metadata lines
        return;
      }
      
      // Determine if it's from user or contact
      // Messages with keywords like "verify", "click", "urgent" are typically from attackers
      const isContactMessage = line.length > 20 || 
                               line.toLowerCase().includes('click') ||
                               line.toLowerCase().includes('verify') ||
                               line.toLowerCase().includes('urgent') ||
                               !line.match(/^(me|user):/i);
      
      const cleanText = line.replace(/^(me|user|contact):\s*/i, '').trim();
      
      if (cleanText) {
        msgs.push({
          text: cleanText,
          sender: isContactMessage ? 'contact' : 'user',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });
      }
    });
    
    // If no structured messages found, treat entire content as one message
    if (msgs.length === 0) {
      msgs.push({
        text: content.trim(),
        sender: 'contact',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    }
    
    return msgs;
  };

  /**
   * Handle message action (Report Smishing)
   */
  const handleReportSmishing = async () => {
    if (!currentScenario) return;
    
    try {
      const response = await scenarioAPI.resolveScenario(currentScenario.id, 'reported_phish');
      const result = response.data;
      
      // Display toast notification
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
      
      // Remove resolved scenario and load next one
      const remainingScenarios = scenarios.filter(s => s.id !== currentScenario.id);
      setScenarios(remainingScenarios);
      
      if (remainingScenarios.length > 0) {
        loadScenario(remainingScenarios[0]);
      } else {
        setCurrentScenario(null);
        setMessages([]);
        toast('All SMS scenarios completed!', { icon: '🎉' });
      }
      
    } catch (err) {
      console.error('Error resolving scenario:', err);
      toast.error('Failed to process action. Please try again.');
    }
  };

  /**
   * Handle delete/ignore action
   */
  const handleDelete = async () => {
    if (!currentScenario) return;
    
    try {
      const response = await scenarioAPI.resolveScenario(currentScenario.id, 'deleted_safe');
      const result = response.data;
      
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
      
      // Load next scenario
      const remainingScenarios = scenarios.filter(s => s.id !== currentScenario.id);
      setScenarios(remainingScenarios);
      
      if (remainingScenarios.length > 0) {
        loadScenario(remainingScenarios[0]);
      } else {
        setCurrentScenario(null);
        setMessages([]);
      }
      
    } catch (err) {
      console.error('Error resolving scenario:', err);
      toast.error('Failed to process action. Please try again.');
    }
  };

  // Loading State
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-center">
          <MessageSquare className="w-12 h-12 text-primary-400 animate-pulse mx-auto mb-3" />
          <p className="text-gray-400">Loading messages...</p>
        </div>
      </div>
    );
  }

  // Error State
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="text-center max-w-md px-4">
          <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-3" />
          <p className="text-red-400 mb-4">{error}</p>
          <Button onClick={() => navigate('/dashboard')}>
            Go to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
      {/* Mobile Phone Frame */}
      <div className="w-full max-w-md h-[700px] bg-gray-900 rounded-[3rem] border-8 border-gray-800 shadow-2xl overflow-hidden relative">
        {/* Phone Notch */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-6 bg-gray-900 rounded-b-2xl z-20"></div>
        
        {/* Status Bar */}
        <div className="bg-gray-900 px-6 pt-2 pb-1 flex items-center justify-between text-xs text-gray-400">
          <span>9:41</span>
          <div className="flex items-center gap-1">
            <div className="w-4 h-3 border border-gray-400 rounded-sm relative">
              <div className="absolute inset-0.5 bg-gray-400"></div>
            </div>
          </div>
        </div>
        
        {/* Chat Header */}
        <div className="bg-gray-800 border-b border-gray-700 px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button 
                onClick={() => navigate('/')}
                className="text-primary-400 hover:text-primary-300 transition-colors"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
              
              <div className="flex items-center gap-3">
                {/* Contact Avatar */}
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center">
                  <MessageSquare className="w-5 h-5 text-gray-300" />
                </div>
                
                <div>
                  <h2 className="text-white font-semibold text-sm">Unknown Number</h2>
                  <p className="text-xs text-gray-400">+1 (555) 0123</p>
                </div>
              </div>
            </div>
            
            {/* Header Actions */}
            <div className="flex items-center gap-3">
              <button className="text-gray-400 hover:text-gray-300 transition-colors">
                <Video className="w-5 h-5" />
              </button>
              <button className="text-gray-400 hover:text-gray-300 transition-colors">
                <Phone className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
        
        {/* Training Badge */}
        <div className="bg-primary-600/10 border-b border-primary-500/20 px-4 py-2 flex items-center justify-center gap-2">
          <Shield className="w-4 h-4 text-primary-400" />
          <span className="text-xs font-medium text-primary-400">Smishing Detection Training</span>
        </div>
        
        {/* Messages Area */}
        <div className="h-[450px] bg-gray-800 flex flex-col">
          <MessageList messages={messages} />
        </div>
        
        {/* Action Buttons */}
        <div className="bg-gray-800 border-t border-gray-700 px-4 py-3 space-y-2">
          <div className="flex gap-2">
            <Button
              variant="danger"
              size="sm"
              onClick={handleReportSmishing}
              disabled={!currentScenario}
              className="flex-1 flex items-center justify-center gap-2"
            >
              <AlertTriangle className="w-4 h-4" />
              Report Smishing
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleDelete}
              disabled={!currentScenario}
              className="flex-1"
            >
              Ignore
            </Button>
          </div>
          
          {/* Scenario Counter */}
          {scenarios.length > 0 && (
            <p className="text-xs text-gray-500 text-center">
              {scenarios.length} message{scenarios.length !== 1 ? 's' : ''} remaining
            </p>
          )}
        </div>
        
        {/* Message Input (Visual Only) */}
        <div className="hidden">
          <MessageInput />
        </div>
        
        {/* Info Panel */}
        <div className="bg-gray-900/50 backdrop-blur-sm px-4 py-2 border-t border-gray-700">
          <div className="flex items-start gap-2">
            <Info className="w-4 h-4 text-primary-400 mt-0.5 flex-shrink-0" />
            <p className="text-xs text-gray-400 leading-relaxed">
              Look for suspicious links, urgent requests, unknown senders, and poor grammar
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SmishingClientPage;
