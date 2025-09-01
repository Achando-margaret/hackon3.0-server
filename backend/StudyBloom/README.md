# StudyBloom Backend

## 🌸 Overview
StudyBloom is a comprehensive AI-powered learning platform that combines subscription management, streak tracking, rewards, and collaborative features to motivate students and learners. The backend is built with Flask and provides a robust API for the frontend application.

## ✨ Features

### 🎯 Core Learning Features
- **Goal & Task Management** - Create, track, and complete learning goals and tasks
- **Study Sessions** - Track study time and session analytics
- **AI Integration** - AI-powered study assistance and personalized recommendations
- **Progress Tracking** - Comprehensive analytics and progress visualization

### 🔥 Motivation & Gamification
- **Streak System** - Daily activity tracking with visual streak counters
- **Rewards Engine** - Unlock discounts and features based on achievements
- **Achievement Badges** - Earn badges for consistency and milestones

### ⏰ Smart Reminders
- **Scheduled Reminders** - Set study reminders with SMS/email notifications
- **Task-based Reminders** - Automatic reminders for upcoming deadlines
- **Recurring Reminders** - Daily/weekly study schedule reminders

### 👥 Collaboration
- **Study Groups** - Join collaborative study groups (unlocked after 20-day streak)
- **Group Management** - Create, manage, and participate in study communities
- **Progress Sharing** - Share achievements and motivate group members

### 💳 Subscription Management
- **Multiple Plans** - Weekly, monthly, and semester subscription options
- **Payment Integration** - Stripe/PayPal integration for secure payments
- **Discount Rewards** - Apply earned discounts to subscription renewals

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 8.0+ or PostgreSQL 12+
- Redis (for background tasks)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudyBloom
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

4. **Set up environment variables**
   ```bash
   cp .env.template .env
   # Edit .env with your configuration
   ```

5. **Configure database**
   ```bash
   # Update DATABASE_URL in .env
   DATABASE_URL=mysql+pymysql://username:password@localhost/study_bloom
   ```

6. **Run database migrations**
   ```bash
   python migrations.py
   ```

7. **Start the application**
   ```bash
   python run.py
   ```

8. **Access the application**
   - Web Interface: http://localhost:5000
   - API Documentation: See `API_DOCUMENTATION.md`

## 📁 Project Structure

```
StudyBloom/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── auth/                    # Authentication routes
│   │   └── routes.py
│   ├── subscription/            # Subscription management
│   │   └── routes.py
│   ├── ai/                      # AI integration
│   │   └── routes.py
│   ├── tasks/                   # Goals & tasks management
│   │   └── routes.py
│   ├── streaks/                 # Streak tracking
│   │   └── routes.py
│   ├── reminders/               # Reminder system
│   │   └── routes.py
│   ├── rewards/                 # Rewards & discounts
│   │   └── routes.py
│   ├── groups/                  # Study groups
│   │   └── routes.py
│   ├── models/                  # Database models
│   │   └── schema.py
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JS, images
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── migrations.py                # Database setup script
├── requirements.txt             # Python dependencies
├── API_DOCUMENTATION.md         # Complete API documentation
└── README.md                    # This file
```

## 🗄️ Database Schema

### Core Tables
- **users** - User accounts and profiles
- **subscriptions** - Subscription plans and status
- **goals** - Learning goals with deadlines
- **tasks** - Individual tasks within goals
- **reminders** - Scheduled reminders and notifications
- **streaks** - Daily activity tracking
- **study_sessions** - Study session logs and analytics
- **rewards** - Unlocked rewards and discounts
- **groups** - Study groups
- **group_memberships** - Group membership relationships
- **ai_interactions** - AI conversation logs

## 🔧 Configuration

### Environment Variables
```env
# Flask Configuration
SECRET_KEY=your_secret_key_here
DEBUG=1

# Database
DATABASE_URL=mysql+pymysql://username:password@localhost/study_bloom

# AI Integration
OPENAI_API_KEY=your_openai_api_key

# Payment Processing
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

# SMS Notifications (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone

# Background Tasks
REDIS_URL=redis://localhost:6379

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```

## 📊 API Endpoints

### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### Goals & Tasks
- `GET /api/goals` - Get user goals
- `POST /api/goals` - Create new goal
- `PUT /api/goals/{id}` - Update goal
- `DELETE /api/goals/{id}` - Delete goal
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Streaks & Analytics
- `GET /api/streaks` - Get current streak
- `POST /api/streaks/update` - Update streak
- `GET /api/streaks/analytics` - Get streak analytics
- `GET /api/study-sessions` - Get study sessions
- `POST /api/study-sessions` - Start study session
- `PUT /api/study-sessions/{id}/end` - End study session

### Reminders
- `GET /api/reminders` - Get user reminders
- `POST /api/reminders` - Create reminder
- `POST /api/reminders/schedule` - Schedule recurring reminder
- `GET /api/reminders/upcoming` - Get upcoming reminders

### Rewards
- `GET /api/rewards` - Get user rewards
- `GET /api/rewards/available` - Get available rewards
- `POST /api/rewards/unlock` - Unlock reward
- `POST /api/rewards/{id}/redeem` - Redeem reward
- `GET /api/rewards/statistics` - Get reward statistics

### Study Groups
- `GET /api/groups` - Get user's groups
- `GET /api/groups/available` - Get available groups
- `POST /api/groups` - Create group
- `POST /api/groups/{id}/join` - Join group
- `GET /api/groups/check-eligibility` - Check group eligibility

## 🎮 Feature Workflows

### Streak System
1. User completes a task or study session
2. System calls `/api/streaks/update`
3. Streak counter increments if consecutive day
4. Rewards automatically unlocked at milestones (7, 14, 20 days)
5. Group access unlocked at 20-day streak

### Reward System
1. User achieves streak milestones
2. System automatically unlocks rewards
3. User can view available rewards at `/api/rewards/available`
4. User redeems rewards for subscription discounts
5. Discounts applied during subscription renewal

### Study Groups
1. User builds 20-day streak
2. Group feature unlocked automatically
3. User can create or join study groups
4. Group members can share progress and motivate each other
5. Group admins can manage group settings

## 🧪 Testing

### Sample Data
The migration script creates sample data for testing:
- Test user: `testuser` / `password123`
- Sample goals, tasks, and study sessions
- Sample streak and rewards

### API Testing
```bash
# Test authentication
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Test goals API
curl -X GET http://localhost:5000/api/goals \
  -H "Cookie: session=your_session_cookie"
```

## 🚀 Deployment

### Production Setup
1. **Use Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

2. **Set up Redis for background tasks**
   ```bash
   # Install Redis
   sudo apt-get install redis-server
   
   # Start Celery worker
   celery -A app.celery worker --loglevel=info
   ```

3. **Configure reverse proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Environment Variables for Production
```env
DEBUG=0
SECRET_KEY=your_very_secure_secret_key
DATABASE_URL=mysql+pymysql://prod_user:prod_password@prod_host/study_bloom_prod
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: See `API_DOCUMENTATION.md` for complete API reference
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions for questions and ideas

## 🔮 Roadmap

- [ ] Real-time chat in study groups
- [ ] Advanced AI tutoring features
- [ ] Mobile app integration
- [ ] Social learning features
- [ ] Advanced analytics dashboard
- [ ] Integration with learning management systems