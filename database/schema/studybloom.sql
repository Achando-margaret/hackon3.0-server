-- StudyBloom Database Schema


CREATE DATABASE studybloom;
\c studybloom;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    profile_picture VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'UTC',
    daily_goal_minutes INTEGER DEFAULT 60,
    streak_goal_days INTEGER DEFAULT 7,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- 2. Subscriptions Table
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_name VARCHAR(50) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'active' 
        CHECK (status IN ('active', 'canceled', 'expired', 'pending')),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending'
        CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    stripe_subscription_id VARCHAR(100),
    stripe_customer_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Goals Table
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    priority VARCHAR(10) DEFAULT 'medium'
        CHECK (priority IN ('low', 'medium', 'high')),
    deadline TIMESTAMP,
    target_minutes INTEGER,
    completed_minutes INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    completion_percentage INTEGER DEFAULT 0,
    color VARCHAR(7) DEFAULT '#3B82F6',
    icon VARCHAR(50),
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tasks Table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal_id INTEGER REFERENCES goals(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending'
        CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    priority VARCHAR(10) DEFAULT 'medium'
        CHECK (priority IN ('low', 'medium', 'high')),
    due_date TIMESTAMP,
    estimated_minutes INTEGER,
    actual_minutes INTEGER,
    completed_at TIMESTAMP,
    reminder_sent BOOLEAN DEFAULT FALSE,
    position INTEGER DEFAULT 0,
    tags VARCHAR(255)[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Reminders Table
CREATE TABLE reminders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    reminder_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
        CHECK (status IN ('pending', 'sent', 'canceled', 'failed')),
    notification_type VARCHAR(20) DEFAULT 'push'
        CHECK (notification_type IN ('email', 'push', 'sms')),
    retry_count INTEGER DEFAULT 0,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Streaks Table
CREATE TABLE streaks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_activity_date DATE,
    total_days_active INTEGER DEFAULT 0,
    streak_type VARCHAR(20) DEFAULT 'daily'
        CHECK (streak_type IN ('daily', 'weekly', 'monthly')),
    goal_streak_days INTEGER DEFAULT 7,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, streak_type)
);

-- 7. Study Sessions Table
CREATE TABLE study_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal_id INTEGER REFERENCES goals(id) ON DELETE SET NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_minutes INTEGER,
    subject VARCHAR(100),
    notes TEXT,
    focus_score INTEGER CHECK (focus_score >= 1 AND focus_score <= 10),
    productivity_score INTEGER CHECK (productivity_score >= 1 AND productivity_score <= 10),
    session_type VARCHAR(20) DEFAULT 'individual'
        CHECK (session_type IN ('individual', 'group', 'coaching')),
    tags VARCHAR(255)[] DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Rewards Table
CREATE TABLE rewards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reward_type VARCHAR(50) NOT NULL
        CHECK (reward_type IN ('discount', 'badge', 'feature', 'content')),
    reward_value DECIMAL(10,2),
    description TEXT NOT NULL,
    unlocked_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,
    is_used BOOLEAN DEFAULT FALSE,
    used_at TIMESTAMP,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Groups Table
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    creator_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    max_members INTEGER DEFAULT 10,
    current_members INTEGER DEFAULT 1,
    is_public BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    category VARCHAR(50),
    meeting_schedule JSONB DEFAULT '{}',
    required_streak_days INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Group Memberships Table
CREATE TABLE group_memberships (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member'
        CHECK (role IN ('member', 'moderator', 'admin')),
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    left_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
        CHECK (status IN ('active', 'inactive', 'banned', 'pending')),
    UNIQUE(user_id, group_id)
);

-- 11. AI Interactions Table
CREATE TABLE ai_interactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    input_text TEXT NOT NULL,
    output_text TEXT,
    interaction_type VARCHAR(50)
        CHECK (interaction_type IN ('question', 'explanation', 'feedback', 'suggestion')),
    model_used VARCHAR(50) DEFAULT 'gpt-4',
    tokens_used INTEGER,
    response_time_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. User Settings Table
CREATE TABLE user_settings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    daily_reminder_enabled BOOLEAN DEFAULT TRUE,
    daily_reminder_time TIME DEFAULT '09:00:00',
    weekly_report_enabled BOOLEAN DEFAULT TRUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    sms_notifications BOOLEAN DEFAULT FALSE,
    theme VARCHAR(20) DEFAULT 'light'
        CHECK (theme IN ('light', 'dark', 'auto')),
    language VARCHAR(10) DEFAULT 'en',
    focus_mode_enabled BOOLEAN DEFAULT TRUE,
    break_reminders_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 13. Notifications Table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20) DEFAULT 'info'
        CHECK (type IN ('info', 'warning', 'reminder', 'achievement', 'streak')),
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_type VARCHAR(50),
    related_entity_id INTEGER,
    action_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_completed ON goals(completed);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_goal_id ON tasks(goal_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_reminders_user_id ON reminders(user_id);
CREATE INDEX idx_reminders_task_id ON reminders(task_id);
CREATE INDEX idx_reminders_status ON reminders(status);
CREATE INDEX idx_reminders_time ON reminders(reminder_time);
CREATE INDEX idx_streaks_user_id ON streaks(user_id);
CREATE INDEX idx_study_sessions_user_id ON study_sessions(user_id);
CREATE INDEX idx_study_sessions_goal_id ON study_sessions(goal_id);
CREATE INDEX idx_rewards_user_id ON rewards(user_id);
CREATE INDEX idx_group_memberships_user_id ON group_memberships(user_id);
CREATE INDEX idx_group_memberships_group_id ON group_memberships(group_id);
CREATE INDEX idx_ai_interactions_user_id ON ai_interactions(user_id);
CREATE INDEX idx_ai_interactions_created_at ON ai_interactions(created_at);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_goals_updated_at BEFORE UPDATE ON goals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reminders_updated_at BEFORE UPDATE ON reminders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_streaks_updated_at BEFORE UPDATE ON streaks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_study_sessions_updated_at BEFORE UPDATE ON study_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_groups_updated_at BEFORE UPDATE ON groups
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_settings_updated_at BEFORE UPDATE ON user_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to update streak on task completion
CREATE OR REPLACE FUNCTION update_user_streak()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        -- Update user's streak
        INSERT INTO streaks (user_id, current_streak, longest_streak, last_activity_date, total_days_active)
        VALUES (
            NEW.user_id, 
            1, 
            1, 
            CURRENT_DATE, 
            1
        )
        ON CONFLICT (user_id, streak_type) 
        DO UPDATE SET
            current_streak = CASE 
                WHEN streaks.last_activity_date = CURRENT_DATE - INTERVAL '1 day' 
                THEN streaks.current_streak + 1
                ELSE 1
            END,
            longest_streak = GREATEST(
                streaks.longest_streak,
                CASE 
                    WHEN streaks.last_activity_date = CURRENT_DATE - INTERVAL '1 day' 
                    THEN streaks.current_streak + 1
                    ELSE 1
                END
            ),
            last_activity_date = CURRENT_DATE,
            total_days_active = streaks.total_days_active + 1,
            updated_at = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for task completion streak update
CREATE TRIGGER on_task_completion_streak
    AFTER UPDATE OF status ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_user_streak();

-- Function to update goal progress
CREATE OR REPLACE FUNCTION update_goal_progress()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND OLD.status != 'completed' THEN
        -- Update goal progress
        UPDATE goals 
        SET 
            completed_minutes = completed_minutes + COALESCE(NEW.actual_minutes, 0),
            completion_percentage = CASE 
                WHEN target_minutes > 0 THEN 
                    LEAST(100, ((completed_minutes + COALESCE(NEW.actual_minutes, 0)) * 100 / target_minutes)::INTEGER)
                ELSE 0
            END,
            completed = CASE 
                WHEN target_minutes > 0 AND (completed_minutes + COALESCE(NEW.actual_minutes, 0)) >= target_minutes 
                THEN TRUE 
                ELSE completed 
            END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.goal_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for goal progress update
CREATE TRIGGER on_task_completion_goal
    AFTER UPDATE OF status ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_goal_progress();

-- Insert initial data
INSERT INTO users (username, email, password_hash, first_name, last_name) VALUES
('testuser', 'test@example.com', 'pbkdf2:sha256:260000$...', 'Test', 'User'),
('demo', 'demo@example.com', 'pbkdf2:sha256:260000$...', 'Demo', 'User');

-- Insert sample goals
INSERT INTO goals (user_id, title, description, category, target_minutes) VALUES
(1, 'Learn Python', 'Complete Python programming course', 'Programming', 1200),
(1, 'Read 10 Books', 'Read 10 books this year', 'Reading', 5000),
(2, 'Fitness Journey', 'Get in shape with daily exercise', 'Fitness', 1800);

-- Insert sample tasks
INSERT INTO tasks (user_id, goal_id, title, description, status, estimated_minutes) VALUES
(1, 1, 'Complete Chapter 1', 'Variables and Data Types', 'completed', 120),
(1, 1, 'Complete Chapter 2', 'Control Structures', 'in_progress', 180),
(1, 2, 'Read Atomic Habits', 'Finish first book', 'pending', 600),
(2, 3, '30-minute Run', 'Morning run', 'completed', 30);

-- Insert sample streaks
INSERT INTO streaks (user_id, current_streak, longest_streak, last_activity_date, total_days_active) VALUES
(1, 5, 10, CURRENT_DATE - INTERVAL '0 days', 15),
(2, 3, 7, CURRENT_DATE - INTERVAL '1 day', 10);

-- Insert sample study sessions
INSERT INTO study_sessions (user_id, goal_id, start_time, end_time, duration_minutes, subject) VALUES
(1, 1, CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP - INTERVAL '1 hour', 60, 'Python'),
(1, 1, CURRENT_TIMESTAMP - INTERVAL '4 hours', CURRENT_TIMESTAMP - INTERVAL '3 hours', 60, 'Python'),
(2, 3, CURRENT_TIMESTAMP - INTERVAL '3 hours', CURRENT_TIMESTAMP - INTERVAL '2.5 hours', 30, 'Running');

-- Create views for common queries
CREATE VIEW user_progress AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(DISTINCT g.id) as total_goals,
    COUNT(DISTINCT CASE WHEN g.completed THEN g.id END) as completed_goals,
    COUNT(DISTINCT t.id) as total_tasks,
    COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) as completed_tasks,
    COALESCE(SUM(s.duration_minutes), 0) as total_study_minutes,
    st.current_streak,
    st.longest_streak,
    st.total_days_active
FROM users u
LEFT JOIN goals g ON u.id = g.user_id
LEFT JOIN tasks t ON u.id = t.user_id
LEFT JOIN study_sessions s ON u.id = s.user_id
LEFT JOIN streaks st ON u.id = st.user_id AND st.streak_type = 'daily'
GROUP BY u.id, u.username, st.current_streak, st.longest_streak, st.total_days_active;

CREATE VIEW upcoming_tasks AS
SELECT 
    t.*,
    u.username,
    g.title as goal_title,
    CASE 
        WHEN t.due_date < CURRENT_TIMESTAMP THEN 'overdue'
        WHEN t.due_date < CURRENT_TIMESTAMP + INTERVAL '1 day' THEN 'due_today'
        WHEN t.due_date < CURRENT_TIMESTAMP + INTERVAL '3 days' THEN 'due_soon'
        ELSE 'future'
    END as urgency
FROM tasks t
JOIN users u ON t.user_id = u.id
LEFT JOIN goals g ON t.goal_id = g.id
WHERE t.status IN ('pending', 'in_progress')
ORDER BY t.due_date ASC;

CREATE VIEW daily_activity AS
SELECT 
    u.id as user_id,
    u.username,
    DATE(s.start_time) as activity_date,
    COUNT(DISTINCT s.id) as session_count,
    SUM(s.duration_minutes) as total_minutes,
    COUNT(DISTINCT t.id) as task_count,
    COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) as completed_tasks
FROM users u
LEFT JOIN study_sessions s ON u.id = s.user_id AND DATE(s.start_time) = CURRENT_DATE
LEFT JOIN tasks t ON u.id = t.user_id AND (t.completed_at IS NULL OR DATE(t.completed_at) = CURRENT_DATE)
GROUP BY u.id, u.username, DATE(s.start_time);

-- Grant permissions (adjust based on your database user)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO studybloom_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO studybloom_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO studybloom_user;

COMMENT ON DATABASE studybloom IS 'StudyBloom learning platform database';
COMMENT ON TABLE users IS 'Stores user account information';
COMMENT ON TABLE goals IS 'Stores user learning goals and objectives';
COMMENT ON TABLE tasks IS 'Stores individual tasks associated with goals';
COMMENT ON TABLE streaks IS 'Tracks user activity streaks for motivation';
COMMENT ON TABLE study_sessions IS 'Logs study sessions with timing and metrics';