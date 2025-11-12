import { useState, useEffect } from 'react';
import { Users, Sparkles, Plus, CheckCircle, XCircle } from 'lucide-react';
import { playerAPI, scenarioAPI } from '../services/api';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '../components/Card';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Label } from '../components/Label';

function DashboardPage() {
  const [players, setPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [scenarios, setScenarios] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generatingScenario, setGeneratingScenario] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [newPlayerForm, setNewPlayerForm] = useState({
    username: '',
    email: '',
  });

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await playerAPI.getPlayers(0, 50);
      setPlayers(response.data);
    } catch (err) {
      setError('Failed to fetch players');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPlayerScenarios = async (playerId) => {
    try {
      const response = await scenarioAPI.getPlayerScenarios(playerId);
      setScenarios(response.data);
    } catch (err) {
      console.error('Failed to fetch scenarios:', err);
    }
  };

  const handleSelectPlayer = async (player) => {
    setSelectedPlayer(player);
    await fetchPlayerScenarios(player.id);
  };

  const handleCreatePlayer = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await playerAPI.createPlayer(newPlayerForm);
      setNewPlayerForm({ username: '', email: '' });
      setSuccess('Player created successfully!');
      await fetchPlayers();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create player');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateScenario = async () => {
    if (!selectedPlayer) return;

    setGeneratingScenario(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await scenarioAPI.generateAIScenario({
        player_id: selectedPlayer.id,
        scenario_type: 'EMAIL_PHISH',
      });
      
      await fetchPlayerScenarios(selectedPlayer.id);
      setSuccess(`Scenario generated! Difficulty: ${response.data.difficulty_label}`);
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate scenario');
    } finally {
      setGeneratingScenario(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-2">
          Administration Dashboard
        </h1>
        <p className="text-gray-400">Manage players and generate AI-powered training scenarios</p>
      </div>

      {/* Notifications */}
      {error && (
        <div className="flex items-center space-x-3 p-4 bg-danger-600/10 border border-danger-600/30 rounded-lg">
          <XCircle className="h-5 w-5 text-danger-400 flex-shrink-0" />
          <p className="text-danger-400 text-sm">{error}</p>
        </div>
      )}

      {success && (
        <div className="flex items-center space-x-3 p-4 bg-success-600/10 border border-success-600/30 rounded-lg">
          <CheckCircle className="h-5 w-5 text-success-400 flex-shrink-0" />
          <p className="text-success-400 text-sm">{success}</p>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Player Management Card */}
        <Card className="border-primary-600/30">
          <CardHeader>
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center shadow-lg shadow-primary-500/30">
                <Users className="h-5 w-5 text-white" />
              </div>
              <div>
                <CardTitle>Player Management</CardTitle>
                <CardDescription>Create and manage training participants</CardDescription>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            <form onSubmit={handleCreatePlayer} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  required
                  placeholder="Enter username"
                  value={newPlayerForm.username}
                  onChange={(e) => setNewPlayerForm({ ...newPlayerForm, username: e.target.value })}
                  disabled={loading}
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  required
                  placeholder="Enter email address"
                  value={newPlayerForm.email}
                  onChange={(e) => setNewPlayerForm({ ...newPlayerForm, email: e.target.value })}
                  disabled={loading}
                />
              </div>
              
              <Button
                type="submit"
                disabled={loading}
                className="w-full"
              >
                <Plus className="h-4 w-4 mr-2" />
                Create Player
              </Button>
            </form>

            <div className="border-t border-gray-800 pt-6">
              <h3 className="text-sm font-semibold text-gray-300 mb-4">REGISTERED PLAYERS ({players.length})</h3>
              {loading && players.length === 0 ? (
                <div className="text-center py-8 text-gray-500">Loading players...</div>
              ) : players.length === 0 ? (
                <div className="text-center py-8 text-gray-500">No players yet</div>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto pr-2">
                  {players.map((player) => (
                    <div
                      key={player.id}
                      onClick={() => handleSelectPlayer(player)}
                      className={`p-4 rounded-lg cursor-pointer transition-all ${
                        selectedPlayer?.id === player.id
                          ? 'bg-primary-600/20 border-2 border-primary-500 shadow-lg shadow-primary-500/20'
                          : 'bg-gray-800/50 hover:bg-gray-800 border-2 border-transparent'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-white">{player.username}</div>
                          <div className="text-sm text-gray-400">{player.email}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs text-gray-500">Skill Rating</div>
                          <div className="text-lg font-bold text-primary-400">{player.player_skill_rating}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Scenario Generation Card */}
        <Card className="border-success-600/30">
          <CardHeader>
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-success-500 to-success-700 flex items-center justify-center shadow-lg shadow-success-500/30">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div>
                <CardTitle>AI Scenario Generation</CardTitle>
                <CardDescription>Create adaptive training scenarios</CardDescription>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {selectedPlayer ? (
              <>
                <div className="p-4 bg-gray-800/50 rounded-lg border border-gray-700">
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <div className="text-sm text-gray-400">Selected Player</div>
                      <div className="text-lg font-bold text-white">{selectedPlayer.username}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-gray-500">Skill Rating</div>
                      <div className="text-2xl font-bold text-primary-400">{selectedPlayer.player_skill_rating}</div>
                    </div>
                  </div>
                  <div className="text-xs text-gray-500">{selectedPlayer.email}</div>
                </div>

                <Button
                  onClick={handleGenerateScenario}
                  disabled={generatingScenario}
                  className="w-full"
                  variant="success"
                  size="lg"
                >
                  {generatingScenario ? (
                    <>
                      <Sparkles className="h-4 w-4 mr-2 animate-spin" />
                      Generating Scenario...
                    </>
                  ) : (
                    <>
                      <Sparkles className="h-4 w-4 mr-2" />
                      Generate AI Scenario
                    </>
                  )}
                </Button>

                <div className="border-t border-gray-800 pt-6">
                  <h3 className="text-sm font-semibold text-gray-300 mb-4">
                    SCENARIOS ({scenarios.length})
                  </h3>
                  {scenarios.length === 0 ? (
                    <div className="text-center py-12 bg-gray-800/30 rounded-lg border border-gray-700/50">
                      <Sparkles className="h-12 w-12 text-gray-600 mx-auto mb-3" />
                      <p className="text-gray-500 mb-2">No scenarios yet</p>
                      <p className="text-sm text-gray-600">Click "Generate AI Scenario" to create one</p>
                    </div>
                  ) : (
                    <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
                      {scenarios.map((scenario) => (
                        <div
                          key={scenario.id}
                          className="p-4 bg-gray-800/50 rounded-lg border border-gray-700 hover:border-gray-600 transition-colors"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-primary-600/20 text-primary-400 border border-primary-600/30">
                              {scenario.scenario_type}
                            </span>
                            <span className="text-xs text-gray-500">
                              Level: {scenario.difficulty_level.toFixed(1)}
                            </span>
                          </div>
                          <p className="text-sm text-gray-300 line-clamp-3">
                            {scenario.content}
                          </p>
                          <div className="mt-3 pt-3 border-t border-gray-700 text-xs text-gray-500">
                            {new Date(scenario.created_at).toLocaleString()}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="text-center py-20">
                <Users className="h-16 w-16 text-gray-700 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-300 mb-2">Select a Player</h3>
                <p className="text-gray-500 text-sm">
                  Choose a player from the left panel to generate scenarios
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default DashboardPage;
