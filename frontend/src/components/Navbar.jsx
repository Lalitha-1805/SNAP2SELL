import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export const Navbar = ({ cartCount = 0 }) => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="sticky top-0 z-50 bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 text-2xl font-bold hover:opacity-90 transition">
            <span>🌾</span>
            <span>AgriSmart</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <span className="text-sm">👤 {user?.name}</span>
                <span className="text-sm text-green-100">({user?.role})</span>

                {user?.role === 'farmer' && (
                  <Link
                    to="/farmer"
                    className="px-3 py-1 bg-yellow-500 hover:bg-yellow-600 rounded text-sm font-semibold transition"
                  >
                    Dashboard
                  </Link>
                )}

                {user?.role === 'consumer' && (
                  <>
                    <Link
                      to="/marketplace"
                      className="px-3 py-1 hover:bg-green-800 rounded text-sm transition"
                    >
                      Marketplace
                    </Link>
                    <Link
                      to="/cart"
                      className="px-3 py-1 hover:bg-green-800 rounded text-sm transition relative"
                    >
                      🛒 Cart
                      {cartCount > 0 && (
                        <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold">
                          {cartCount}
                        </span>
                      )}
                    </Link>
                    <Link
                      to="/orders"
                      className="px-3 py-1 hover:bg-green-800 rounded text-sm transition"
                    >
                      Orders
                    </Link>
                  </>
                )}

                <Link
                  to="/ai-assistant"
                  className="px-3 py-1 hover:bg-green-800 rounded text-sm transition"
                >
                  🤖 AI Assistant
                </Link>

                <button
                  onClick={handleLogout}
                  className="px-3 py-1 bg-red-600 hover:bg-red-700 rounded text-sm transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 text-white hover:bg-green-800 rounded text-sm transition"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="px-4 py-2 bg-white text-green-600 hover:bg-gray-100 rounded font-semibold text-sm transition"
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded hover:bg-green-800"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            {isAuthenticated ? (
              <>
                <div className="px-4 py-2 text-sm">
                  👤 {user?.name} ({user?.role})
                </div>

                {user?.role === 'farmer' && (
                  <Link
                    to="/farmer"
                    className="block px-4 py-2 hover:bg-green-800 rounded text-sm"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    Dashboard
                  </Link>
                )}

                {user?.role === 'consumer' && (
                  <>
                    <Link
                      to="/marketplace"
                      className="block px-4 py-2 hover:bg-green-800 rounded text-sm"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Marketplace
                    </Link>
                    <Link
                      to="/cart"
                      className="block px-4 py-2 hover:bg-green-800 rounded text-sm"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Cart ({cartCount})
                    </Link>
                    <Link
                      to="/orders"
                      className="block px-4 py-2 hover:bg-green-800 rounded text-sm"
                      onClick={() => setMobileMenuOpen(false)}
                    >
                      Orders
                    </Link>
                  </>
                )}

                <Link
                  to="/ai-assistant"
                  className="block px-4 py-2 hover:bg-green-800 rounded text-sm"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  AI Assistant
                </Link>

                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 bg-red-600 hover:bg-red-700 rounded text-sm"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="block px-4 py-2 hover:bg-green-800 rounded text-sm"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="block px-4 py-2 bg-white text-green-600 rounded font-semibold text-sm"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Sign Up
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </nav>
  );
};
