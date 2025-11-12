import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import MainLayout from './components/MainLayout';
import HomePage from './pages/HomePage';
import PlayerDashboardPage from './pages/PlayerDashboardPage';
import DashboardPage from './pages/DashboardPage';
import EmailClientPage from './pages/simulations/EmailClientPage';
import SmishingClientPage from './pages/simulations/SmishingClientPage';

function App() {
  return (
    <Router>
      <Toaster 
        position="top-center" 
        reverseOrder={false}
        toastOptions={{
          // Default options
          duration: 4000,
          style: {
            background: '#1f2937',
            color: '#f3f4f6',
            border: '1px solid #374151',
          },
          // Success toast style
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#f3f4f6',
            },
          },
          // Error toast style
          error: {
            duration: 4000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#f3f4f6',
            },
          },
        }}
      />
      <MainLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<PlayerDashboardPage />} />
          <Route path="/admin" element={<DashboardPage />} />
          <Route path="/simulations/email" element={<EmailClientPage />} />
          <Route path="/simulations/sms" element={<SmishingClientPage />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;
