# 🚀 StudyBloom Frontend-Backend Integration Setup Guide

## 📋 Overview
This guide will help you connect your frontend with the StudyBloom backend using the comprehensive PostgreSQL database schema.

## 🗄️ Step 1: PostgreSQL Database Setup

### 1.1 Install PostgreSQL (if not already installed)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (using Homebrew)
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

### 1.2 Set up PostgreSQL
```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql

# Create a new user (optional)
CREATE USER studybloom_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE studybloom TO studybloom_user;
\q
```

### 1.3 Run the Database Schema
```bash
# Navigate to backend directory
cd backend/StudyBloom

# Run the PostgreSQL schema
psql -U postgres -f database_schema.sql

# Or if you created a specific user:
psql -U studybloom_user -d studybloom -f database_schema.sql
```

## 🔧 Step 2: Backend Setup

### 2.1 Install Python Dependencies
```bash
# Navigate to backend directory
cd backend/StudyBloom

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configure Environment Variables
```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://postgres:your_password@localhost/studybloom
SECRET_KEY=your_super_secret_key_here
DEBUG=1
OPENAI_API_KEY=your_openai_key_here
STRIPE_SECRET_KEY=your_stripe_key_here
TWILIO_ACCOUNT_SID=your_twilio_sid_here
TWILIO_AUTH_TOKEN=your_twilio_token_here
EOF
```

### 2.3 Set up Database and Sample Data
```bash
# Run the PostgreSQL setup script
python setup_postgres.py

# This will:
# - Create the database if it doesn't exist
# - Run the schema SQL
# - Create sample data for testing
```

### 2.4 Start the Backend Server
```bash
# Start Flask server
python run.py
```

Your backend will be running at: `http://localhost:5000`

## 🌐 Step 3: Frontend Integration

### 3.1 Configure Frontend Environment
Create a `.env` file in your frontend project:
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENVIRONMENT=development
```

### 3.2 Test Backend Connection
```bash
# Test if backend is running
curl http://localhost:5000/ai/status

# Test login with sample user
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  -c cookies.txt

# Test API endpoints
curl -X GET http://localhost:5000/api/goals -b cookies.txt
curl -X GET http://localhost:5000/api/streaks -b cookies.txt
```

### 3.3 Frontend API Integration Examples

#### Authentication
```javascript
// Login function
const loginUser = async (username, password) => {
  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ username, password })
    });
    
    if (response.ok) {
      const data = await response.json();
      return { success: true, data };
    } else {
      return { success: false, error: 'Login failed' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Goals Management
```javascript
// Get user goals
const fetchGoals = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/goals', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const goals = await response.json();
      return { success: true, data: goals };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// Create new goal
const createGoal = async (goalData) => {
  try {
    const response = await fetch('http://localhost:5000/api/goals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(goalData)
    });
    
    if (response.ok) {
      const goal = await response.json();
      return { success: true, data: goal };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Streak Tracking
```javascript
// Get current streak
const fetchStreak = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/streaks', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const streak = await response.json();
      return { success: true, data: streak };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// Update streak (when user completes task)
const updateStreak = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/streaks/update', {
      method: 'POST',
      credentials: 'include'
    });
    
    if (response.ok) {
      const result = await response.json();
      return { success: true, data: result };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Study Sessions
```javascript
// Start study session
const startStudySession = async (sessionData) => {
  try {
    const response = await fetch('http://localhost:5000/api/study-sessions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(sessionData)
    });
    
    if (response.ok) {
      const session = await response.json();
      return { success: true, data: session };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// End study session
const endStudySession = async (sessionId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/study-sessions/${sessionId}/end`, {
      method: 'PUT',
      credentials: 'include'
    });
    
    if (response.ok) {
      const result = await response.json();
      return { success: true, data: result };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Rewards System
```javascript
// Get available rewards
const fetchRewards = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/rewards/available', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const rewards = await response.json();
      return { success: true, data: rewards };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// Check reward eligibility
const checkRewardEligibility = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/rewards/check-eligibility', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const eligibility = await response.json();
      return { success: true, data: eligibility };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

#### Study Groups
```javascript
// Check group eligibility
const checkGroupEligibility = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/groups/check-eligibility', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const eligibility = await response.json();
      return { success: true, data: eligibility };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};

// Get available groups
const fetchAvailableGroups = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/groups/available', {
      method: 'GET',
      credentials: 'include'
    });
    
    if (response.ok) {
      const groups = await response.json();
      return { success: true, data: groups };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
};
```

## 🧪 Step 4: Testing the Integration

### 4.1 Test Authentication Flow
```javascript
// Test login
const testLogin = async () => {
  const result = await loginUser('testuser', 'password123');
  console.log('Login result:', result);
  
  if (result.success) {
    // Test fetching user data
    const goals = await fetchGoals();
    console.log('Goals:', goals);
    
    const streak = await fetchStreak();
    console.log('Streak:', streak);
  }
};
```

### 4.2 Test Complete User Journey
```javascript
const testUserJourney = async () => {
  // 1. Login
  const login = await loginUser('testuser', 'password123');
  if (!login.success) return;
  
  // 2. Create a new goal
  const newGoal = await createGoal({
    title: 'Learn React',
    description: 'Master React fundamentals',
    deadline: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    target_minutes: 600
  });
  
  // 3. Start a study session
  const session = await startStudySession({
    subject: 'React',
    notes: 'Learning React hooks'
  });
  
  // 4. End study session after some time
  setTimeout(async () => {
    const endSession = await endStudySession(session.data.id);
    console.log('Session ended:', endSession);
    
    // 5. Check updated streak
    const updatedStreak = await fetchStreak();
    console.log('Updated streak:', updatedStreak);
  }, 5000);
};
```

## 🚨 Troubleshooting

### Common Issues

#### 1. CORS Errors
```javascript
// Ensure your frontend requests include:
credentials: 'include'
```

#### 2. Database Connection Issues
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check database connection
psql -U postgres -d studybloom -c "SELECT version();"
```

#### 3. Session Issues
```javascript
// Ensure cookies are being sent
// Backend uses Flask-Login for session management
// Frontend must include credentials: 'include' in all requests
```

#### 4. Port Conflicts
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill process if needed
kill -9 <PID>
```

## 📊 API Endpoints Summary

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Goals & Tasks
- `GET /api/goals` - Get user goals
- `POST /api/goals` - Create goal
- `PUT /api/goals/{id}` - Update goal
- `DELETE /api/goals/{id}` - Delete goal
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Streaks & Analytics
- `GET /api/streaks` - Get current streak
- `POST /api/streaks/update` - Update streak
- `GET /api/streaks/analytics` - Get analytics
- `GET /api/study-sessions` - Get study sessions
- `POST /api/study-sessions` - Start session
- `PUT /api/study-sessions/{id}/end` - End session

### Rewards & Groups
- `GET /api/rewards/available` - Get rewards
- `GET /api/rewards/check-eligibility` - Check eligibility
- `GET /api/groups/available` - Get groups
- `GET /api/groups/check-eligibility` - Check group eligibility

## 🎯 Next Steps

1. **Test all API endpoints** with your frontend
2. **Implement error handling** for network issues
3. **Add loading states** for better UX
4. **Implement real-time features** if needed
5. **Add offline support** if required
6. **Set up production deployment**

## 📞 Support

If you encounter any issues:
1. Check the browser console for errors
2. Check the backend logs for server errors
3. Verify database connection and schema
4. Test API endpoints with curl or Postman
5. Ensure CORS is properly configured

Your StudyBloom backend is now fully functional with PostgreSQL and ready to power your beautiful frontend! 🌸✨ 