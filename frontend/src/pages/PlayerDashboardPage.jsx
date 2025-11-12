import { useState, useEffect } from 'react';
import { Shield, Target, AlertTriangle, CheckCircle, TrendingUp, Award } from 'lucide-react';
import { motion } from 'framer-motion';
import { playerAPI } from '../services/api';
import StatCard from '../components/dashboard/StatCard';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../components/Card';

/**
 * PlayerDashboardPage - Player performance statistics dashboard
 * 
 * This component displays comprehensive performance metrics for a player,
 * including skill rating, accuracy, phishing detection stats, and more.
 * Uses a clean card-based layout with visual indicators.
 */
const PlayerDashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Hardcoded player_id for now (will be dynamic with auth system)
  const playerId = 1;

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await playerAPI.getPlayerStats(playerId);
        setStats(response.data);
      } catch (err) {
        console.error('Error fetching player stats:', err);
        setError('Failed to load statistics. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [playerId]);

  // Loading State
  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <Shield className="w-12 h-12 text-primary-400 animate-pulse mx-auto mb-3" />
            <p className="text-gray-400">Loading your statistics...</p>
          </div>
        </div>
      </div>
    );
  }

  // Error State
  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertTriangle className="w-12 h-12 text-red-400 mx-auto mb-3" />
            <p className="text-red-400">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      {/* Header Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center space-y-4"
      >
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="inline-flex items-center space-x-2 bg-primary-600/10 border border-primary-600/20 text-primary-400 px-4 py-2 rounded-full text-sm font-medium"
        >
          <Award className="h-4 w-4" />
          <span>Performance Dashboard</span>
        </motion.div>
        
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent"
        >
          Your Statistics
        </motion.h1>
        
        <motion.p 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-gray-400 max-w-2xl mx-auto"
        >
          Track your progress and performance across all cybersecurity training scenarios
        </motion.p>
      </motion.div>

      {/* Main Stats Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="grid md:grid-cols-3 gap-6"
      >
        {[
          { icon: Shield, title: "Skill Rating", value: stats.current_skill_rating.toFixed(0), unit: "pts", description: "Your current skill level", variant: "primary" },
          { icon: Target, title: "Accuracy", value: stats.accuracy_percentage.toFixed(1), unit: "%", description: "Overall success rate", variant: stats.accuracy_percentage >= 70 ? 'success' : stats.accuracy_percentage >= 50 ? 'warning' : 'danger' },
          { icon: TrendingUp, title: "Scenarios Completed", value: stats.total_scenarios_resolved, description: "Total training scenarios", variant: "primary" }
        ].map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 + index * 0.1 }}
            whileHover={{ y: -5, transition: { duration: 0.2 } }}
          >
            <StatCard {...stat} />
          </motion.div>
        ))}
      </motion.div>

      {/* Detailed Performance Stats */}
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9, duration: 0.6 }}
        className="grid md:grid-cols-2 gap-6"
      >
        {/* Phishing Detection Stats */}
        <motion.div
          whileHover={{ y: -5, transition: { duration: 0.2 } }}
        >
          <Card className="border-gray-800 hover:border-success-600/30 transition-all">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-success-500 to-success-700 flex items-center justify-center shadow-lg shadow-success-500/30">
                  <CheckCircle className="h-5 w-5 text-white" />
                </div>
                <CardTitle>Phishing Detection</CardTitle>
              </div>
              <CardDescription>
                Your performance in identifying phishing attacks
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                <span className="text-gray-300">Correctly Identified</span>
                <span className="text-2xl font-bold text-success-400">
                  {stats.correctly_identified_phish}
                </span>
              </div>
              <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                <span className="text-gray-300">Missed Threats</span>
                <span className="text-2xl font-bold text-danger-400">
                  {stats.missed_phish}
                </span>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Error Analysis */}
        <motion.div
          whileHover={{ y: -5, transition: { duration: 0.2 } }}
        >
          <Card className="border-gray-800 hover:border-yellow-600/30 transition-all">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-yellow-500 to-yellow-700 flex items-center justify-center shadow-lg shadow-yellow-500/30">
                  <AlertTriangle className="h-5 w-5 text-white" />
                </div>
                <CardTitle>Error Analysis</CardTitle>
              </div>
              <CardDescription>
                Areas for improvement in your training
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-800/50 rounded-lg">
                <span className="text-gray-300">False Positives</span>
                <span className="text-2xl font-bold text-yellow-400">
                  {stats.incorrectly_reported_safe}
                </span>
              </div>
              <div className="p-4 bg-primary-600/10 border border-primary-500/20 rounded-lg">
                <p className="text-sm text-primary-400">
                  💡 <strong>Tip:</strong> Focus on analyzing sender addresses and looking for urgency tactics in messages.
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </motion.div>

      {/* Progress Insights */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.1, duration: 0.6 }}
      >
        <Card className="border-primary-600/30">
          <CardHeader>
            <CardTitle className="text-xl">Performance Insights</CardTitle>
            <CardDescription>
              How you're progressing in your cybersecurity training
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {/* Skill Rating Insight */}
              <motion.div 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.2 }}
                className="flex items-start gap-3 p-4 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors"
              >
                <Shield className="w-5 h-5 text-primary-400 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-white mb-1">Skill Rating Progress</p>
                  <p className="text-sm text-gray-400">
                    {stats.current_skill_rating >= 600 
                      ? "Excellent! You're performing at an advanced level."
                      : stats.current_skill_rating >= 500
                      ? "Good progress! Keep training to reach expert level."
                      : "You're learning! More practice will improve your skills."}
                  </p>
                </div>
              </motion.div>

              {/* Accuracy Insight */}
              <motion.div 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.3 }}
                className="flex items-start gap-3 p-4 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors"
              >
                <Target className="w-5 h-5 text-success-400 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-white mb-1">Accuracy Analysis</p>
                  <p className="text-sm text-gray-400">
                    {stats.accuracy_percentage >= 80
                      ? "Outstanding accuracy! You're consistently making correct decisions."
                      : stats.accuracy_percentage >= 60
                      ? "Solid performance. Focus on reducing mistakes for even better results."
                      : "Keep practicing! Review the training tips to improve your accuracy."}
                  </p>
                </div>
              </motion.div>

              {/* Detection Rate Insight */}
              <motion.div 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.4 }}
                className="flex items-start gap-3 p-4 bg-gray-800/30 rounded-lg hover:bg-gray-800/50 transition-colors"
              >
                <CheckCircle className="w-5 h-5 text-success-400 mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-white mb-1">Threat Detection</p>
                  <p className="text-sm text-gray-400">
                    {stats.missed_phish === 0
                      ? "Perfect! You haven't missed any phishing attempts."
                      : stats.missed_phish <= 2
                      ? `Good job! Only ${stats.missed_phish} missed threat${stats.missed_phish > 1 ? 's' : ''}. Stay vigilant!`
                      : `You've missed ${stats.missed_phish} threats. Focus on identifying suspicious patterns.`}
                  </p>
                </div>
              </motion.div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default PlayerDashboardPage;
