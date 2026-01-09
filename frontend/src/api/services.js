import api from './axiosConfig';

export const authService = {
  signup: (data) => api.post('/auth/signup', data),
  login: (email, password) => api.post('/auth/login', { email, password }),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/update-profile', data),
  logout: () => api.post('/auth/logout'),
  refresh: () => api.post('/auth/refresh')
};

export const productService = {
  getProducts: (page = 1, limit = 20, filters = {}) =>
    api.get('/products', { params: { page, limit, ...filters } }),
  getProduct: (productId) => api.get(`/products/${productId}`),
  createProduct: (data) => api.post('/products', data),
  updateProduct: (productId, data) => api.put(`/products/${productId}`, data),
  deleteProduct: (productId) => api.delete(`/products/${productId}`),
  getFarmerProducts: (farmerId, page = 1, limit = 20) =>
    api.get(`/products/farmer/${farmerId}`, { params: { page, limit } })
};

export const orderService = {
  createOrder: (data) => api.post('/orders', data),
  getOrders: (page = 1, limit = 20, filters = {}) =>
    api.get('/orders', { params: { page, limit, ...filters } }),
  getOrder: (orderId) => api.get(`/orders/${orderId}`),
  updateOrderStatus: (orderId, status) =>
    api.put(`/orders/${orderId}/status`, { status }),
  cancelOrder: (orderId) => api.post(`/orders/${orderId}/cancel`)
};

export const reviewService = {
  createReview: (productId, data) =>
    api.post('/reviews', { ...data, product_id: productId }),
  getReviews: (productId) =>
    api.get('/reviews', { params: { product_id: productId } }),
  updateReview: (reviewId, data) =>
    api.put(`/reviews/${reviewId}`, data),
  deleteReview: (reviewId) =>
    api.delete(`/reviews/${reviewId}`)
};

export const mlService = {
  analyzeImage: (formData) =>
    api.post('/ml/analyze-crop', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
  recommendCrops: (data) =>
    api.post('/ml/crop-recommendation', data),
  predictPrice: (data) =>
    api.post('/ml/price-prediction', data),
  recommendProducts: (nRecommendations = 5) =>
    api.post('/ml/product-recommendation', { n_recommendations: nRecommendations }),
  getModelInfo: () =>
    api.get('/ml/model-info')
};

export const chatbotService = {
  ask: (question) =>
    api.post('/chatbot/ask', { question }),
  getSuggestions: () =>
    api.get('/chatbot/suggestions'),
  getKBStats: () =>
    api.get('/chatbot/kb-stats'),
  addDocument: (data) =>
    api.post('/chatbot/add-document', data)
};

export const cartService = {
  addToCart: (product) => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const existing = cart.find(p => p.product_id === product.product_id);
    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({ ...product, quantity: 1 });
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    return cart;
  },

  removeFromCart: (productId) => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const filtered = cart.filter(p => p.product_id !== productId);
    localStorage.setItem('cart', JSON.stringify(filtered));
    return filtered;
  },

  updateQuantity: (productId, quantity) => {
    const cart = JSON.parse(localStorage.getItem('cart') || '[]');
    const item = cart.find(p => p.product_id === productId);
    if (item) {
      item.quantity = Math.max(1, quantity);
    }
    localStorage.setItem('cart', JSON.stringify(cart));
    return cart;
  },

  getCart: () =>
    JSON.parse(localStorage.getItem('cart') || '[]'),

  clearCart: () => {
    localStorage.setItem('cart', '[]');
    return [];
  }
};

export const adminService = {
  getUsers: (page = 1, limit = 20) =>
    api.get('/admin/users', { params: { page, limit } }),
  getUserDetails: (userId) =>
    api.get(`/admin/users/${userId}`),
  updateUser: (userId, data) =>
    api.put(`/admin/users/${userId}`, data),
  deleteUser: (userId) =>
    api.delete(`/admin/users/${userId}`),
  getProducts: (page = 1, limit = 20) =>
    api.get('/admin/products', { params: { page, limit } }),
  getOrders: (page = 1, limit = 20) =>
    api.get('/admin/orders', { params: { page, limit } }),
  uploadRAGDocument: (file) => {
    const formData = new FormData();
    formData.append('document', file);
    return api.post('/admin/upload-document', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }
};

export default {
  authService,
  productService,
  orderService,
  reviewService,
  mlService,
  chatbotService,
  cartService,
  adminService
};
