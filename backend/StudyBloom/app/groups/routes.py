from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.schema import db, Group, GroupMembership, Streak, Reward
from datetime import datetime

groups_bp = Blueprint('groups', __name__)

@groups_bp.route('/api/groups', methods=['GET'])
@login_required
def get_groups():
    """Get all groups the user is a member of"""
    memberships = GroupMembership.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).all()
    
    groups = []
    for membership in memberships:
        group = membership.group
        member_count = GroupMembership.query.filter_by(
            group_id=group.id,
            is_active=True
        ).count()
        
        groups.append({
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'max_members': group.max_members,
            'current_members': member_count,
            'role': membership.role,
            'joined_at': membership.joined_at.isoformat(),
            'created_at': group.created_at.isoformat()
        })
    
    return jsonify(groups)

@groups_bp.route('/api/groups/available', methods=['GET'])
@login_required
def get_available_groups():
    """Get groups available to join (user must have 20-day streak)"""
    # Check if user has 20-day streak
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak or streak.current_streak < 20:
        return jsonify({
            'message': 'You need a 20-day streak to join study groups',
            'current_streak': streak.current_streak if streak else 0,
            'required_streak': 20,
            'groups': []
        })
    
    # Get groups that have space and user is not already a member
    user_group_ids = [m.group_id for m in GroupMembership.query.filter_by(user_id=current_user.id).all()]
    
    available_groups = Group.query.filter(
        Group.is_active == True,
        ~Group.id.in_(user_group_ids)
    ).all()
    
    groups = []
    for group in available_groups:
        member_count = GroupMembership.query.filter_by(
            group_id=group.id,
            is_active=True
        ).count()
        
        if member_count < group.max_members:
            groups.append({
                'id': group.id,
                'name': group.name,
                'description': group.description,
                'max_members': group.max_members,
                'current_members': member_count,
                'available_spots': group.max_members - member_count,
                'created_at': group.created_at.isoformat()
            })
    
    return jsonify({
        'message': 'Groups available to join',
        'groups': groups
    })

@groups_bp.route('/api/groups', methods=['POST'])
@login_required
def create_group():
    """Create a new study group (requires 20-day streak)"""
    # Check if user has 20-day streak
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak or streak.current_streak < 20:
        return jsonify({
            'message': 'You need a 20-day streak to create study groups',
            'current_streak': streak.current_streak if streak else 0,
            'required_streak': 20
        }), 403
    
    data = request.json
    
    new_group = Group(
        name=data['name'],
        description=data.get('description', ''),
        max_members=data.get('max_members', 10)
    )
    
    db.session.add(new_group)
    db.session.flush()  # Get the group ID
    
    # Add creator as admin
    membership = GroupMembership(
        user_id=current_user.id,
        group_id=new_group.id,
        role='admin'
    )
    
    db.session.add(membership)
    db.session.commit()
    
    return jsonify({
        'id': new_group.id,
        'name': new_group.name,
        'description': new_group.description,
        'max_members': new_group.max_members,
        'current_members': 1,
        'role': 'admin',
        'created_at': new_group.created_at.isoformat(),
        'message': 'Study group created successfully!'
    }), 201

@groups_bp.route('/api/groups/<int:group_id>/join', methods=['POST'])
@login_required
def join_group(group_id):
    """Join a study group (requires 20-day streak)"""
    # Check if user has 20-day streak
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak or streak.current_streak < 20:
        return jsonify({
            'message': 'You need a 20-day streak to join study groups',
            'current_streak': streak.current_streak if streak else 0,
            'required_streak': 20
        }), 403
    
    group = Group.query.get_or_404(group_id)
    
    if not group.is_active:
        return jsonify({'message': 'Group is not active'}), 400
    
    # Check if user is already a member
    existing_membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()
    
    if existing_membership:
        if existing_membership.is_active:
            return jsonify({'message': 'You are already a member of this group'}), 400
        else:
            # Reactivate membership
            existing_membership.is_active = True
            db.session.commit()
            return jsonify({'message': 'Rejoined group successfully'})
    
    # Check if group is full
    member_count = GroupMembership.query.filter_by(
        group_id=group_id,
        is_active=True
    ).count()
    
    if member_count >= group.max_members:
        return jsonify({'message': 'Group is full'}), 400
    
    # Add user to group
    membership = GroupMembership(
        user_id=current_user.id,
        group_id=group_id,
        role='member'
    )
    
    db.session.add(membership)
    db.session.commit()
    
    return jsonify({
        'message': 'Joined group successfully',
        'group_id': group_id,
        'group_name': group.name
    })

@groups_bp.route('/api/groups/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    """Leave a study group"""
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first_or_404()
    
    if not membership.is_active:
        return jsonify({'message': 'You are not an active member of this group'}), 400
    
    membership.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Left group successfully'})

@groups_bp.route('/api/groups/<int:group_id>/members', methods=['GET'])
@login_required
def get_group_members(group_id):
    """Get all members of a group"""
    # Check if user is a member of the group
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        is_active=True
    ).first()
    
    if not membership:
        return jsonify({'message': 'You are not a member of this group'}), 403
    
    memberships = GroupMembership.query.filter_by(
        group_id=group_id,
        is_active=True
    ).all()
    
    members = []
    for member_membership in memberships:
        user = member_membership.user
        members.append({
            'user_id': user.id,
            'username': user.username,
            'role': member_membership.role,
            'joined_at': member_membership.joined_at.isoformat()
        })
    
    return jsonify(members)

@groups_bp.route('/api/groups/<int:group_id>', methods=['PUT'])
@login_required
def update_group(group_id):
    """Update group details (admin only)"""
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        is_active=True
    ).first_or_404()
    
    if membership.role != 'admin':
        return jsonify({'message': 'Only admins can update group details'}), 403
    
    group = Group.query.get_or_404(group_id)
    data = request.json
    
    group.name = data.get('name', group.name)
    group.description = data.get('description', group.description)
    group.max_members = data.get('max_members', group.max_members)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Group updated successfully',
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'max_members': group.max_members
    })

@groups_bp.route('/api/groups/<int:group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    """Delete a group (admin only)"""
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        is_active=True
    ).first_or_404()
    
    if membership.role != 'admin':
        return jsonify({'message': 'Only admins can delete groups'}), 403
    
    group = Group.query.get_or_404(group_id)
    group.is_active = False
    
    # Deactivate all memberships
    GroupMembership.query.filter_by(group_id=group_id).update({'is_active': False})
    
    db.session.commit()
    
    return jsonify({'message': 'Group deleted successfully'})

@groups_bp.route('/api/groups/check-eligibility', methods=['GET'])
@login_required
def check_group_eligibility():
    """Check if user is eligible to join/create groups"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak:
        return jsonify({
            'eligible': False,
            'current_streak': 0,
            'required_streak': 20,
            'message': 'Start studying to build your streak!'
        })
    
    eligible = streak.current_streak >= 20
    
    return jsonify({
        'eligible': eligible,
        'current_streak': streak.current_streak,
        'required_streak': 20,
        'message': 'You can join study groups!' if eligible else f'Keep going! You need {20 - streak.current_streak} more days to unlock study groups.'
    }) 