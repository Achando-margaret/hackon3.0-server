#!/usr/bin/env python3
"""
Simple database setup script for StudyBloom with PostgreSQL
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

def setup_database():
    """Set up the database tables"""
    app = create_app()
    
    with app.app_context():
        print("🗄️  Creating database tables...")
        db.create_all()
        print("✅ All tables created successfully!")
        
        # Create sample data
        create_sample_data()
        
def create_sample_data():
    """Create sample data for testing"""
    print("📝 Creating sample data...")
    
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
    
    print("✅ Sample data creation completed!")

if __name__ == '__main__':
    setup_database()
    print("\n🎉 Database setup completed!")
    print("\nYou can now run the application with:")
    print("python run.py") 