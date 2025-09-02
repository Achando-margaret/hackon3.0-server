#!/usr/bin/env python3
"""
PostgreSQL Database Setup Script for StudyBloom
This script works with the comprehensive PostgreSQL schema provided
"""

import os
import sys
import psycopg2
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_database():
    """Create the studybloom database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'studybloom'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE studybloom")
            print("✅ Created studybloom database")
        else:
            print("✅ Database studybloom already exists")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    
    return True

def run_schema_sql():
    """Run the PostgreSQL schema SQL"""
    try:
        # Connect to studybloom database
        conn = psycopg2.connect(
            host="localhost",
            database="studybloom",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read and execute the schema SQL
        schema_file = "database_schema.sql"
        if os.path.exists(schema_file):
            with open(schema_file, 'r') as f:
                sql = f.read()
                cursor.execute(sql)
            print("✅ Schema executed successfully")
        else:
            print("⚠️  Schema file not found. Please run the SQL manually.")
            return False
            
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error executing schema: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="studybloom",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )
        cursor = conn.cursor()
        
        # Check if sample data already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'testuser'")
        if cursor.fetchone()[0] > 0:
            print("✅ Sample data already exists")
            cursor.close()
            conn.close()
            return True
        
        # Create sample user
        password_hash = generate_password_hash('password123')
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, ('testuser', 'test@example.com', password_hash, 'Test', 'User'))
        
        user_id = cursor.fetchone()[0]
        print(f"✅ Created test user: testuser (password: password123)")
        
        # Create sample subscription
        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan_name, start_date, end_date, status, amount, currency)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, 'monthly', datetime.utcnow(), datetime.utcnow() + timedelta(days=30), 'active', 9.99, 'USD'))
        print("✅ Created sample subscription")
        
        # Create sample goal
        cursor.execute("""
            INSERT INTO goals (user_id, title, description, category, target_minutes, priority)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (user_id, 'Learn Python Programming', 'Complete Python programming course', 'Programming', 1200, 'high'))
        
        goal_id = cursor.fetchone()[0]
        print("✅ Created sample goal")
        
        # Create sample tasks
        tasks = [
            ('Complete Chapter 1', 'Variables and Data Types', 'completed', 120),
            ('Complete Chapter 2', 'Control Structures', 'in_progress', 180),
            ('Build First Project', 'Create a simple calculator', 'pending', 240)
        ]
        
        for title, description, status, minutes in tasks:
            cursor.execute("""
                INSERT INTO tasks (user_id, goal_id, title, description, status, estimated_minutes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, goal_id, title, description, status, minutes))
        print("✅ Created sample tasks")
        
        # Create sample streak
        cursor.execute("""
            INSERT INTO streaks (user_id, current_streak, longest_streak, last_activity_date, total_days_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, 5, 10, datetime.utcnow().date(), 15))
        print("✅ Created sample streak")
        
        # Create sample study sessions
        sessions = [
            (datetime.utcnow() - timedelta(hours=2), datetime.utcnow() - timedelta(hours=1), 60, 'Python'),
            (datetime.utcnow() - timedelta(hours=4), datetime.utcnow() - timedelta(hours=3), 60, 'Python')
        ]
        
        for start_time, end_time, duration, subject in sessions:
            cursor.execute("""
                INSERT INTO study_sessions (user_id, goal_id, start_time, end_time, duration_minutes, subject)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, goal_id, start_time, end_time, duration, subject))
        print("✅ Created sample study sessions")
        
        # Create sample reward
        cursor.execute("""
            INSERT INTO rewards (user_id, reward_type, reward_value, description, unlocked_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, 'discount', 10.0, '5-day streak discount: 10% off next subscription', datetime.utcnow()))
        print("✅ Created sample reward")
        
        # Create user settings
        cursor.execute("""
            INSERT INTO user_settings (user_id, daily_reminder_enabled, theme, language)
            VALUES (%s, %s, %s, %s)
        """, (user_id, True, 'light', 'en'))
        print("✅ Created user settings")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Sample data creation completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="studybloom",
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Database connection successful: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up StudyBloom PostgreSQL Database...")
    
    # Set environment variables if not set
    if not os.getenv("DB_USER"):
        os.environ["DB_USER"] = "postgres"
    if not os.getenv("DB_PASSWORD"):
        os.environ["DB_PASSWORD"] = ""
    
    # Step 1: Create database
    if not create_database():
        return
    
    # Step 2: Test connection
    if not test_connection():
        return
    
    # Step 3: Run schema (if schema file exists)
    if os.path.exists("database_schema.sql"):
        if not run_schema_sql():
            return
    else:
        print("⚠️  Please run the PostgreSQL schema SQL manually")
        print("   Copy the schema from your message and run it in psql")
    
    # Step 4: Create sample data
    if not create_sample_data():
        return
    
    print("\n🎉 Database setup completed!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with:")
    print("   DATABASE_URL=postgresql://postgres:password@localhost/studybloom")
    print("2. Start the backend server:")
    print("   python run.py")
    print("3. Test the API endpoints")

if __name__ == '__main__':
    main() 