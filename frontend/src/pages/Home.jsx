import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';

export const Home = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Side */}
          <div>
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              AgriSmart: AI-Powered Agriculture
            </h1>
            <p className="text-xl text-gray-700 mb-8">
              Connect farmers directly with consumers. Leverage AI for crop analysis, price prediction, and smart recommendations.
            </p>

            <div className="flex gap-4 mb-12">
              {isAuthenticated ? (
                <>
                  {user?.role === 'farmer' ? (
                    <button
                      onClick={() => navigate('/farmer')}
                      className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition"
                    >
                      Go to Dashboard
                    </button>
                  ) : (
                    <button
                      onClick={() => navigate('/marketplace')}
                      className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition"
                    >
                      Go to Marketplace
                    </button>
                  )}
                </>
              ) : (
                <>
                  <button
                    onClick={() => navigate('/signup')}
                    className="px-8 py-4 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition"
                  >
                    Get Started
                  </button>
                  <button
                    onClick={() => navigate('/login')}
                    className="px-8 py-4 border-2 border-green-600 text-green-600 font-bold rounded-lg hover:bg-green-50 transition"
                  >
                    Login
                  </button>
                </>
              )}
            </div>

            {/* Features */}
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <span className="text-2xl">🌾</span>
                <div>
                  <h3 className="font-bold text-gray-900">For Farmers</h3>
                  <p className="text-gray-600">Upload crops, get AI-powered descriptions & price predictions</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">🛒</span>
                <div>
                  <h3 className="font-bold text-gray-900">For Consumers</h3>
                  <p className="text-gray-600">Browse fresh products directly from farmers</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-2xl">🤖</span>
                <div>
                  <h3 className="font-bold text-gray-900">AI Assistant</h3>
                  <p className="text-gray-600">Get instant answers to agriculture questions</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Illustration */}
          <div className="hidden lg:flex items-center justify-center">
            <div className="text-center">
              <div className="text-9xl mb-6">🌾</div>
              <div className="text-8xl mb-6 animate-pulse">📱</div>
              <div className="text-8xl">🚀</div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-16">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Key Features</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <span className="text-4xl mb-4 block">🖼️</span>
              <h3 className="text-lg font-bold text-gray-900 mb-2">AI Image Analysis</h3>
              <p className="text-gray-600">Upload crop images for instant AI analysis, description generation, and price suggestions</p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <span className="text-4xl mb-4 block">📊</span>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Price Prediction</h3>
              <p className="text-gray-600">ML-powered price prediction based on crop type, quality, and market trends</p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <span className="text-4xl mb-4 block">🔍</span>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Smart Search</h3>
              <p className="text-gray-600">Find products by category, location, price, and get personalized recommendations</p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <span className="text-4xl mb-4 block">💬</span>
              <h3 className="text-lg font-bold text-gray-900 mb-2">AI Chatbot</h3>
              <p className="text-gray-600">24/7 agriculture support with RAG-powered knowledge base</p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <span className="text-4xl mb-4 block">🛒</span>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Easy Ordering</h3>
              <p className="text-gray-600">Browse, compare, and order fresh agricultural products seamlessly</p>
            </div>

            <div className="p-6 rounded-lg shadow-md hover:shadow-lg transition">
              <span className="text-4xl mb-4 block">⭐</span>
              <h3 className="text-lg font-bold text-gray-900 mb-2">Reviews & Ratings</h3>
              <p className="text-gray-600">Read authentic reviews from other buyers to make informed decisions</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Join the AgriSmart Community</h2>
          <p className="text-lg mb-8">Whether you're a farmer looking to sell or a consumer seeking fresh products, AgriSmart connects you directly.</p>

          {!isAuthenticated && (
            <button
              onClick={() => navigate('/signup')}
              className="px-8 py-4 bg-white text-green-600 font-bold rounded-lg hover:bg-gray-100 transition"
            >
              Sign Up Now
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
