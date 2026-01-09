import React, { useState, useEffect } from 'react'
import { authService, productService, orderService } from './services'

// ============================================
// NAVBAR COMPONENT
// ============================================
function Navbar({ isAuth, user, onNavigate, onLogout, cartCount }) {
  return (
    <nav className="sticky top-0 bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <button onClick={() => onNavigate('home')} className="flex items-center space-x-2 text-2xl font-bold hover:opacity-90">
          <span>🌾</span>
          <span>AgriSmart</span>
        </button>
        <div className="flex items-center space-x-4">
          {isAuth ? (
            <>
              <span className="text-sm">👤 {user?.name} ({user?.role})</span>
              {user?.role === 'farmer' && (
                <button onClick={() => onNavigate('farmer-dashboard')} className="px-3 py-1 bg-yellow-500 rounded hover:bg-yellow-600 text-sm font-bold">
                  Dashboard
                </button>
              )}
              {user?.role === 'consumer' && (
                <>
                  <button onClick={() => onNavigate('marketplace')} className="px-3 py-1 hover:bg-green-800 rounded text-sm">
                    Marketplace
                  </button>
                  <button onClick={() => onNavigate('cart')} className="px-3 py-1 hover:bg-green-800 rounded text-sm relative">
                    🛒 Cart {cartCount > 0 && <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">{cartCount}</span>}
                  </button>
                  <button onClick={() => onNavigate('orders')} className="px-3 py-1 hover:bg-green-800 rounded text-sm">
                    Orders
                  </button>
                </>
              )}
              <button onClick={() => onNavigate('ai-assistant')} className="px-3 py-1 hover:bg-green-800 rounded text-sm">
                AI Assistant
              </button>
              {user?.role === 'admin' && (
                <button onClick={() => onNavigate('admin')} className="px-3 py-1 bg-purple-600 rounded hover:bg-purple-700 text-sm font-bold">
                  Admin
                </button>
              )}
              <button onClick={onLogout} className="px-3 py-1 bg-red-600 rounded hover:bg-red-700 text-sm">
                Logout
              </button>
            </>
          ) : (
            <>
              <button onClick={() => onNavigate('login')} className="px-4 py-2 border-2 border-white rounded hover:bg-green-800">
                Login
              </button>
              <button onClick={() => onNavigate('signup')} className="px-4 py-2 bg-yellow-500 text-gray-900 rounded font-bold hover:bg-yellow-600">
                Sign Up
              </button>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

// ============================================
// HOME PAGE
// ============================================
function HomePage({ onNavigate }) {
  return (
    <div className="min-h-screen bg-white">
      <section className="bg-gradient-to-r from-green-500 to-green-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-5xl font-bold mb-6">Direct from Farm to Your Table</h1>
          <p className="text-xl mb-8">Buy fresh agricultural products & AI-powered farming guidance</p>
          <div className="space-x-4">
            <button onClick={() => onNavigate('marketplace')} className="px-8 py-3 bg-yellow-500 text-gray-900 font-bold rounded hover:bg-yellow-600">
              Browse Products
            </button>
            <button onClick={() => onNavigate('signup')} className="px-8 py-3 border-2 border-white rounded hover:bg-green-800">
              Join Now
            </button>
          </div>
        </div>
      </section>

      <section className="bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-3 gap-8 text-center">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-4xl font-bold text-green-600">2340+</h3>
            <p className="text-gray-600">Active Farmers</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-4xl font-bold text-green-600">1240+</h3>
            <p className="text-gray-600">Products</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-4xl font-bold text-green-600">5630+</h3>
            <p className="text-gray-600">Happy Buyers</p>
          </div>
        </div>
      </section>
    </div>
  )
}

// ============================================
// MARKETPLACE PAGE
// ============================================
function MarketplacePage() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ category: 'all', priceMax: 10000, search: '' })

  useEffect(() => {
    loadProducts()
  }, [filters])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const res = await productService.getProducts(1, 20, filters.category === 'all' ? null : filters.category)
      let filtered = (res.data.products || []).filter(p => p.price <= filters.priceMax)
      if (filters.search) {
        filtered = filtered.filter(p => p.name.toLowerCase().includes(filters.search.toLowerCase()))
      }
      setProducts(filtered)
    } catch (err) {
      console.error('Failed to load products:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddToCart = (product) => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]')
    const existing = cart.find(p => p.product_id === product.product_id)
    if (existing) {
      existing.quantity += 1
    } else {
      cart.push({ ...product, quantity: 1 })
    }
    localStorage.setItem('cart', JSON.stringify(cart))
    alert('Added to cart!')
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-6">
        <h1 className="text-3xl font-bold mb-8">Agricultural Marketplace</h1>

        <div className="bg-white p-6 rounded-lg shadow mb-8 grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-bold mb-2">Search</label>
            <input
              type="text"
              placeholder="Search products..."
              value={filters.search}
              onChange={(e) => setFilters({...filters, search: e.target.value})}
              className="w-full px-4 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-bold mb-2">Category</label>
            <select
              value={filters.category}
              onChange={(e) => setFilters({...filters, category: e.target.value})}
              className="w-full px-4 py-2 border rounded"
            >
              <option value="all">All Categories</option>
              <option value="Vegetables">Vegetables</option>
              <option value="Grains">Grains</option>
              <option value="Fruits">Fruits</option>
              <option value="Spices">Spices</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-bold mb-2">Max Price: ₹{filters.priceMax}</label>
            <input
              type="range"
              min="0"
              max="50000"
              value={filters.priceMax}
              onChange={(e) => setFilters({...filters, priceMax: parseInt(e.target.value)})}
              className="w-full"
            />
          </div>
        </div>

        {loading ? (
          <div className="text-center text-gray-500">Loading products...</div>
        ) : products.length === 0 ? (
          <div className="text-center text-gray-500">No products found</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <div key={product.product_id} className="bg-white rounded-lg shadow hover:shadow-lg transition overflow-hidden">
                <div className="h-48 bg-gradient-to-br from-green-200 to-green-300 flex items-center justify-center text-6xl">
                  {product.category === 'Vegetables' ? '🥕' : product.category === 'Grains' ? '🌾' : product.category === 'Fruits' ? '🍎' : '🌶️'}
                </div>
                <div className="p-4">
                  <h3 className="font-bold text-lg mb-1">{product.name}</h3>
                  <p className="text-sm text-gray-600 mb-2">{product.category}</p>
                  <p className="text-xs text-gray-500 mb-3">{product.description?.substring(0, 50)}...</p>
                  <div className="flex justify-between items-center mb-3">
                    <p className="text-2xl font-bold text-green-600">₹{product.price}</p>
                    <p className="text-yellow-500">⭐ {product.rating?.toFixed(1) || 'N/A'}</p>
                  </div>
                  <button onClick={() => handleAddToCart(product)} className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 font-bold">
                    Add to Cart
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// ============================================
// CART PAGE
// ============================================
function CartPage({ onNavigate }) {
  const [cart, setCart] = useState([])

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem('cart') || '[]')
    setCart(stored)
  }, [])

  const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  const handleCheckout = async () => {
    if (cart.length === 0) return

    try {
      const orderData = {
        products: cart.map(p => ({ product_id: p.product_id, quantity: p.quantity, price: p.price })),
        total_price: total,
        status: 'pending'
      }
      
      await orderService.createOrder(orderData)
      localStorage.setItem('cart', '[]')
      alert('Order placed successfully!')
      onNavigate('orders')
    } catch (err) {
      alert('Failed to place order: ' + (err.response?.data?.message || err.message))
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-6">
        <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

        {cart.length === 0 ? (
          <div className="bg-white p-8 rounded-lg shadow text-center">
            <p className="text-gray-600 mb-4">Your cart is empty</p>
            <button onClick={() => onNavigate('marketplace')} className="px-6 py-2 bg-green-600 text-white rounded hover:bg-green-700">
              Continue Shopping
            </button>
          </div>
        ) : (
          <>
            <div className="bg-white rounded-lg shadow mb-8">
              {cart.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center p-6 border-b">
                  <div>
                    <h3 className="font-bold text-lg">{item.name}</h3>
                    <p className="text-gray-600">₹{item.price} x {item.quantity}</p>
                  </div>
                  <p className="text-xl font-bold">₹{item.price * item.quantity}</p>
                </div>
              ))}
            </div>

            <div className="bg-white p-6 rounded-lg shadow mb-8">
              <div className="text-right">
                <p className="text-gray-600 mb-2">Subtotal: ₹{total}</p>
                <p className="text-gray-600 mb-4">Shipping: Free</p>
                <p className="text-3xl font-bold text-green-600 mb-6">Total: ₹{total}</p>
                <button onClick={handleCheckout} className="w-full px-6 py-3 bg-green-600 text-white font-bold rounded hover:bg-green-700 text-lg">
                  Place Order
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

// ============================================
// ORDERS PAGE
// ============================================
function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadOrders()
  }, [])

  const loadOrders = async () => {
    try {
      const res = await orderService.getOrders()
      setOrders(res.data.orders || [])
    } catch (err) {
      console.error('Failed to load orders:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = { pending: 'yellow', confirmed: 'blue', shipped: 'purple', delivered: 'green' }
    return colors[status] || 'gray'
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-6">
        <h1 className="text-3xl font-bold mb-8">My Orders</h1>

        {loading ? (
          <div className="text-center text-gray-500">Loading orders...</div>
        ) : orders.length === 0 ? (
          <div className="text-center text-gray-500">No orders yet</div>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => (
              <div key={order.order_id} className="bg-white p-6 rounded-lg shadow">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-bold text-lg">Order #{order.order_id}</h3>
                    <p className="text-gray-600">{new Date(order.created_at).toLocaleDateString()}</p>
                  </div>
                  <span className={`px-4 py-2 bg-${getStatusColor(order.status)}-200 text-${getStatusColor(order.status)}-800 rounded font-bold`}>
                    {order.status?.charAt(0).toUpperCase() + order.status?.slice(1)}
                  </span>
                </div>

                <div className="border-t pt-4">
                  <div className="flex justify-between items-end">
                    <div>
                      <p className="text-sm text-gray-600">Total: <span className="text-2xl font-bold text-green-600">₹{order.total_price}</span></p>
                    </div>
                    <div className="flex space-x-2">
                      {['pending', 'confirmed', 'shipped', 'delivered'].map((s, i) => (
                        <div key={i} className={`text-center ${['pending', 'confirmed', 'shipped', 'delivered'].indexOf(order.status) >= i ? 'text-green-600' : 'text-gray-400'}`}>
                          <div className="text-2xl">{'✓'}</div>
                          <p className="text-xs">{s}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// ============================================
// FARMER DASHBOARD
// ============================================
function FarmerDashboardPage() {
  const [products, setProducts] = useState([])
  const [showAddProduct, setShowAddProduct] = useState(false)
  const [formData, setFormData] = useState({ name: '', category: 'Vegetables', price: '', quantity: '', description: '' })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadFarmerProducts()
  }, [])

  const loadFarmerProducts = async () => {
    try {
      const res = await productService.getProducts()
      setProducts(res.data.products || [])
    } catch (err) {
      console.error('Failed to load products:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddProduct = async (e) => {
    e.preventDefault()
    try {
      await productService.createProduct(formData)
      alert('Product added successfully!')
      setFormData({ name: '', category: 'Vegetables', price: '', quantity: '', description: '' })
      setShowAddProduct(false)
      loadFarmerProducts()
    } catch (err) {
      alert('Failed to add product: ' + (err.response?.data?.message || err.message))
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Farmer Dashboard</h1>
          <button onClick={() => setShowAddProduct(!showAddProduct)} className="px-6 py-3 bg-green-600 text-white font-bold rounded hover:bg-green-700">
            + Add Product
          </button>
        </div>

        {showAddProduct && (
          <div className="bg-white p-8 rounded-lg shadow mb-8">
            <h2 className="text-2xl font-bold mb-6">Add New Product</h2>
            <form onSubmit={handleAddProduct} className="space-y-4">
              <input
                type="text"
                placeholder="Product Name"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className="w-full px-4 py-2 border rounded"
                required
              />
              <select
                value={formData.category}
                onChange={(e) => setFormData({...formData, category: e.target.value})}
                className="w-full px-4 py-2 border rounded"
              >
                <option>Vegetables</option>
                <option>Grains</option>
                <option>Fruits</option>
                <option>Spices</option>
              </select>
              <input
                type="number"
                placeholder="Price (₹)"
                value={formData.price}
                onChange={(e) => setFormData({...formData, price: parseInt(e.target.value)})}
                className="w-full px-4 py-2 border rounded"
                required
              />
              <input
                type="number"
                placeholder="Quantity (kg)"
                value={formData.quantity}
                onChange={(e) => setFormData({...formData, quantity: parseInt(e.target.value)})}
                className="w-full px-4 py-2 border rounded"
                required
              />
              <textarea
                placeholder="Description"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                className="w-full px-4 py-2 border rounded h-24"
              ></textarea>
              <button type="submit" className="w-full bg-green-600 text-white py-3 rounded font-bold hover:bg-green-700">
                Add Product
              </button>
            </form>
          </div>
        )}

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-6">My Products ({products.length})</h2>
          {loading ? (
            <div>Loading...</div>
          ) : products.length === 0 ? (
            <div className="text-gray-500">No products yet</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {products.map((product) => (
                <div key={product.product_id} className="border rounded-lg p-4">
                  <h3 className="font-bold text-lg mb-2">{product.name}</h3>
                  <p className="text-gray-600 mb-2">{product.category}</p>
                  <p className="text-2xl font-bold text-green-600 mb-2">₹{product.price}</p>
                  <p className="text-sm text-gray-600 mb-4">Stock: {product.quantity}kg</p>
                  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mr-2">
                    Edit
                  </button>
                  <button className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ============================================
// AI ASSISTANT PAGE
// ============================================
function AIAssistantPage() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! I\'m AgriSmart Assistant. Ask me about crops, farming, prices, or anything agriculture-related!' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return

    setMessages([...messages, { role: 'user', text: input }])
    setLoading(true)

    try {
      // Call backend chatbot API
      const res = await chatbotService.ask(input)
      const botResponse = res.data.data.answer || 'Unable to process your question'
      
      setMessages(prev => [...prev, { role: 'bot', text: botResponse }])
    } catch (err) {
      console.error('AI error:', err)
      const errorMsg = err.response?.data?.message || 'Error connecting to AI Assistant'
      setMessages(prev => [...prev, { role: 'bot', text: errorMsg }])
    } finally {
      setLoading(false)
      setInput('')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-6">
        <div className="bg-white rounded-lg shadow h-[600px] flex flex-col">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-md px-4 py-2 rounded-lg ${msg.role === 'user' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-900'}`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {loading && <div className="text-center text-gray-500">Thinking...</div>}
          </div>

          <div className="border-t p-4 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about crops, farming, prices..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-600"
            />
            <button onClick={handleSend} disabled={loading} className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 font-bold disabled:opacity-50">
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================
// LOGIN PAGE
// ============================================
function LoginPage({ onLogin, onSwitchToSignup }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await authService.login(email, password)
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)
      onLogin(res.data.user)
    } catch (err) {
      console.error('Login error:', err)
      setError(err.response?.data?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold mb-6 text-center">Login to AgriSmart</h2>
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-2 rounded font-bold hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <button onClick={onSwitchToSignup} className="w-full text-center text-blue-600 hover:underline mt-4">
          Don't have an account? Sign Up
        </button>
      </div>
    </div>
  )
}

// ============================================
// SIGNUP PAGE
// ============================================
function SignupPage({ onSignup, onSwitchToLogin }) {
  const [formData, setFormData] = useState({ name: '', email: '', password: '', role: 'consumer', phone: '', address: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await authService.signup(formData)
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)
      onSignup(res.data.user)
    } catch (err) {
      console.error('Signup error:', err)
      const errorMsg = err.response?.data?.message || err.message || 'Signup failed'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold mb-6 text-center">Join AgriSmart</h2>
        {error && <div className="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Full Name"
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            required
          />
          <input
            type="password"
            placeholder="Password (min 6 chars)"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            required
          />
          <input
            type="tel"
            placeholder="Phone Number"
            value={formData.phone}
            onChange={(e) => setFormData({...formData, phone: e.target.value})}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          />
          <input
            type="text"
            placeholder="Address"
            value={formData.address}
            onChange={(e) => setFormData({...formData, address: e.target.value})}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          />
          <select
            value={formData.role}
            onChange={(e) => setFormData({...formData, role: e.target.value})}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          >
            <option value="consumer">I'm a Consumer</option>
            <option value="farmer">I'm a Farmer</option>
          </select>
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 text-white py-2 rounded font-bold hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>
        <button onClick={onSwitchToLogin} className="w-full text-center text-blue-600 hover:underline mt-4">
          Already have an account? Login
        </button>
      </div>
    </div>
  )
}

// ============================================
// ADMIN DASHBOARD
// ============================================
function AdminDashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-6">
        <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
        
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 font-bold mb-2">Total Users</h3>
            <p className="text-3xl font-bold text-green-600">2340+</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 font-bold mb-2">Total Products</h3>
            <p className="text-3xl font-bold text-blue-600">1240+</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 font-bold mb-2">Total Orders</h3>
            <p className="text-3xl font-bold text-purple-600">5630+</p>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-2xl font-bold mb-4">Manage Platform</h2>
          <div className="space-y-2">
            <button className="w-full text-left px-4 py-3 bg-gray-50 rounded hover:bg-gray-100">View All Users</button>
            <button className="w-full text-left px-4 py-3 bg-gray-50 rounded hover:bg-gray-100">Review Products</button>
            <button className="w-full text-left px-4 py-3 bg-gray-50 rounded hover:bg-gray-100">Verify Farmers</button>
            <button className="w-full text-left px-4 py-3 bg-gray-50 rounded hover:bg-gray-100">Monitor Orders</button>
            <button className="w-full text-left px-4 py-3 bg-gray-50 rounded hover:bg-gray-100">Upload RAG Documents</button>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================
// MAIN APP COMPONENT
// ============================================
export default function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const [cart, setCart] = useState([])

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      authService.getProfile()
        .then(res => {
          setUser(res.data.user)
          setIsAuthenticated(true)
        })
        .catch(() => {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          setIsAuthenticated(false)
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }

    // Load cart
    const stored = JSON.parse(localStorage.getItem('cart') || '[]')
    setCart(stored)
  }, [])

  if (loading) {
    return <div className="flex items-center justify-center h-screen text-lg">Loading AgriSmart...</div>
  }

  const handleNavigate = (page) => {
    if (['marketplace', 'ai-assistant', 'farmer-dashboard', 'cart', 'orders', 'admin'].includes(page) && !isAuthenticated) {
      setCurrentPage('login')
      return
    }
    setCurrentPage(page)
  }

  const handleLogin = (userData) => {
    setUser(userData)
    setIsAuthenticated(true)
    setCurrentPage(userData.role === 'farmer' ? 'farmer-dashboard' : userData.role === 'admin' ? 'admin' : 'marketplace')
  }

  const handleLogout = () => {
    authService.logout().catch(() => {})
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    setIsAuthenticated(false)
    setCurrentPage('home')
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={handleNavigate} />
      case 'marketplace':
        return <MarketplacePage />
      case 'cart':
        return <CartPage onNavigate={handleNavigate} />
      case 'orders':
        return <OrdersPage />
      case 'ai-assistant':
        return <AIAssistantPage />
      case 'farmer-dashboard':
        return <FarmerDashboardPage />
      case 'admin':
        return <AdminDashboardPage />
      case 'login':
        return <LoginPage onLogin={handleLogin} onSwitchToSignup={() => setCurrentPage('signup')} />
      case 'signup':
        return <SignupPage onSignup={handleLogin} onSwitchToLogin={() => setCurrentPage('login')} />
      default:
        return <HomePage onNavigate={handleNavigate} />
    }
  }

  return (
    <div className="min-h-screen bg-white">
      <Navbar 
        isAuth={isAuthenticated} 
        user={user} 
        onNavigate={handleNavigate} 
        onLogout={handleLogout}
        cartCount={cart.length}
      />
      {renderPage()}
    </div>
  )
}