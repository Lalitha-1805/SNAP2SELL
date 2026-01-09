import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { cartService, orderService } from '../api/services';
import { formatPrice, calculateCartTotal } from '../utils/helpers';
import { Loader } from '../components/Loader';

export const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Load cart on mount
  useEffect(() => {
    const cart = cartService.getCart();
    setCartItems(cart);
  }, []);

  const handleUpdateQuantity = (productId, newQuantity) => {
    if (newQuantity < 1) return;
    const updated = cartService.updateQuantity(productId, newQuantity);
    setCartItems(updated);
  };

  const handleRemoveItem = (productId) => {
    const updated = cartService.removeFromCart(productId);
    setCartItems(updated);
  };

  const handleCheckout = async () => {
    if (cartItems.length === 0) {
      setError('Cart is empty');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const orderData = {
        items: cartItems,
        total_amount: calculateCartTotal(cartItems),
        delivery_address: 'Default Address' // Can be enhanced with user input
      };

      const response = await orderService.createOrder(orderData);
      
      if (response.status === 201) {
        setSuccess('Order placed successfully!');
        cartService.clearCart();
        setCartItems([]);
        
        setTimeout(() => {
          navigate('/orders');
        }, 2000);
      }
    } catch (err) {
      const message = err.response?.data?.message || 'Failed to place order';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

        {/* Messages */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
            {success}
          </div>
        )}

        {cartItems.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-xl text-gray-600 mb-6">Your cart is empty</p>
            <button
              onClick={() => navigate('/marketplace')}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition"
            >
              Continue Shopping
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Cart Items */}
            <div className="lg:col-span-2 bg-white rounded-lg shadow">
              <div className="p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">
                  Items ({cartItems.length})
                </h2>

                <div className="space-y-4">
                  {cartItems.map((item) => (
                    <div key={item.product_id} className="flex gap-4 py-4 border-b last:border-b-0">
                      {/* Image */}
                      <div className="w-20 h-20 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        {item.image_url ? (
                          <img
                            src={item.image_url}
                            alt={item.name}
                            className="w-full h-full object-cover rounded"
                          />
                        ) : (
                          <span className="text-2xl">🌽</span>
                        )}
                      </div>

                      {/* Details */}
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{item.name}</h3>
                        <p className="text-green-600 font-bold mt-1">
                          {formatPrice(item.price)}
                        </p>

                        {/* Quantity Controls */}
                        <div className="flex items-center gap-2 mt-3">
                          <button
                            onClick={() => handleUpdateQuantity(item.product_id, item.quantity - 1)}
                            className="px-2 py-1 border border-gray-300 rounded hover:bg-gray-100"
                          >
                            −
                          </button>
                          <span className="px-4 py-1 border border-gray-300 rounded">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => handleUpdateQuantity(item.product_id, item.quantity + 1)}
                            className="px-2 py-1 border border-gray-300 rounded hover:bg-gray-100"
                          >
                            +
                          </button>
                        </div>
                      </div>

                      {/* Subtotal & Remove */}
                      <div className="text-right flex flex-col justify-between">
                        <div>
                          <p className="text-sm text-gray-600">Subtotal</p>
                          <p className="text-lg font-bold text-gray-900">
                            {formatPrice(item.price * item.quantity)}
                          </p>
                        </div>
                        <button
                          onClick={() => handleRemoveItem(item.product_id)}
                          className="text-red-600 hover:text-red-700 text-sm font-semibold"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Order Summary */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-6">Order Summary</h2>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-600">
                  <span>Subtotal</span>
                  <span>{formatPrice(calculateCartTotal(cartItems))}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Shipping</span>
                  <span>{formatPrice(0)}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                  <span>Tax</span>
                  <span>{formatPrice(0)}</span>
                </div>

                <div className="border-t pt-4 flex justify-between text-lg font-bold text-gray-900">
                  <span>Total</span>
                  <span>{formatPrice(calculateCartTotal(cartItems))}</span>
                </div>
              </div>

              <button
                onClick={handleCheckout}
                disabled={loading || cartItems.length === 0}
                className="w-full px-6 py-3 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white font-bold rounded-lg transition"
              >
                {loading ? 'Processing...' : 'Proceed to Checkout'}
              </button>

              <button
                onClick={() => navigate('/marketplace')}
                className="w-full mt-3 px-6 py-3 border-2 border-green-600 text-green-600 font-bold rounded-lg hover:bg-green-50 transition"
              >
                Continue Shopping
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
