from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.schema import db, Goal, Task
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/api/goals', methods=['GET'])
@login_required
def get_goals():
    """Get all goals for the current user"""
    try:
        goals = Goal.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': goal.id,
            'title': goal.title,
            'description': goal.description,
            'deadline': goal.deadline.isoformat() if goal.deadline else None,
            'completed': goal.completed,
            'completion_percentage': goal.completion_percentage,
            'target_minutes': goal.target_minutes,
            'completed_minutes': goal.completed_minutes,
            'category': goal.category,
            'priority': goal.priority,
            'color': goal.color,
            'icon': goal.icon,
            'created_at': goal.created_at.isoformat(),
            'updated_at': goal.updated_at.isoformat()
        } for goal in goals]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch goals'}), 500

@tasks_bp.route('/api/goals', methods=['POST'])
@login_required
def create_goal():
    """Create a new goal"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.json
    
    # Validate required fields
    if not data.get('title'):
        return jsonify({'error': 'Goal title is required'}), 400
    
    try:
        new_goal = Goal(
            user_id=current_user.id,
            title=data['title'],
            description=data.get('description', ''),
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            category=data.get('category'),
            priority=data.get('priority', 'medium'),
            target_minutes=data.get('target_minutes'),
            color=data.get('color', '#3B82F6'),
            icon=data.get('icon')
        )
        
        db.session.add(new_goal)
        db.session.commit()
        
        return jsonify({
            'id': new_goal.id,
            'title': new_goal.title,
            'description': new_goal.description,
            'deadline': new_goal.deadline.isoformat() if new_goal.deadline else None,
            'completed': new_goal.completed,
            'completion_percentage': new_goal.completion_percentage,
            'target_minutes': new_goal.target_minutes,
            'completed_minutes': new_goal.completed_minutes,
            'category': new_goal.category,
            'priority': new_goal.priority,
            'color': new_goal.color,
            'icon': new_goal.icon,
            'created_at': new_goal.created_at.isoformat(),
            'updated_at': new_goal.updated_at.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create goal'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@tasks_bp.route('/api/goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    """Update a goal"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        data = request.json
        
        # Update fields if provided
        if 'title' in data:
            goal.title = data['title']
        if 'description' in data:
            goal.description = data['description']
        if 'deadline' in data:
            try:
                goal.deadline = datetime.fromisoformat(data['deadline']) if data['deadline'] else None
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        if 'completed' in data:
            goal.completed = data['completed']
        if 'category' in data:
            goal.category = data['category']
        if 'priority' in data:
            goal.priority = data['priority']
        if 'target_minutes' in data:
            goal.target_minutes = data['target_minutes']
        if 'color' in data:
            goal.color = data['color']
        if 'icon' in data:
            goal.icon = data['icon']
        
        goal.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': {
                'id': goal.id,
                'title': goal.title,
                'description': goal.description,
                'deadline': goal.deadline.isoformat() if goal.deadline else None,
                'completed': goal.completed,
                'completion_percentage': goal.completion_percentage,
                'target_minutes': goal.target_minutes,
                'completed_minutes': goal.completed_minutes,
                'category': goal.category,
                'priority': goal.priority,
                'color': goal.color,
                'icon': goal.icon,
                'updated_at': goal.updated_at.isoformat()
            }
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update goal'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@tasks_bp.route('/api/goals/<int:goal_id>', methods=['DELETE'])
@login_required
def delete_goal(goal_id):
    """Delete a goal"""
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({'message': 'Goal deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete goal'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@tasks_bp.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get all tasks for the current user"""
    try:
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': task.id,
            'goal_id': task.goal_id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'estimated_minutes': task.estimated_minutes,
            'actual_minutes': task.actual_minutes,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'position': task.position,
            'tags': task.tags or [],
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat()
        } for task in tasks]), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tasks'}), 500

@tasks_bp.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.json
    
    # Validate required fields
    if not data.get('title'):
        return jsonify({'error': 'Task title is required'}), 400
    
    try:
        new_task = Task(
            user_id=current_user.id,
            goal_id=data.get('goal_id'),
            title=data['title'],
            description=data.get('description', ''),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            estimated_minutes=data.get('estimated_minutes'),
            priority=data.get('priority', 'medium'),
            position=data.get('position', 0),
            tags=data.get('tags', [])
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            'id': new_task.id,
            'goal_id': new_task.goal_id,
            'title': new_task.title,
            'description': new_task.description,
            'status': new_task.status,
            'priority': new_task.priority,
            'due_date': new_task.due_date.isoformat() if new_task.due_date else None,
            'estimated_minutes': new_task.estimated_minutes,
            'actual_minutes': new_task.actual_minutes,
            'position': new_task.position,
            'tags': new_task.tags or [],
            'created_at': new_task.created_at.isoformat(),
            'updated_at': new_task.updated_at.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create task'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update a task"""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.json
        
        # Update fields if provided
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'due_date' in data:
            try:
                task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400
        if 'estimated_minutes' in data:
            task.estimated_minutes = data['estimated_minutes']
        if 'actual_minutes' in data:
            task.actual_minutes = data['actual_minutes']
        if 'position' in data:
            task.position = data['position']
        if 'tags' in data:
            task.tags = data['tags']
        
        # Handle completion
        if data.get('status') == 'completed' and not task.completed_at:
            task.completed_at = datetime.utcnow()
        elif data.get('status') != 'completed':
            task.completed_at = None
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': {
                'id': task.id,
                'goal_id': task.goal_id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'estimated_minutes': task.estimated_minutes,
                'actual_minutes': task.actual_minutes,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'position': task.position,
                'tags': task.tags or [],
                'updated_at': task.updated_at.isoformat()
            }
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500

@tasks_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500 