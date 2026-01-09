import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import { ProtectedRoute } from './auth/ProtectedRoute';
import { useAuth } from './auth/AuthContext';
import { cartService } from './api/services';

// Pages
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Signup } from './pages/Signup';
import { FarmerDashboard } from './pages/FarmerDashboard';
import { ConsumerMarketplace } from './pages/ConsumerMarketplace';
import { ProductDetails } from './pages/ProductDetails';
import { Cart } from './pages/Cart';
import { Orders } from './pages/Orders';

// Components
import { Navbar } from './components/Navbar';
import { AIChatbot } from './components/AIChatbot';

// Main App Content
function AppContent() {
  const { isAuthenticated, user } = useAuth();
  const [cartCount, setCartCount] = useState(0);

  // Update cart count whenever localStorage changes
  useEffect(() => {
    const updateCartCount = () => {
      const cart = cartService.getCart();
      setCartCount(cart.length);
    };

    updateCartCount();

    // Listen for storage changes
    window.addEventListener('storage', updateCartCount);
    const interval = setInterval(updateCartCount, 500); // Poll every 500ms

    return () => {
      window.removeEventListener('storage', updateCartCount);
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen bg-white">
      <Navbar cartCount={cartCount} />

      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={isAuthenticated ? <Navigate to="/" replace /> : <Login />} />
        <Route path="/signup" element={isAuthenticated ? <Navigate to="/" replace /> : <Signup />} />

        {/* Farmer Routes */}
        <Route
          path="/farmer"
          element={
            <ProtectedRoute requiredRole="farmer">
              <FarmerDashboard />
            </ProtectedRoute>
          }
        />

        {/* Consumer Routes */}
        <Route
          path="/marketplace"
          element={
            <ProtectedRoute requiredRole="consumer">
              <ConsumerMarketplace />
            </ProtectedRoute>
          }
        />

        <Route
          path="/product/:productId"
          element={
            <ProtectedRoute requiredRole="consumer">
              <ProductDetails />
            </ProtectedRoute>
          }
        />

        <Route
          path="/cart"
          element={
            <ProtectedRoute requiredRole="consumer">
              <Cart />
            </ProtectedRoute>
          }
        />

        <Route
          path="/orders"
          element={
            <ProtectedRoute requiredRole="consumer">
              <Orders />
            </ProtectedRoute>
          }
        />

        {/* AI Assistant - Available to all authenticated users */}
        <Route
          path="/ai-assistant"
          element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 py-8">
                <div className="max-w-4xl mx-auto px-4">
                  <h1 className="text-3xl font-bold text-gray-900 mb-4">Agriculture AI Assistant</h1>
                  <p className="text-gray-600">Click the chat icon at the bottom right to start asking questions!</p>
                </div>
              </div>
            </ProtectedRoute>
          }
        />

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* AI Chatbot - Always available */}
      <AIChatbot />
    </div>
  );
}

// Main App with Router
export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}
