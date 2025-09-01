from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.schema import db, Streak, StudySession
from datetime import datetime, date, timedelta

streaks_bp = Blueprint('streaks', __name__)

@streaks_bp.route('/api/streaks', methods=['GET'])
@login_required
def get_streak():
    """Get current user's streak information"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak:
        # Create streak record if it doesn't exist
        streak = Streak(user_id=current_user.id)
        db.session.add(streak)
        db.session.commit()
    
    return jsonify({
        'current_streak': streak.current_streak,
        'longest_streak': streak.longest_streak,
        'last_activity_date': streak.last_activity_date.isoformat() if streak.last_activity_date else None,
        'streak_type': streak.streak_type
    })

@streaks_bp.route('/api/streaks/update', methods=['POST'])
@login_required
def update_streak():
    """Update user's streak (called when user completes a task or study session)"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak:
        streak = Streak(user_id=current_user.id)
        db.session.add(streak)
    
    today = date.today()
    
    # Check if user already has activity today
    if streak.last_activity_date == today:
        return jsonify({'message': 'Already updated today', 'current_streak': streak.current_streak})
    
    # Check if this is consecutive day
    if streak.last_activity_date and streak.last_activity_date == today - timedelta(days=1):
        streak.current_streak += 1
    else:
        # Reset streak if not consecutive
        streak.current_streak = 1
    
    # Update longest streak if current is longer
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak
    
    streak.last_activity_date = today
    db.session.commit()
    
    return jsonify({
        'current_streak': streak.current_streak,
        'longest_streak': streak.longest_streak,
        'message': 'Streak updated successfully'
    })

@streaks_bp.route('/api/streaks/reset', methods=['POST'])
@login_required
def reset_streak():
    """Reset user's streak (for testing or manual reset)"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if streak:
        streak.current_streak = 0
        streak.last_activity_date = None
        db.session.commit()
    
    return jsonify({'message': 'Streak reset successfully', 'current_streak': 0})

@streaks_bp.route('/api/study-sessions', methods=['GET'])
@login_required
def get_study_sessions():
    """Get user's study sessions"""
    sessions = StudySession.query.filter_by(user_id=current_user.id).order_by(StudySession.start_time.desc()).all()
    
    return jsonify([{
        'id': session.id,
        'start_time': session.start_time.isoformat(),
        'end_time': session.end_time.isoformat() if session.end_time else None,
        'duration_minutes': session.duration_minutes,
        'subject': session.subject,
        'notes': session.notes,
        'created_at': session.created_at.isoformat()
    } for session in sessions])

@streaks_bp.route('/api/study-sessions', methods=['POST'])
@login_required
def create_study_session():
    """Start a new study session"""
    data = request.json
    new_session = StudySession(
        user_id=current_user.id,
        start_time=datetime.utcnow(),
        subject=data.get('subject', ''),
        notes=data.get('notes', '')
    )
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({
        'id': new_session.id,
        'start_time': new_session.start_time.isoformat(),
        'subject': new_session.subject,
        'notes': new_session.notes
    }), 201

@streaks_bp.route('/api/study-sessions/<int:session_id>/end', methods=['PUT'])
@login_required
def end_study_session(session_id):
    """End a study session"""
    session = StudySession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    
    if session.end_time:
        return jsonify({'message': 'Session already ended'}), 400
    
    session.end_time = datetime.utcnow()
    session.duration_minutes = int((session.end_time - session.start_time).total_seconds() / 60)
    
    db.session.commit()
    
    # Update streak after study session
    from app.streaks.routes import update_streak
    update_streak()
    
    return jsonify({
        'id': session.id,
        'duration_minutes': session.duration_minutes,
        'message': 'Study session ended successfully'
    })

@streaks_bp.route('/api/streaks/analytics', methods=['GET'])
@login_required
def get_streak_analytics():
    """Get streak analytics and statistics"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak:
        return jsonify({
            'current_streak': 0,
            'longest_streak': 0,
            'total_study_sessions': 0,
            'total_study_time': 0,
            'average_session_length': 0
        })
    
    # Get study session statistics
    sessions = StudySession.query.filter_by(user_id=current_user.id).all()
    total_sessions = len(sessions)
    total_time = sum(s.duration_minutes or 0 for s in sessions)
    avg_session_length = total_time / total_sessions if total_sessions > 0 else 0
    
    return jsonify({
        'current_streak': streak.current_streak,
        'longest_streak': streak.longest_streak,
        'total_study_sessions': total_sessions,
        'total_study_time': total_time,
        'average_session_length': round(avg_session_length, 2),
        'can_join_groups': streak.current_streak >= 20
    }) 