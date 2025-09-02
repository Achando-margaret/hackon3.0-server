#!/usr/bin/env python3
"""
Database migration script for StudyBloom
Run this script to create all database tables
"""

import os
import sys
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.schema import (
    User, Subscription, Goal, Task, Reminder, Streak, 
    StudySession, Reward, Group, GroupMembership, AIInteraction
)

def create_tables():
    """Create all database tables"""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ All tables created successfully!")
        
        # Create sample data for testing
        create_sample_data()
        
def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Create a sample user
    if not User.query.filter_by(username='testuser').first():
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        print("✅ Created test user: testuser (password: password123)")
    
    # Create sample subscription
    user = User.query.filter_by(username='testuser').first()
    if user and not Subscription.query.filter_by(user_id=user.id).first():
        subscription = Subscription(
            user_id=user.id,
            plan_name='monthly',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            status='active',
            amount=9.99,
            payment_method='stripe'
        )
        db.session.add(subscription)
        db.session.commit()
        print("✅ Created sample subscription")
    
    # Create sample goal
    if user and not Goal.query.filter_by(user_id=user.id).first():
        goal = Goal(
            user_id=user.id,
            title='Complete Python Course',
            description='Learn Python programming fundamentals',
            deadline=datetime.utcnow() + timedelta(days=30),
            completed=False
        )
        db.session.add(goal)
        db.session.commit()
        print("✅ Created sample goal")
    
    # Create sample tasks
    goal = Goal.query.filter_by(user_id=user.id).first()
    if goal and not Task.query.filter_by(user_id=user.id).first():
        tasks = [
            Task(
                user_id=user.id,
                goal_id=goal.id,
                title='Complete Chapter 1',
                description='Read and complete exercises for Chapter 1',
                status='pending',
                due_date=datetime.utcnow() + timedelta(days=7)
            ),
            Task(
                user_id=user.id,
                goal_id=goal.id,
                title='Take Chapter 1 Quiz',
                description='Complete the quiz for Chapter 1',
                status='pending',
                due_date=datetime.utcnow() + timedelta(days=10)
            )
        ]
        for task in tasks:
            db.session.add(task)
        db.session.commit()
        print("✅ Created sample tasks")
    
    # Create sample streak
    if user and not Streak.query.filter_by(user_id=user.id).first():
        streak = Streak(
            user_id=user.id,
            current_streak=5,
            longest_streak=10,
            last_activity_date=datetime.utcnow().date(),
            streak_type='daily'
        )
        db.session.add(streak)
        db.session.commit()
        print("✅ Created sample streak")
    
    # Create sample study session
    if user and not StudySession.query.filter_by(user_id=user.id).first():
        session = StudySession(
            user_id=user.id,
            start_time=datetime.utcnow() - timedelta(hours=2),
            end_time=datetime.utcnow() - timedelta(hours=1),
            duration_minutes=60,
            subject='Python Programming',
            notes='Studied variables and data types'
        )
        db.session.add(session)
        db.session.commit()
        print("✅ Created sample study session")
    
    # Create sample reminder
    task = Task.query.filter_by(user_id=user.id).first()
    if task and not Reminder.query.filter_by(user_id=user.id).first():
        reminder = Reminder(
            user_id=user.id,
            task_id=task.id,
            title='Study Reminder',
            message='Time to study Python!',
            reminder_time=datetime.utcnow() + timedelta(hours=1),
            status='pending',
            notification_type='sms'
        )
        db.session.add(reminder)
        db.session.commit()
        print("✅ Created sample reminder")
    
    # Create sample reward
    if user and not Reward.query.filter_by(user_id=user.id).first():
        reward = Reward(
            user_id=user.id,
            reward_type='discount',
            reward_value=10.0,
            description='5-day streak discount: 10% off next subscription',
            unlocked_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=30),
            is_used=False
        )
        db.session.add(reward)
        db.session.commit()
        print("✅ Created sample reward")
    
    # Create sample group
    if not Group.query.filter_by(name='Python Learners').first():
        group = Group(
            name='Python Learners',
            description='Group for learning Python programming',
            max_members=15,
            is_active=True
        )
        db.session.add(group)
        db.session.commit()
        print("✅ Created sample group")
    
    # Add user to group if they have 20-day streak
    group = Group.query.filter_by(name='Python Learners').first()
    streak = Streak.query.filter_by(user_id=user.id).first()
    if group and streak and streak.current_streak >= 20:
        membership = GroupMembership(
            user_id=user.id,
            group_id=group.id,
            role='member'
        )
        db.session.add(membership)
        db.session.commit()
        print("✅ Added user to sample group")
    
    print("✅ Sample data creation completed!")

def reset_database():
    """Reset the database (drop all tables and recreate)"""
    app = create_app()
    
    with app.app_context():
        print("⚠️  Dropping all tables...")
        db.drop_all()
        print("✅ All tables dropped!")
        
        print("Creating fresh tables...")
        db.create_all()
        print("✅ Fresh tables created!")
        
        create_sample_data()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        reset_database()
    else:
        create_tables()
    
    print("\n🎉 Database setup completed!")
    print("\nYou can now run the application with:")
    print("python run.py") 