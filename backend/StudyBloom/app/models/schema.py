from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_picture = db.Column(db.String(255))
    timezone = db.Column(db.String(50), default='UTC')
    daily_goal_minutes = db.Column(db.Integer, default=60)
    streak_goal_days = db.Column(db.Integer, default=7)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    reminders = db.relationship('Reminder', backref='user', lazy=True)
    streaks = db.relationship('Streak', backref='user', lazy=True)
    study_sessions = db.relationship('StudySession', backref='user', lazy=True)
    rewards = db.relationship('Reward', backref='user', lazy=True)
    group_memberships = db.relationship('GroupMembership', backref='user', lazy=True)
    ai_interactions = db.relationship('AIInteraction', backref='user', lazy=True)
    settings = db.relationship('UserSettings', backref='user', lazy=True, uselist=False)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    created_groups = db.relationship('Group', backref='creator', lazy=True, foreign_keys='Group.creator_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
    stripe_subscription_id = db.Column(db.String(100))
    stripe_customer_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    priority = db.Column(db.String(10), default='medium')
    deadline = db.Column(db.DateTime)
    target_minutes = db.Column(db.Integer)
    completed_minutes = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    completion_percentage = db.Column(db.Integer, default=0)
    color = db.Column(db.String(7), default='#3B82F6')
    icon = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='goal', lazy=True)
    study_sessions = db.relationship('StudySession', backref='goal', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id', ondelete='CASCADE'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(10), default='medium')
    due_date = db.Column(db.DateTime)
    estimated_minutes = db.Column(db.Integer)
    actual_minutes = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime)
    reminder_sent = db.Column(db.Boolean, default=False)
    position = db.Column(db.Integer, default=0)
    tags = db.Column(db.ARRAY(db.String(255)), default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reminders = db.relationship('Reminder', backref='task', lazy=True)

class Reminder(db.Model):
    __tablename__ = 'reminders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'))
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    notification_type = db.Column(db.String(20), default='push')
    retry_count = db.Column(db.Integer, default=0)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Streak(db.Model):
    __tablename__ = 'streaks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.Date)
    total_days_active = db.Column(db.Integer, default=0)
    streak_type = db.Column(db.String(20), default='daily')
    goal_streak_days = db.Column(db.Integer, default=7)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class StudySession(db.Model):
    __tablename__ = 'study_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id', ondelete='SET NULL'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    subject = db.Column(db.String(100))
    notes = db.Column(db.Text)
    focus_score = db.Column(db.Integer)
    productivity_score = db.Column(db.Integer)
    session_type = db.Column(db.String(20), default='individual')
    tags = db.Column(db.ARRAY(db.String(255)), default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Reward(db.Model):
    __tablename__ = 'rewards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reward_type = db.Column(db.String(50), nullable=False)
    reward_value = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text, nullable=False)
    unlocked_at = db.Column(db.DateTime, nullable=False)
    expires_at = db.Column(db.DateTime)
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)
    metadata = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    max_members = db.Column(db.Integer, default=10)
    current_members = db.Column(db.Integer, default=1)
    is_public = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    category = db.Column(db.String(50))
    meeting_schedule = db.Column(db.JSON, default={})
    required_streak_days = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = db.relationship('GroupMembership', backref='group', lazy=True)

class GroupMembership(db.Model):
    __tablename__ = 'group_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(20), default='member')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')

class AIInteraction(db.Model):
    __tablename__ = 'ai_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    session_id = db.Column(db.String(100))
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text)
    interaction_type = db.Column(db.String(50))
    model_used = db.Column(db.String(50), default='gpt-4')
    tokens_used = db.Column(db.Integer)
    response_time_ms = db.Column(db.Integer)
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text)
    metadata = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    daily_reminder_enabled = db.Column(db.Boolean, default=True)
    daily_reminder_time = db.Column(db.Time, default=datetime.strptime('09:00:00', '%H:%M:%S').time())
    weekly_report_enabled = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    theme = db.Column(db.String(20), default='light')
    language = db.Column(db.String(10), default='en')
    focus_mode_enabled = db.Column(db.Boolean, default=True)
    break_reminders_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')
    is_read = db.Column(db.Boolean, default=False)
    related_entity_type = db.Column(db.String(50))
    related_entity_id = db.Column(db.Integer)
    action_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)