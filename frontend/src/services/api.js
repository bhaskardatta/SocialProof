import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      console.error('Network Error:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export const playerAPI = {
  createPlayer: (data) => api.post('/players/', data),
  getPlayers: (skip = 0, limit = 10) => api.get('/players/', { params: { skip, limit } }),
  getPlayer: (playerId) => api.get(`/players/${playerId}`),
  getPlayerStats: (playerId) => api.get(`/players/${playerId}/stats`),
};

export const scenarioAPI = {
  createScenario: (data) => api.post('/scenarios/', data),
  getScenario: (scenarioId) => api.get(`/scenarios/${scenarioId}`),
  getPlayerScenarios: (playerId) => api.get(`/players/${playerId}/scenarios`),
  generateAIScenario: (data) => api.post('/scenarios/generate', data),
  resolveScenario: (scenarioId, action) => api.post(`/scenarios/${scenarioId}/resolve`, { action }),
};

export const guardianAPI = {
  query: (data) => api.post('/guardian/query', data),
};

export const aiAPI = {
  getProvider: () => api.get('/ai/provider'),
  validateConfig: () => api.get('/ai/validate'),
};

export default api;
