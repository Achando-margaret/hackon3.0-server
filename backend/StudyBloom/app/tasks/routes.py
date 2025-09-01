from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.schema import db, Goal, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/goals', methods=['GET'])
@login_required
def get_goals():
    """Get all goals for the current user"""
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': goal.id,
        'title': goal.title,
        'description': goal.description,
        'deadline': goal.deadline.isoformat(),
        'completed': goal.completed,
        'created_at': goal.created_at.isoformat()
    } for goal in goals])

@tasks_bp.route('/api/goals', methods=['POST'])
@login_required
def create_goal():
    """Create a new goal"""
    data = request.json
    new_goal = Goal(
        user_id=current_user.id,
        title=data['title'],
        description=data.get('description', ''),
        deadline=datetime.fromisoformat(data['deadline'])
    )
    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({
        'id': new_goal.id,
        'title': new_goal.title,
        'description': new_goal.description,
        'deadline': new_goal.deadline.isoformat(),
        'completed': new_goal.completed,
        'created_at': new_goal.created_at.isoformat()
    }), 201

@tasks_bp.route('/api/goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    """Update a goal"""
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    data = request.json
    
    goal.title = data.get('title', goal.title)
    goal.description = data.get('description', goal.description)
    goal.deadline = datetime.fromisoformat(data['deadline']) if 'deadline' in data else goal.deadline
    goal.completed = data.get('completed', goal.completed)
    
    db.session.commit()
    return jsonify({'message': 'Goal updated successfully'})

@tasks_bp.route('/api/goals/<int:goal_id>', methods=['DELETE'])
@login_required
def delete_goal(goal_id):
    """Delete a goal"""
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    db.session.delete(goal)
    db.session.commit()
    return jsonify({'message': 'Goal deleted successfully'})

@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get all tasks for the current user"""
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': task.id,
        'goal_id': task.goal_id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'due_date': task.due_date.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None,
        'created_at': task.created_at.isoformat()
    } for task in tasks])

@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task"""
    data = request.json
    new_task = Task(
        user_id=current_user.id,
        goal_id=data.get('goal_id'),
        title=data['title'],
        description=data.get('description', ''),
        due_date=datetime.fromisoformat(data['due_date'])
    )
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        'id': new_task.id,
        'goal_id': new_task.goal_id,
        'title': new_task.title,
        'description': new_task.description,
        'status': new_task.status,
        'due_date': new_task.due_date.isoformat(),
        'created_at': new_task.created_at.isoformat()
    }), 201

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update a task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.json
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.due_date = datetime.fromisoformat(data['due_date']) if 'due_date' in data else task.due_date
    
    if data.get('status') == 'completed' and not task.completed_at:
        task.completed_at = datetime.utcnow()
    elif data.get('status') != 'completed':
        task.completed_at = None
    
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}) 