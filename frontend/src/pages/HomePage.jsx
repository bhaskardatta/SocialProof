import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Mail, MessageSquare, Phone, Shield, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { guardianAPI, aiAPI } from '../services/api';
import AppIcon from '../components/AppIcon';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../components/Card';
import { Button } from '../components/Button';
import { Textarea } from '../components/Textarea';
import { Label } from '../components/Label';

function HomePage() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [aiProvider, setAiProvider] = useState(null);

  useEffect(() => {
    const fetchAIProvider = async () => {
      try {
        const response = await aiAPI.getProvider();
        setAiProvider(response.data);
      } catch (err) {
        console.error('Failed to fetch AI provider:', err);
      }
    };
    fetchAIProvider();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      const response = await guardianAPI.query({ query });
      setAnswer(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const apps = [
    {
      icon: Mail,
      title: 'Email',
      description: 'Detect phishing attempts in your inbox and learn to identify fraudulent emails.',
      comingSoon: false,
    },
    {
      icon: MessageSquare,
      title: 'Messages',
      description: 'Recognize smishing attacks in SMS and protect your mobile communications.',
      comingSoon: false,
    },
    {
      icon: Phone,
      title: 'Phone',
      description: 'Identify vishing attempts and defend against voice-based social engineering.',
      comingSoon: true,
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      {/* Hero Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center space-y-6"
      >
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="inline-flex items-center space-x-2 bg-primary-600/10 border border-primary-600/20 text-primary-400 px-4 py-2 rounded-full text-sm font-medium"
        >
          <Shield className="h-4 w-4" />
          <span>Cybersecurity Training Platform</span>
        </motion.div>
        
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent"
        >
          Your Digital Life
        </motion.h1>
        
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed"
        >
          Master cybersecurity through interactive simulations. Train yourself to identify and defend against 
          phishing, smishing, and social engineering attacks in a safe, controlled environment.
        </motion.p>

        {aiProvider && aiProvider.status === 'active' && (
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 }}
            className="inline-flex items-center space-x-2 bg-success-600/10 border border-success-600/20 text-success-400 px-4 py-2 rounded-full text-sm"
          >
            <Sparkles className="h-4 w-4" />
            <span>AI Guardian Active ({aiProvider.provider})</span>
          </motion.div>
        )}
      </motion.div>

      {/* App Icons Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
        className="grid md:grid-cols-3 gap-6"
      >
        {apps.map((app, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 + index * 0.1 }}
            whileHover={{ y: -8, transition: { duration: 0.2 } }}
          >
            {index === 0 ? (
              <Link to="/simulations/email" className="block">
                <AppIcon {...app} />
              </Link>
            ) : index === 1 ? (
              <Link to="/simulations/sms" className="block">
                <AppIcon {...app} />
              </Link>
            ) : (
              <AppIcon {...app} />
            )}
          </motion.div>
        ))}
      </motion.div>

      {/* Digital Guardian Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      >
        <Card className="max-w-4xl mx-auto border-primary-600/30 shadow-2xl shadow-primary-500/10">
          <CardHeader>
            <div className="flex items-center space-x-3 mb-2">
              <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/30">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <CardTitle className="text-2xl">Digital Guardian</CardTitle>
                <CardDescription>Your AI-powered cybersecurity assistant</CardDescription>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="query">Ask a cybersecurity question</Label>
                <Textarea
                  id="query"
                  rows="4"
                  placeholder="e.g., What are the red flags in phishing emails? How can I identify a smishing attack?"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  disabled={loading}
                />
              </div>
              
              <Button
                type="submit"
                disabled={loading || !query.trim()}
                className="w-full"
                size="lg"
              >
                {loading ? (
                  <>
                    <Sparkles className="h-4 w-4 mr-2 animate-spin" />
                    Guardian is thinking...
                  </>
                ) : (
                  <>
                    <Shield className="h-4 w-4 mr-2" />
                    Ask Guardian
                  </>
                )}
              </Button>
            </form>

            {error && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="p-4 bg-danger-600/10 border border-danger-600/30 rounded-lg"
              >
                <p className="text-danger-400 text-sm">{error}</p>
              </motion.div>
            )}

            {answer && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4 p-6 bg-gray-800/50 rounded-lg border border-gray-700"
              >
                <div className="flex items-start space-x-3">
                  <Shield className="h-5 w-5 text-primary-400 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 space-y-3">
                    <p className="text-gray-100 leading-relaxed whitespace-pre-wrap">{answer.answer}</p>
                    
                    {answer.sources && answer.sources.length > 0 && (
                      <div className="pt-3 border-t border-gray-700">
                        <p className="text-xs font-semibold text-gray-400 mb-2">SOURCES</p>
                        <div className="space-y-1">
                          {answer.sources.map((source, index) => (
                            <div key={index} className="text-xs text-gray-500 flex items-center space-x-2">
                              <div className="h-1 w-1 rounded-full bg-primary-500"></div>
                              <span>{source}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div className="flex items-center justify-between pt-2">
                      <span className="text-xs text-gray-500">Powered by {answer.provider}</span>
                      <span className="text-xs text-gray-600">{new Date(answer.timestamp).toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Features Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1, duration: 0.6 }}
        className="grid md:grid-cols-3 gap-6 pt-8"
      >
        {[
          { icon: Mail, title: 'Phishing Detection', desc: 'Learn to identify fraudulent emails and protect yourself from credential theft attacks.', color: 'primary' },
          { icon: MessageSquare, title: 'Smishing Awareness', desc: 'Master SMS-based attack recognition and keep your mobile devices secure from threats.', color: 'success' },
          { icon: Shield, title: 'Social Engineering', desc: 'Understand psychological manipulation tactics used by attackers in modern cyber threats.', color: 'danger' },
        ].map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1 + index * 0.1 }}
            whileHover={{ y: -5, transition: { duration: 0.2 } }}
          >
            <Card className={`border-${feature.color}-600/20 h-full transition-all hover:border-${feature.color}-600/40 hover:shadow-lg hover:shadow-${feature.color}-500/10`}>
              <CardHeader>
                <div className={`h-12 w-12 rounded-xl bg-gradient-to-br from-${feature.color}-500 to-${feature.color}-700 flex items-center justify-center mb-4 shadow-lg shadow-${feature.color}-500/30`}>
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
                <CardDescription>{feature.desc}</CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}

export default HomePage;
