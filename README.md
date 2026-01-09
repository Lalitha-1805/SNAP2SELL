# AgriSmart - AI-Powered Agriculture E-Commerce Platform

A complete, production-ready agriculture e-commerce platform with machine learning, RAG-powered chatbot, and automation capabilities.

## 🌾 Features

### Core Features
- **User Management**: Farmer, Buyer, and Admin roles with JWT authentication
- **Product Management**: Create, list, search, and filter agricultural products
- **Order Management**: Complete order lifecycle with status tracking
- **Reviews & Ratings**: Product reviews and buyer feedback

### Machine Learning
- **Crop Recommendation**: Random Forest classifier for crop suggestions based on environmental factors
- **Price Prediction**: Regression model for future price forecasting
- **Product Recommendation**: Collaborative filtering for personalized recommendations

### RAG Chatbot
- **Knowledge Base**: FAISS vector database with agriculture information
- **Query Processing**: LangChain-powered semantic search and retrieval
- **Smart Responses**: Context-aware answers to farming questions

### Automation
- **Price Updates**: Automatic market price tracking and updates
- **Stock Alerts**: Low inventory notifications
- **Order Reminders**: Pending order follow-ups
- **Weather Notifications**: Weather-based farming alerts

## 🏗️ Project Structure

```
agri-smart/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── config.py              # Configuration management
│   ├── extensions.py          # Flask extensions setup
│   ├── requirements.txt        # Python dependencies
│   ├── .env                   # Environment variables
│   ├── models/
│   │   ├── database.py        # MongoDB models
│   │   └── __init__.py
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── products.py        # Product endpoints
│   │   ├── orders.py          # Order endpoints
│   │   ├── ml.py              # ML prediction endpoints
│   │   ├── chatbot.py         # Chatbot endpoints
│   │   └── __init__.py
│   ├── services/              # Business logic
│   ├── ml/
│   │   ├── models.py          # ML model implementations
│   │   └── __init__.py
│   ├── rag/
│   │   ├── chatbot.py         # RAG chatbot
│   │   └── __init__.py
│   ├── automation/
│   │   ├── scheduler.py       # APScheduler tasks
│   │   └── __init__.py
│   ├── utils/
│   │   ├── validators.py      # Input validation
│   │   ├── errors.py          # Custom error classes
│   │   ├── decorators.py      # Authentication decorators
│   │   └── __init__.py
│   └── data/                  # ML models and knowledge base
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx           # React entry point
│   │   ├── App.jsx            # Main component
│   │   ├── api.js             # Axios client
│   │   ├── services.js        # API service calls
│   │   └── index.css          # Tailwind CSS
│   └── public/
└── README.md
```

## 🚀 Quick Start

### Backend Setup

1. **Clone and navigate to backend**
```bash
cd agri-smart/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Edit `.env` file with your MongoDB URI and other configs:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agrismart
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

5. **Run application**
```bash
python app.py
```

Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend**
```bash
cd agri-smart/frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend runs on `http://localhost:5173`

## 📚 API Documentation

### Authentication Endpoints

```
POST   /api/auth/signup              # Register new user
POST   /api/auth/login               # User login
POST   /api/auth/refresh             # Refresh JWT token
GET    /api/auth/profile             # Get user profile
PUT    /api/auth/update-profile      # Update profile
POST   /api/auth/logout              # Logout
```

### Product Endpoints

```
GET    /api/products                 # List all products (paginated)
GET    /api/products/<id>            # Get product details
POST   /api/products                 # Create product (farmer only)
PUT    /api/products/<id>            # Update product (owner only)
DELETE /api/products/<id>            # Delete product (owner only)
GET    /api/products/farmer/<id>     # Get farmer's products
```

### Order Endpoints

```
POST   /api/orders                   # Create order (buyer only)
GET    /api/orders                   # List user's orders (paginated)
GET    /api/orders/<id>              # Get order details
PUT    /api/orders/<id>/status       # Update status (admin only)
POST   /api/orders/<id>/cancel       # Cancel order (owner only)
```

### ML Endpoints

```
POST   /api/ml/crop-recommendation   # Get crop recommendations
POST   /api/ml/price-prediction      # Predict crop prices
POST   /api/ml/product-recommendation # Get personalized products
GET    /api/ml/model-info            # Get available models info
```

### Chatbot Endpoints

```
POST   /api/chatbot/ask              # Ask agricultural question
GET    /api/chatbot/suggestions      # Get question suggestions
GET    /api/chatbot/kb-stats         # Knowledge base statistics
POST   /api/chatbot/add-document     # Add KB document (admin)
```

### System Endpoints

```
GET    /api/health                   # Health check
GET    /api/info                     # API information
GET    /api/database-info            # Database status
GET    /api/scheduler-status         # Automation job status
```

## 🔑 Authentication

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <access_token>
```

### User Roles

- **farmer**: Can create and manage products
- **buyer**: Can browse and purchase products
- **admin**: Full platform access

## 🤖 Machine Learning Models

### 1. Crop Recommendation
**Input:**
- Soil type (Loam, Clay, Sandy, Silt, Chalk)
- Season (Spring, Summer, Monsoon, Winter)
- Rainfall (Low, Medium, High)
- Temperature (0-50°C)
- Humidity (0-100%)

**Output:**
- Top 3 recommended crops with confidence scores

### 2. Price Prediction
**Input:**
- Days from now (0-365)
- Season (0-3)
- Category (0-4)
- Quantity (units)

**Output:**
- Predicted price
- Confidence level

### 3. Product Recommendation
**Input:**
- Buyer ID (authenticated user)
- Number of recommendations (1-20)

**Output:**
- List of personalized product recommendations

## 💬 RAG Chatbot

The chatbot uses:
- **Embeddings**: Sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS for semantic search
- **Knowledge Base**: Agricultural information and best practices

### Knowledge Topics
- Crop rotation
- Soil preparation
- Fertilizer management
- Pest management
- Irrigation techniques
- Disease prevention
- Government schemes
- Harvesting practices

## ⏰ Automation Tasks

Scheduled jobs that run automatically:

1. **Price Updates** (Every 30 min)
   - Updates market prices
   - Records price history
   
2. **Stock Alerts** (Daily at 2 AM)
   - Notifies farmers of low inventory
   
3. **Order Reminders** (Every 6 hours)
   - Reminds buyers about pending orders
   
4. **Weather Notifications** (Daily at 9 AM)
   - Sends weather-based farming alerts

## 🗄️ Database Schema

### MongoDB Collections

**users**
```javascript
{
  _id: ObjectId,
  email: String (unique),
  password_hash: String,
  name: String,
  role: String (farmer/buyer/admin),
  phone: String,
  address: String,
  is_active: Boolean,
  created_at: DateTime,
  updated_at: DateTime
}
```

**products**
```javascript
{
  _id: ObjectId,
  farmer_id: ObjectId,
  name: String,
  category: String,
  description: String,
  price: Number,
  quantity: Number,
  soil_type: String,
  season: String,
  quality_grade: String,
  image_url: String,
  rating: Number,
  review_count: Number,
  is_active: Boolean,
  created_at: DateTime,
  updated_at: DateTime
}
```

**orders**
```javascript
{
  _id: ObjectId,
  buyer_id: ObjectId,
  items: Array,
  total_price: Number,
  status: String,
  shipping_address: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

**reviews**
```javascript
{
  _id: ObjectId,
  product_id: ObjectId,
  buyer_id: ObjectId,
  rating: Number (1-5),
  comment: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA256 password hashing
- **CORS**: Enabled for frontend communication
- **Input Validation**: Comprehensive input validation
- **Role-Based Access Control**: User role enforcement
- **Error Handling**: Proper error responses without data leakage

## 📝 Example API Usage

### User Signup
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "password123",
    "name": "John Farmer",
    "role": "farmer",
    "phone": "+919876543210"
  }'
```

### Create Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Organic Tomatoes",
    "category": "crops",
    "description": "Fresh organic tomatoes",
    "price": 50,
    "quantity": 100,
    "season": "Summer",
    "quality_grade": "A"
  }'
```

### Crop Recommendation
```bash
curl -X POST http://localhost:5000/api/ml/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "soil_type": "Loam",
    "season": "Monsoon",
    "rainfall": "High",
    "temperature": 25,
    "humidity": 75
  }'
```

### Ask Chatbot
```bash
curl -X POST http://localhost:5000/api/chatbot/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How should I prepare soil for vegetable farming?"
  }'
```

## 🧪 Testing

Run tests (when implemented):
```bash
pytest
```

## 📦 Deployment

### Production Checklist

1. ✅ Update `.env` with production values
2. ✅ Use production MongoDB URI
3. ✅ Set `FLASK_ENV=production`
4. ✅ Use strong secret keys
5. ✅ Enable HTTPS
6. ✅ Set up proper logging
7. ✅ Configure rate limiting
8. ✅ Set up monitoring

### Deploy with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔧 Configuration

Key configuration options in `config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | development |
| `DEBUG` | Debug mode | False |
| `MONGODB_URI` | MongoDB connection | localhost |
| `JWT_ACCESS_TOKEN_EXPIRES` | Token expiry | 1 hour |
| `CORS_ORIGINS` | Allowed origins | localhost |

## 📊 Performance Optimization

- **Database Indexes**: Created on frequently queried fields
- **Pagination**: Implemented for list endpoints
- **Caching**: Ready for Redis integration
- **ML Model Serialization**: Models saved as .pkl files
- **Background Jobs**: APScheduler for non-blocking tasks

## 🐛 Troubleshooting

### MongoDB Connection Failed
- Verify MongoDB URI in `.env`
- Check network connectivity
- Ensure MongoDB Atlas IP whitelist includes your IP

### ML Models Not Loading
- Check if `models/` directory exists
- Verify scikit-learn and joblib are installed
- Models auto-train on first run

### CORS Errors
- Add frontend URL to `CORS_ORIGINS` in config.py
- Ensure backend is running before frontend

### JWT Token Expired
- Frontend automatically refreshes expired tokens
- Check JWT_SECRET_KEY is consistent

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API examples

## 🎯 Future Enhancements

- [ ] Advanced payment integration
- [ ] Real-time notifications
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Video consultations with experts
- [ ] Blockchain for supply chain
- [ ] IoT sensor integration
- [ ] Multilingual support

---


