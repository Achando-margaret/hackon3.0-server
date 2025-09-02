# StudyBloom Backend API Documentation

## Overview
StudyBloom is an AI-powered learning platform with subscription management, streak tracking, rewards, and collaborative features. This document outlines all available API endpoints.

## Base URL
```
http://localhost:5000
```

## Authentication
Most endpoints require authentication. Use Flask-Login session-based authentication.

## API Endpoints

### Authentication Endpoints

#### Register User
```
POST /register
```
**Request Body:**
```json
{
  "username": "string",
  "email": "string", 
  "password": "string"
}
```

#### Login User
```
POST /login
```
**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

#### Logout User
```
GET /logout
```

### Goals & Tasks Management

#### Get All Goals
```
GET /api/goals
```
**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete Math Course",
    "description": "Finish all chapters",
    "deadline": "2024-01-15T00:00:00",
    "completed": false,
    "created_at": "2024-01-01T10:00:00"
  }
]
```

#### Create Goal
```
POST /api/goals
```
**Request Body:**
```json
{
  "title": "Complete Math Course",
  "description": "Finish all chapters",
  "deadline": "2024-01-15T00:00:00"
}
```

#### Update Goal
```
PUT /api/goals/{goal_id}
```
**Request Body:**
```json
{
  "title": "Updated Title",
  "completed": true
}
```

#### Delete Goal
```
DELETE /api/goals/{goal_id}
```

#### Get All Tasks
```
GET /api/tasks
```
**Response:**
```json
[
  {
    "id": 1,
    "goal_id": 1,
    "title": "Chapter 1 Quiz",
    "description": "Complete quiz for chapter 1",
    "status": "pending",
    "due_date": "2024-01-10T00:00:00",
    "completed_at": null,
    "created_at": "2024-01-01T10:00:00"
  }
]
```

#### Create Task
```
POST /api/tasks
```
**Request Body:**
```json
{
  "goal_id": 1,
  "title": "Chapter 1 Quiz",
  "description": "Complete quiz for chapter 1",
  "due_date": "2024-01-10T00:00:00"
}
```

#### Update Task
```
PUT /api/tasks/{task_id}
```
**Request Body:**
```json
{
  "status": "completed",
  "title": "Updated Task Title"
}
```

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

### Streak Management

#### Get Current Streak
```
GET /api/streaks
```
**Response:**
```json
{
  "current_streak": 15,
  "longest_streak": 20,
  "last_activity_date": "2024-01-15",
  "streak_type": "daily"
}
```

#### Update Streak
```
POST /api/streaks/update
```
**Response:**
```json
{
  "current_streak": 16,
  "longest_streak": 20,
  "message": "Streak updated successfully"
}
```

#### Reset Streak
```
POST /api/streaks/reset
```

#### Get Streak Analytics
```
GET /api/streaks/analytics
```
**Response:**
```json
{
  "current_streak": 15,
  "longest_streak": 20,
  "total_study_sessions": 45,
  "total_study_time": 1800,
  "average_session_length": 40.0,
  "can_join_groups": false
}
```

### Study Sessions

#### Get Study Sessions
```
GET /api/study-sessions
```

#### Start Study Session
```
POST /api/study-sessions
```
**Request Body:**
```json
{
  "subject": "Mathematics",
  "notes": "Studying calculus"
}
```

#### End Study Session
```
PUT /api/study-sessions/{session_id}/end
```

### Reminders

#### Get All Reminders
```
GET /api/reminders
```

#### Create Reminder
```
POST /api/reminders
```
**Request Body:**
```json
{
  "task_id": 1,
  "title": "Study Reminder",
  "message": "Time to study!",
  "reminder_time": "2024-01-15T14:00:00",
  "notification_type": "sms"
}
```

#### Create Task Reminder
```
POST /api/reminders/task/{task_id}
```

#### Get Upcoming Reminders
```
GET /api/reminders/upcoming
```

#### Schedule Recurring Reminder
```
POST /api/reminders/schedule
```
**Request Body:**
```json
{
  "title": "Daily Study Reminder",
  "message": "Time to study!",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-01-31T00:00:00",
  "time_of_day": "2024-01-01T09:00:00",
  "notification_type": "sms"
}
```

### Rewards System

#### Get All Rewards
```
GET /api/rewards
```

#### Get Available Rewards
```
GET /api/rewards/available
```

#### Check Reward Eligibility
```
GET /api/rewards/check-eligibility
```
**Response:**
```json
{
  "eligible_rewards": [
    {
      "type": "discount",
      "value": 15.0,
      "description": "14-day streak discount: 15% off next subscription",
      "requirement": "14-day study streak"
    }
  ]
}
```

#### Unlock Reward
```
POST /api/rewards/unlock
```
**Request Body:**
```json
{
  "reward_type": "discount",
  "reward_value": 15.0,
  "description": "14-day streak discount"
}
```

#### Redeem Reward
```
POST /api/rewards/{reward_id}/redeem
```

#### Auto Check Rewards
```
POST /api/rewards/auto-check
```

#### Get Reward Statistics
```
GET /api/rewards/statistics
```

### Study Groups (Requires 20-day streak)

#### Get User's Groups
```
GET /api/groups
```

#### Get Available Groups
```
GET /api/groups/available
```

#### Create Group
```
POST /api/groups
```
**Request Body:**
```json
{
  "name": "Math Study Group",
  "description": "Group for studying advanced mathematics",
  "max_members": 10
}
```

#### Join Group
```
POST /api/groups/{group_id}/join
```

#### Leave Group
```
POST /api/groups/{group_id}/leave
```

#### Get Group Members
```
GET /api/groups/{group_id}/members
```

#### Update Group (Admin Only)
```
PUT /api/groups/{group_id}
```

#### Delete Group (Admin Only)
```
DELETE /api/groups/{group_id}
```

#### Check Group Eligibility
```
GET /api/groups/check-eligibility
```

### Subscription Management

#### View Subscriptions
```
GET /subscriptions
```

#### Create Subscription
```
POST /subscriptions/create
```

#### Cancel Subscription
```
POST /subscriptions/cancel/{subscription_id}
```

### AI Integration

#### Generate AI Response
```
POST /ai/generate
```
**Request Body:**
```json
{
  "input": "Help me understand calculus"
}
```

#### Get AI Status
```
GET /ai/status
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

**Error Response Format:**
```json
{
  "message": "Error description",
  "error_code": "ERROR_CODE"
}
```

## Rate Limiting

- API calls are limited to 100 requests per minute per user
- Streak updates are limited to 1 per day per user
- Reminder creation is limited to 10 per day per user

## Webhook Endpoints

### Payment Webhooks
```
POST /webhooks/payment
```

### SMS Delivery Status
```
POST /webhooks/sms-status
```

## Environment Variables

Required environment variables:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=mysql+pymysql://username:password@localhost/study_bloom
OPENAI_API_KEY=your_openai_key
STRIPE_SECRET_KEY=your_stripe_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
REDIS_URL=redis://localhost:6379
```

## Database Schema

The application uses the following main tables:
- `users` - User accounts and profiles
- `subscriptions` - Subscription plans and status
- `goals` - Learning goals
- `tasks` - Individual tasks within goals
- `reminders` - Scheduled reminders
- `streaks` - Daily activity tracking
- `study_sessions` - Study session logs
- `rewards` - Unlocked rewards and discounts
- `groups` - Study groups
- `group_memberships` - Group membership relationships
- `ai_interactions` - AI conversation logs 