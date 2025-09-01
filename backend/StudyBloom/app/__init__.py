from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend integration
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], supports_credentials=True)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.schema import User
        return User.query.get(int(user_id))

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.subscription.routes import subscription_bp
    from app.ai.routes import ai_bp
    from app.tasks.routes import tasks_bp
    from app.streaks.routes import streaks_bp
    from app.reminders.routes import reminders_bp
    from app.rewards.routes import rewards_bp
    from app.groups.routes import groups_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(streaks_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(rewards_bp)
    app.register_blueprint(groups_bp)

    return app