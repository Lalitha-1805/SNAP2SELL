# AgriSmart Quick Reference Guide

## 🚀 Start Here

### Windows Users
```bash
start.bat
```

### macOS/Linux Users
```bash
chmod +x start.sh
./start.sh
```

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:5173 | User interface |
| Backend API | http://localhost:5000/api | REST API |
| Health Check | http://localhost:5000/api/health | Server status |
| API Info | http://localhost:5000/api/info | Available endpoints |

## 📝 Common API Calls

### Authentication

**Sign Up**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "role": "farmer"
  }'
```

**Login**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Products

**List Products**
```bash
curl http://localhost:5000/api/products?page=1&limit=20&category=crops
```

**Create Product (Farmer)**
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "name": "Tomatoes",
    "category": "crops",
    "description": "Fresh tomatoes",
    "price": 50,
    "quantity": 100,
    "season": "Summer"
  }'
```

### Orders

**Create Order (Buyer)**
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "items": [
      {"product_id": "PRODUCT_ID", "quantity": 5}
    ],
    "shipping_address": "123 Main St"
  }'
```

**List Orders**
```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:5000/api/orders
```

### ML Predictions

**Crop Recommendation**
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

**Price Prediction**
```bash
curl -X POST http://localhost:5000/api/ml/price-prediction \
  -H "Content-Type: application/json" \
  -d '{
    "days_from_now": 7,
    "season": 0,
    "category": 0,
    "quantity": 100
  }'
```

**Product Recommendation (Buyer)**
```bash
curl -X POST http://localhost:5000/api/ml/product-recommendation \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "n_recommendations": 5
  }'
```

### Chatbot

**Ask Question**
```bash
curl -X POST http://localhost:5000/api/chatbot/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I prepare soil for vegetables?"
  }'
```

**Get Suggestions**
```bash
curl http://localhost:5000/api/chatbot/suggestions
```

## 🔐 User Roles

| Role | Can Do |
|------|--------|
| **farmer** | Create/update products, view orders, recommendations |
| **buyer** | Browse products, create orders, get recommendations |
| **admin** | Manage everything, update order status, add KB docs |

## 📊 Database Entities

### User
- `user_id`, `email`, `name`, `role`, `phone`, `address`

### Product
- `product_id`, `farmer_id`, `name`, `category`, `price`, `quantity`, `season`

### Order
- `order_id`, `buyer_id`, `items`, `total_price`, `status`, `shipping_address`

### Review
- `review_id`, `product_id`, `buyer_id`, `rating` (1-5), `comment`

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Ports in use | Kill process: `lsof -ti:5000 \| xargs kill -9` |
| MongoDB not found | Install/run MongoDB locally or use Atlas |
| Import errors | Activate venv: `source venv/bin/activate` |
| Dependencies missing | Run: `pip install -r requirements.txt` |
| npm issues | Delete node_modules: `rm -rf node_modules && npm install` |

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `config.py` | Configuration settings |
| `models/database.py` | Database models |
| `routes/*.py` | API endpoints |
| `ml/models.py` | ML implementations |
| `rag/chatbot.py` | RAG chatbot |
| `automation/scheduler.py` | Scheduled jobs |

## 🔑 Environment Variables

Must set in `.env`:
- `MONGODB_URI` - Database connection
- `JWT_SECRET_KEY` - JWT signing key
- `SECRET_KEY` - Flask secret key
- `FLASK_ENV` - development/production

Optional:
- `OPENAI_API_KEY` - For LLM features
- `MAIL_USERNAME`, `MAIL_PASSWORD` - For emails

## 📚 Documentation

- **README.md** - Full documentation
- **SETUP.md** - Installation guide
- **IMPLEMENTATION.md** - What's built
- **This file** - Quick reference

## 🚀 Deployment

### Docker
```bash
docker-compose up -d
```

### Manual
```bash
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend
cd frontend && npm run dev
```

## 🤖 ML Models

| Model | Input | Output |
|-------|-------|--------|
| Crop Recommendation | Environmental factors | Top 3 crops |
| Price Prediction | Market data | Predicted price |
| Product Recommendation | User history | Similar products |

## ⏰ Automation Jobs

- **Every 30 min**: Update prices
- **Daily 2 AM**: Check low stock
- **Every 6 hours**: Order reminders
- **Daily 9 AM**: Weather notifications

## 💡 Tips

1. Always activate virtual environment before working
2. Keep `.env` file with your actual credentials
3. Test API endpoints with curl before frontend
4. Check logs in terminal for errors
5. Restart servers if changes don't appear

## 🎯 Development Workflow

1. **Backend changes** → Auto-reload in dev mode
2. **Frontend changes** → Auto-refresh in Vite
3. **Database changes** → Manual migration
4. **ML changes** → Models auto-retrain

## 📞 Getting Help

1. Check API response messages
2. Review console logs
3. Check `.env` configuration
4. Verify MongoDB connection
5. Read SETUP.md troubleshooting

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 16+ installed
- [ ] MongoDB running/configured
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` configured
- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:5173
- [ ] API responds at localhost:5000/api/health

## 🎉 Next Steps

1. Run startup script
2. Test API endpoints
3. Create test users
4. Add test products
5. Create orders
6. Explore AI features
7. Customize for production

---

**AgriSmart - Making Agriculture Smart and Profitable! 🌾**
