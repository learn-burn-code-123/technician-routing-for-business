# Deployment Guide - ISP Technician Routing System

## Prerequisites

- Python 3.8+
- Node.js 16+
- MongoDB 4.4+
- Redis (optional, for caching)
- Google Maps API Key
- Expo CLI (for mobile app)

## Backend Deployment

### 1. Environment Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your actual configuration values
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Start MongoDB
mongod --dbpath /path/to/your/db

# Create indexes (optional)
python scripts/create_indexes.py
```

### 4. Run Backend

```bash
# Development
python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## Frontend Deployment

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Setup

```bash
# Create .env file
REACT_APP_API_URL=http://localhost:5000/api/v1
```

### 3. Build and Deploy

```bash
# Development
npm start

# Production build
npm run build

# Deploy to static hosting (Netlify, Vercel, etc.)
```

## Mobile App Deployment

### 1. Install Dependencies

```bash
cd mobile
npm install
```

### 2. Configure API URL

Edit `src/services/api.js` to point to your production API URL.

### 3. Build and Deploy

```bash
# Development
expo start

# Build for production
expo build:android
expo build:ios
```

## Production Considerations

### Security
- Use HTTPS in production
- Set strong JWT secrets
- Configure proper CORS origins
- Enable rate limiting
- Use environment variables for sensitive data

### Monitoring
- Set up logging with structured logs
- Monitor API response times
- Track job completion rates
- Monitor technician locations and status

### Scaling
- Use load balancer for multiple backend instances
- Consider Redis for session storage
- Implement database connection pooling
- Use CDN for static assets

### Backup
- Regular MongoDB backups
- Backup environment configurations
- Store API keys securely
