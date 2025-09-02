# Frontend-Backend Integration Guide

## 🌐 Connecting Your Frontend to StudyBloom Backend

### Prerequisites
- Backend running on `http://localhost:5000`
- Frontend running on `http://localhost:3000` (or your frontend port)
- PostgreSQL database configured

## 🚀 Quick Setup

### 1. Database Setup
```bash
# Navigate to backend directory
cd backend/StudyBloom

# Install dependencies
pip install -r requirements.txt

# Set up your PostgreSQL database URL in .env
echo "DATABASE_URL=postgresql://username:password@localhost/study_bloom" > .env

# Create database tables and sample data
python setup_db.py
```

### 2. Start Backend Server
```bash
# Start the Flask server
python run.py
```

Your backend will be running at: `http://localhost:5000`

## 🔗 API Integration Examples

### Authentication

#### Login
```javascript
// Frontend JavaScript/React
const loginUser = async (username, password) => {
  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Important for session cookies
      body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      // Handle successful login
      return data;
    }
  } catch (error) {
    console.error('Login error:', error);
  }
};
```

#### Register
```javascript
const registerUser = async (username, email, password) => {
  try {
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ username, email, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (error) {
    console.error('Registration error:', error);
  }
};
```

### Goals & Tasks

#### Get User Goals
```javascript
const fetchGoals = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/goals', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const goals = await response.json();
      return goals;
    }
  } catch (error) {
    console.error('Error fetching goals:', error);
  }
};
```

#### Create New Goal
```javascript
const createGoal = async (title, description, deadline) => {
  try {
    const response = await fetch('http://localhost:5000/api/goals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        title,
        description,
        deadline: deadline.toISOString()
      })
    });
    
    if (response.ok) {
      const goal = await response.json();
      return goal;
    }
  } catch (error) {
    console.error('Error creating goal:', error);
  }
};
```

### Streaks & Analytics

#### Get Current Streak
```javascript
const fetchStreak = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/streaks', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const streak = await response.json();
      return streak;
    }
  } catch (error) {
    console.error('Error fetching streak:', error);
  }
};
```

#### Update Streak (when user completes task)
```javascript
const updateStreak = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/streaks/update', {
      method: 'POST',
      credentials: 'include'
    });
    
    if (response.ok) {
      const result = await response.json();
      return result;
    }
  } catch (error) {
    console.error('Error updating streak:', error);
  }
};
```

### Rewards

#### Get Available Rewards
```javascript
const fetchRewards = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/rewards/available', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const rewards = await response.json();
      return rewards;
    }
  } catch (error) {
    console.error('Error fetching rewards:', error);
  }
};
```

### Study Groups

#### Check Group Eligibility
```javascript
const checkGroupEligibility = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/groups/check-eligibility', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const eligibility = await response.json();
      return eligibility;
    }
  } catch (error) {
    console.error('Error checking eligibility:', error);
  }
};
```

#### Get Available Groups
```javascript
const fetchAvailableGroups = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/groups/available', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const groups = await response.json();
      return groups;
    }
  } catch (error) {
    console.error('Error fetching groups:', error);
  }
};
```

## 🎨 Frontend Integration Patterns

### React Hook Example
```javascript
// hooks/useStudyBloom.js
import { useState, useEffect } from 'react';

export const useStudyBloom = () => {
  const [user, setUser] = useState(null);
  const [goals, setGoals] = useState([]);
  const [streak, setStreak] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUserData = async () => {
    try {
      // Fetch user goals
      const goalsResponse = await fetch('http://localhost:5000/api/goals', {
        credentials: 'include'
      });
      if (goalsResponse.ok) {
        const goalsData = await goalsResponse.json();
        setGoals(goalsData);
      }

      // Fetch user streak
      const streakResponse = await fetch('http://localhost:5000/api/streaks', {
        credentials: 'include'
      });
      if (streakResponse.ok) {
        const streakData = await streakResponse.json();
        setStreak(streakData);
      }
    } catch (error) {
      console.error('Error fetching user data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  return { user, goals, streak, loading, fetchUserData };
};
```

### Context Provider Example
```javascript
// contexts/StudyBloomContext.js
import React, { createContext, useContext, useState } from 'react';

const StudyBloomContext = createContext();

export const StudyBloomProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [goals, setGoals] = useState([]);
  const [streak, setStreak] = useState(null);

  const login = async (username, password) => {
    // Login implementation
  };

  const createGoal = async (goalData) => {
    // Create goal implementation
  };

  const updateStreak = async () => {
    // Update streak implementation
  };

  return (
    <StudyBloomContext.Provider value={{
      user,
      goals,
      streak,
      login,
      createGoal,
      updateStreak
    }}>
      {children}
    </StudyBloomContext.Provider>
  );
};

export const useStudyBloom = () => useContext(StudyBloomContext);
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in your frontend project:
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENVIRONMENT=development
```

### CORS Configuration
The backend is already configured to accept requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

If your frontend runs on a different port, update the CORS configuration in `app/__init__.py`.

## 🧪 Testing the Integration

### 1. Test Authentication
```bash
# Test login with sample user
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  -c cookies.txt
```

### 2. Test API Endpoints
```bash
# Test goals endpoint
curl -X GET http://localhost:5000/api/goals \
  -b cookies.txt

# Test streak endpoint
curl -X GET http://localhost:5000/api/streaks \
  -b cookies.txt
```

## 🚨 Common Issues & Solutions

### CORS Errors
- Ensure backend CORS is configured correctly
- Check that frontend URL is in allowed origins
- Use `credentials: 'include'` in fetch requests

### Session Issues
- Backend uses Flask-Login for session management
- Ensure cookies are being sent with requests
- Check that `credentials: 'include'` is set

### Database Connection
- Verify PostgreSQL is running
- Check database URL in `.env` file
- Ensure database exists and user has permissions

## 📱 Mobile App Integration

For mobile apps (React Native, Flutter), use the same API endpoints but:
- Replace `credentials: 'include'` with proper token management
- Use JWT tokens instead of session cookies
- Implement proper error handling for network issues

## 🔄 Real-time Updates

For real-time features (chat, notifications), consider:
- WebSocket integration
- Server-Sent Events (SSE)
- Polling for updates

## 📊 Monitoring & Debugging

### Backend Logs
```bash
# Enable debug mode
export DEBUG=1
python run.py
```

### Frontend Network Tab
- Use browser dev tools to monitor API calls
- Check request/response headers
- Verify CORS headers are present

## 🎯 Next Steps

1. **Test all API endpoints** with your frontend
2. **Implement error handling** for network issues
3. **Add loading states** for better UX
4. **Implement offline support** if needed
5. **Add real-time features** for collaboration 