# AgriSmart Installation & Setup Guide

## Prerequisites

Before starting, ensure you have:

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **MongoDB** - Local or [MongoDB Atlas](https://www.mongodb.com/atlas)
- **Git** - [Download](https://git-scm.com/)

## Step 1: Clone the Repository

```bash
cd agri-smart
```

## Step 2: Backend Setup

### 2.1 Create Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
cd ..
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
cd ..
```

### 2.2 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 2.3 Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your values:

```env
# Essential Configuration
FLASK_ENV=development
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agrismart
JWT_SECRET_KEY=your-secret-key-change-this
```

### 2.4 Verify MongoDB Connection

```bash
cd backend
python -c "from extensions import init_mongo; from config import config; print('Testing MongoDB...')"
```

## Step 3: Frontend Setup

### 3.1 Install Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3.2 Configure Environment (Optional)

Create `.env` in frontend directory:
```
VITE_API_URL=http://localhost:5000/api
```

## Step 4: Run the Application

### Option A: Automated Startup

**Windows:**
```bash
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### Option B: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Step 5: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api
- **API Health**: http://localhost:5000/api/health
- **API Info**: http://localhost:5000/api/info

## Database Setup

### Option 1: Local MongoDB

```bash
# Windows (if MongoDB installed)
mongod

# macOS (with Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### Option 2: MongoDB Atlas (Cloud)

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Get connection string
4. Update `MONGODB_URI` in `.env`

## Testing the API

### 1. User Signup

```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "password123",
    "name": "John Farmer",
    "role": "farmer"
  }'
```

### 2. User Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "farmer@example.com",
    "password": "password123"
  }'
```

**Response:**
```json
{
  "status": "success",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "user_id": "...",
    "email": "farmer@example.com",
    "name": "John Farmer",
    "role": "farmer"
  }
}
```

### 3. Create Product (Farmer)

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
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

### 4. Get Crop Recommendations

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

### 5. Ask Chatbot

```bash
curl -X POST http://localhost:5000/api/chatbot/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How should I prepare soil for vegetable farming?"
  }'
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up -d
```

Services will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- MongoDB: localhost:27017

### Stop Docker Services

```bash
docker-compose down
```

## Troubleshooting

### 1. Python Virtual Environment Issues

**Problem**: `venv not activating`

**Solution**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. MongoDB Connection Failed

**Problem**: `Unable to connect to MongoDB`

**Solution**:
- Verify MongoDB is running
- Check MONGODB_URI in `.env`
- Ensure IP whitelist in MongoDB Atlas

### 3. Port Already in Use

**Problem**: `Address already in use`

**Solution**:
```bash
# Find process using port (Windows)
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Find and kill process (macOS/Linux)
lsof -ti:5000 | xargs kill -9
```

### 4. Module Not Found

**Problem**: `ModuleNotFoundError`

**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### 5. Node Modules Issues

**Problem**: `npm module errors`

**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Performance Tuning

### Backend

```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Frontend

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Change `JWT_SECRET_KEY` in `.env`
- [ ] Use strong MongoDB password
- [ ] Enable HTTPS in production
- [ ] Set `FLASK_ENV=production`
- [ ] Configure rate limiting
- [ ] Enable CORS properly
- [ ] Keep dependencies updated

## Next Steps

1. **Explore the API**: Use Postman or curl to test endpoints
2. **Build Frontend UI**: Develop React components for each feature
3. **Setup Database**: Create sample data
4. **Configure Email**: Setup SMTP for notifications
5. **Deploy**: Deploy to cloud platform (Heroku, AWS, GCP, etc.)

## Getting Help

- Check API documentation: `/api/info`
- View logs in console
- Check database collections in MongoDB
- Review error messages carefully

## Performance Monitoring

### Check API Health

```bash
curl http://localhost:5000/api/health
```

### Monitor Database

```bash
curl http://localhost:5000/api/database-info
```

### Check Scheduler Status

```bash
curl http://localhost:5000/api/scheduler-status
```

## Development Workflow

1. **Backend Changes**: Changes hot-reload in development mode
2. **Frontend Changes**: Vite auto-refreshes on save
3. **Database Changes**: Manually run migration scripts
4. **ML Model Changes**: Models retrain automatically

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Setup Complete!** 🎉

Your AgriSmart instance is now running. Start developing!
