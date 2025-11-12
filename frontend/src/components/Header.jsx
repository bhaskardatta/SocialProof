import { Link, useLocation } from 'react-router-dom';
import { Shield, Home, Award } from 'lucide-react';

function Header() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-800 bg-gray-900/80 backdrop-blur-lg supports-[backdrop-filter]:bg-gray-900/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="relative">
              <Shield className="h-8 w-8 text-primary-500 group-hover:text-primary-400 transition-colors" />
              <div className="absolute inset-0 bg-primary-500/20 blur-xl group-hover:bg-primary-400/30 transition-all"></div>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
              SocialProof
            </span>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-2">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/')
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-600/30'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              <Home className="h-4 w-4" />
              <span>Home</span>
            </Link>
            <Link
              to="/dashboard"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/dashboard')
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-600/30'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`}
            >
              <Award className="h-4 w-4" />
              <span>My Stats</span>
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

export default Header;
