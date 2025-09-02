from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.schema import db, Reminder, Task
from datetime import datetime, timedelta

reminders_bp = Blueprint('reminders', __name__)

@reminders_bp.route('/api/reminders', methods=['GET'])
@login_required
def get_reminders():
    """Get all reminders for the current user"""
    reminders = Reminder.query.filter_by(user_id=current_user.id).order_by(Reminder.reminder_time).all()
    
    return jsonify([{
        'id': reminder.id,
        'task_id': reminder.task_id,
        'title': reminder.title,
        'message': reminder.message,
        'reminder_time': reminder.reminder_time.isoformat(),
        'status': reminder.status,
        'notification_type': reminder.notification_type,
        'created_at': reminder.created_at.isoformat()
    } for reminder in reminders])

@reminders_bp.route('/api/reminders', methods=['POST'])
@login_required
def create_reminder():
    """Create a new reminder"""
    data = request.json
    
    new_reminder = Reminder(
        user_id=current_user.id,
        task_id=data.get('task_id'),
        title=data['title'],
        message=data.get('message', ''),
        reminder_time=datetime.fromisoformat(data['reminder_time']),
        notification_type=data.get('notification_type', 'sms')
    )
    
    db.session.add(new_reminder)
    db.session.commit()
    
    return jsonify({
        'id': new_reminder.id,
        'task_id': new_reminder.task_id,
        'title': new_reminder.title,
        'message': new_reminder.message,
        'reminder_time': new_reminder.reminder_time.isoformat(),
        'status': new_reminder.status,
        'notification_type': new_reminder.notification_type,
        'created_at': new_reminder.created_at.isoformat()
    }), 201

@reminders_bp.route('/api/reminders/<int:reminder_id>', methods=['PUT'])
@login_required
def update_reminder(reminder_id):
    """Update a reminder"""
    reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first_or_404()
    data = request.json
    
    reminder.title = data.get('title', reminder.title)
    reminder.message = data.get('message', reminder.message)
    reminder.reminder_time = datetime.fromisoformat(data['reminder_time']) if 'reminder_time' in data else reminder.reminder_time
    reminder.status = data.get('status', reminder.status)
    reminder.notification_type = data.get('notification_type', reminder.notification_type)
    
    db.session.commit()
    return jsonify({'message': 'Reminder updated successfully'})

@reminders_bp.route('/api/reminders/<int:reminder_id>', methods=['DELETE'])
@login_required
def delete_reminder(reminder_id):
    """Delete a reminder"""
    reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first_or_404()
    db.session.delete(reminder)
    db.session.commit()
    return jsonify({'message': 'Reminder deleted successfully'})

@reminders_bp.route('/api/reminders/task/<int:task_id>', methods=['POST'])
@login_required
def create_task_reminder(task_id):
    """Create a reminder for a specific task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.json
    
    # Calculate reminder time (default to 1 hour before due date)
    reminder_time = data.get('reminder_time')
    if not reminder_time:
        reminder_time = task.due_date - timedelta(hours=1)
    else:
        reminder_time = datetime.fromisoformat(reminder_time)
    
    new_reminder = Reminder(
        user_id=current_user.id,
        task_id=task_id,
        title=f"Reminder: {task.title}",
        message=data.get('message', f"Don't forget to complete: {task.title}"),
        reminder_time=reminder_time,
        notification_type=data.get('notification_type', 'sms')
    )
    
    db.session.add(new_reminder)
    db.session.commit()
    
    return jsonify({
        'id': new_reminder.id,
        'task_id': new_reminder.task_id,
        'title': new_reminder.title,
        'message': new_reminder.message,
        'reminder_time': new_reminder.reminder_time.isoformat(),
        'status': new_reminder.status,
        'notification_type': new_reminder.notification_type
    }), 201

@reminders_bp.route('/api/reminders/upcoming', methods=['GET'])
@login_required
def get_upcoming_reminders():
    """Get upcoming reminders (next 24 hours)"""
    now = datetime.utcnow()
    tomorrow = now + timedelta(days=1)
    
    reminders = Reminder.query.filter(
        Reminder.user_id == current_user.id,
        Reminder.reminder_time >= now,
        Reminder.reminder_time <= tomorrow,
        Reminder.status == 'pending'
    ).order_by(Reminder.reminder_time).all()
    
    return jsonify([{
        'id': reminder.id,
        'task_id': reminder.task_id,
        'title': reminder.title,
        'message': reminder.message,
        'reminder_time': reminder.reminder_time.isoformat(),
        'notification_type': reminder.notification_type,
        'time_until': int((reminder.reminder_time - now).total_seconds() / 60)  # minutes until reminder
    } for reminder in reminders])

@reminders_bp.route('/api/reminders/send', methods=['POST'])
@login_required
def send_reminder():
    """Manually send a reminder (for testing or immediate sending)"""
    reminder_id = request.json.get('reminder_id')
    reminder = Reminder.query.filter_by(id=reminder_id, user_id=current_user.id).first_or_404()
    
    # Here you would integrate with SMS/email service
    # For now, we'll just mark it as sent
    reminder.status = 'sent'
    db.session.commit()
    
    return jsonify({
        'message': 'Reminder sent successfully',
        'reminder_id': reminder.id,
        'status': reminder.status
    })

@reminders_bp.route('/api/reminders/schedule', methods=['POST'])
@login_required
def schedule_recurring_reminder():
    """Schedule a recurring reminder (e.g., daily study reminder)"""
    data = request.json
    
    # Create multiple reminders based on schedule
    start_date = datetime.fromisoformat(data['start_date'])
    end_date = datetime.fromisoformat(data['end_date'])
    time_of_day = datetime.fromisoformat(data['time_of_day']).time()
    
    current_date = start_date.date()
    reminders_created = []
    
    while current_date <= end_date.date():
        reminder_time = datetime.combine(current_date, time_of_day)
        
        new_reminder = Reminder(
            user_id=current_user.id,
            title=data['title'],
            message=data.get('message', 'Time to study!'),
            reminder_time=reminder_time,
            notification_type=data.get('notification_type', 'sms')
        )
        
        db.session.add(new_reminder)
        reminders_created.append(new_reminder)
        current_date += timedelta(days=1)
    
    db.session.commit()
    
    return jsonify({
        'message': f'Created {len(reminders_created)} recurring reminders',
        'reminders_count': len(reminders_created)
    }) 