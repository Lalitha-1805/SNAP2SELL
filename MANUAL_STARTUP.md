# AgriSmart - Manual Startup Guide

## If the automated script fails, follow these manual steps:

### STEP 1: Setup Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Or PowerShell:
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

**Expected Output:**
```
✓ MongoDB connected successfully
✓ All MongoDB indexes created successfully
✓ Flask application initialized successfully

🚀 Server running on http://0.0.0.0:5000
📚 API Documentation: http://0.0.0.0:5000/api/info
💾 Database: agrismart
```

---

### STEP 2: Setup Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Expected Output:**
```
  ➜  Local:   http://localhost:5173/
  ➜  Press h to show help
```

---

### STEP 3: Access the Application

Open your browser:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

---

## Troubleshooting

### Issue: Python not found
**Solution:**
```bash
# Install Python 3.10+
# Download from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation
python --version  # Should show Python 3.10+
```

### Issue: Node not found
**Solution:**
```bash
# Install Node.js 16+
# Download from https://nodejs.org/
node --version  # Should show v16+
npm --version   # Should show 8+
```

### Issue: Virtual environment activation fails
**Solution (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Issue: Port already in use
**Solution:**
```bash
# Find process on port 5000
netstat -ano | findstr :5000
# Kill process (replace PID with the number found)
taskkill /PID <PID> /F

# For port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Issue: Module not found error
**Solution:**
```bash
# Ensure venv is activated
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: npm dependencies fail
**Solution:**
```bash
# Clear cache and reinstall
cd frontend
rm -r node_modules package-lock.json
npm cache clean --force
npm install
```

---

## Quick Test After Startup

### Test Backend API
```bash
# In another terminal or Postman
curl http://localhost:5000/api/health
# Should return: {"status":"healthy",...}

curl http://localhost:5000/api/info
# Should return API information
```

### Test Frontend
Visit http://localhost:5173 in your browser

---

## MongoDB Setup

If you don't have MongoDB set up, you have two options:

### Option 1: MongoDB Atlas (Cloud - Recommended)
1. Go to https://www.mongodb.com/atlas
2. Create a free account
3. Create a cluster
4. Get connection string
5. Update `.env` file:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agrismart
```

### Option 2: Local MongoDB
1. Download from https://www.mongodb.com/try/download/community
2. Install and start MongoDB
3. Update `.env` file:
```
MONGODB_URI=mongodb://localhost:27017/agrismart
```

---

## Environment Configuration

Edit `backend/.env` with your settings:

```env
# Required
FLASK_ENV=development
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/agrismart
JWT_SECRET_KEY=your-secret-key-here
SECRET_KEY=your-secret-key-here

# Optional but recommended
OPENAI_API_KEY=sk-your-key
HF_TOKEN=hf-your-token
```

---

## Next Steps After Startup

1. **Test API Endpoints**
   ```bash
   # Signup
   curl -X POST http://localhost:5000/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"user@test.com","password":"pass123","name":"Test","role":"farmer"}'
   ```

2. **Build Frontend Components**
   - Add pages for signup/login
   - Add product listing
   - Add order management
   - Add AI chatbot interface

3. **Configure MongoDB**
   - Setup connection
   - Create indexes
   - Add sample data

4. **Test ML Features**
   ```bash
   # Crop recommendation
   curl -X POST http://localhost:5000/api/ml/crop-recommendation \
     -H "Content-Type: application/json" \
     -d '{"soil_type":"Loam","season":"Monsoon","rainfall":"High","temperature":25,"humidity":75}'
   ```

5. **Deploy**
   - Docker: `docker-compose up -d`
   - Cloud: Follow platform-specific guides

---

## Support

If you encounter issues:
1. Check the console logs for error messages
2. Verify all prerequisites are installed
3. Check .env configuration
4. Ensure MongoDB is accessible
5. Read detailed SETUP.md guide

---

**AgriSmart is now ready to develop!** 🌾
