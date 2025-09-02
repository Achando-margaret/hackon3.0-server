from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.schema import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
        else:
            username = request.form['username']
            email = request.form.get('email', '')
            password = request.form['password']
        
        # Validate required fields
        if not username or not password:
            if request.is_json:
                return jsonify({'error': 'Username and password are required'}), 400
            flash('Username and password are required.')
            return redirect(url_for('auth.register'))
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'error': 'Username already exists'}), 409
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        
        # Create new user
        try:
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            
            if request.is_json:
                return jsonify({
                    'message': 'Registration successful!',
                    'user': {
                        'id': new_user.id,
                        'username': new_user.username,
                        'email': new_user.email
                    }
                }), 201
            else:
                flash('Registration successful! Please log in.')
                return redirect(url_for('auth.login'))
                
        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({'error': 'Registration failed. Please try again.'}), 500
            flash('Registration failed. Please try again.')
            return redirect(url_for('auth.register'))
    
    # GET request - show registration form
    if request.is_json:
        return jsonify({'error': 'GET method not allowed for JSON'}), 405
    return render_template('login.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.form['username']
            password = request.form['password']
        
        # Validate required fields
        if not username or not password:
            if request.is_json:
                return jsonify({'error': 'Username and password are required'}), 400
            flash('Username and password are required.')
            return redirect(url_for('auth.login'))
        
        # Find user and verify password
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            
            if request.is_json:
                return jsonify({
                    'message': 'Login successful!',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }), 200
            else:
                return redirect(url_for('dashboard'))
        else:
            if request.is_json:
                return jsonify({'error': 'Invalid username or password'}), 401
            flash('Login failed. Check your username and/or password.')
            return redirect(url_for('auth.login'))
    
    # GET request - show login form
    if request.is_json:
        return jsonify({'error': 'GET method not allowed for JSON'}), 405
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    if request.is_json:
        return jsonify({'message': 'Logout successful'}), 200
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth_bp.route('/api/user/profile', methods=['GET'])
@login_required
def get_user_profile():
    """Get current user profile"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'created_at': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None
    }), 200

@auth_bp.route('/api/user/profile', methods=['PUT'])
@login_required
def update_user_profile():
    """Update current user profile"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    try:
        if 'first_name' in data:
            current_user.first_name = data['first_name']
        if 'last_name' in data:
            current_user.last_name = data['last_name']
        if 'email' in data:
            current_user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'first_name': current_user.first_name,
                'last_name': current_user.last_name
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile'}), 500