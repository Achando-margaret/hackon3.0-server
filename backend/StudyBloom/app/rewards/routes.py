from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.schema import db, Reward, Streak
from datetime import datetime, timedelta

rewards_bp = Blueprint('rewards', __name__)

@rewards_bp.route('/api/rewards', methods=['GET'])
@login_required
def get_rewards():
    """Get all rewards for the current user"""
    rewards = Reward.query.filter_by(user_id=current_user.id).order_by(Reward.created_at.desc()).all()
    
    return jsonify([{
        'id': reward.id,
        'reward_type': reward.reward_type,
        'reward_value': reward.reward_value,
        'description': reward.description,
        'unlocked_at': reward.unlocked_at.isoformat() if reward.unlocked_at else None,
        'expires_at': reward.expires_at.isoformat() if reward.expires_at else None,
        'is_used': reward.is_used,
        'created_at': reward.created_at.isoformat()
    } for reward in rewards])

@rewards_bp.route('/api/rewards/available', methods=['GET'])
@login_required
def get_available_rewards():
    """Get available (unlocked but unused) rewards"""
    rewards = Reward.query.filter_by(
        user_id=current_user.id,
        is_used=False
    ).filter(
        (Reward.expires_at.is_(None)) | (Reward.expires_at > datetime.utcnow())
    ).all()
    
    return jsonify([{
        'id': reward.id,
        'reward_type': reward.reward_type,
        'reward_value': reward.reward_value,
        'description': reward.description,
        'expires_at': reward.expires_at.isoformat() if reward.expires_at else None
    } for reward in rewards])

@rewards_bp.route('/api/rewards/check-eligibility', methods=['GET'])
@login_required
def check_reward_eligibility():
    """Check what rewards the user is eligible for based on their activity"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak:
        return jsonify({'eligible_rewards': []})
    
    eligible_rewards = []
    
    # Check for streak-based rewards
    if streak.current_streak >= 7 and streak.current_streak < 14:
        eligible_rewards.append({
            'type': 'discount',
            'value': 10.0,
            'description': '7-day streak discount: 10% off next subscription',
            'requirement': '7-day study streak'
        })
    elif streak.current_streak >= 14 and streak.current_streak < 20:
        eligible_rewards.append({
            'type': 'discount',
            'value': 15.0,
            'description': '14-day streak discount: 15% off next subscription',
            'requirement': '14-day study streak'
        })
    elif streak.current_streak >= 20:
        eligible_rewards.append({
            'type': 'feature_unlock',
            'value': 100.0,
            'description': '20-day streak: Unlock study groups feature',
            'requirement': '20-day study streak'
        })
        eligible_rewards.append({
            'type': 'discount',
            'value': 25.0,
            'description': '20-day streak discount: 25% off next subscription',
            'requirement': '20-day study streak'
        })
    
    return jsonify({'eligible_rewards': eligible_rewards})

@rewards_bp.route('/api/rewards/unlock', methods=['POST'])
@login_required
def unlock_reward():
    """Unlock a reward based on user's current achievements"""
    data = request.json
    reward_type = data.get('reward_type')
    reward_value = data.get('reward_value')
    description = data.get('description')
    
    # Check if user already has this reward
    existing_reward = Reward.query.filter_by(
        user_id=current_user.id,
        reward_type=reward_type,
        reward_value=reward_value,
        is_used=False
    ).first()
    
    if existing_reward:
        return jsonify({'message': 'Reward already unlocked', 'reward_id': existing_reward.id}), 400
    
    # Create new reward
    new_reward = Reward(
        user_id=current_user.id,
        reward_type=reward_type,
        reward_value=reward_value,
        description=description,
        unlocked_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=30) if reward_type == 'discount' else None
    )
    
    db.session.add(new_reward)
    db.session.commit()
    
    return jsonify({
        'id': new_reward.id,
        'reward_type': new_reward.reward_type,
        'reward_value': new_reward.reward_value,
        'description': new_reward.description,
        'unlocked_at': new_reward.unlocked_at.isoformat(),
        'expires_at': new_reward.expires_at.isoformat() if new_reward.expires_at else None,
        'message': 'Reward unlocked successfully!'
    }), 201

@rewards_bp.route('/api/rewards/<int:reward_id>/redeem', methods=['POST'])
@login_required
def redeem_reward(reward_id):
    """Redeem a reward (mark as used)"""
    reward = Reward.query.filter_by(id=reward_id, user_id=current_user.id).first_or_404()
    
    if reward.is_used:
        return jsonify({'message': 'Reward already used'}), 400
    
    if reward.expires_at and reward.expires_at < datetime.utcnow():
        return jsonify({'message': 'Reward has expired'}), 400
    
    reward.is_used = True
    db.session.commit()
    
    return jsonify({
        'message': 'Reward redeemed successfully',
        'reward_type': reward.reward_type,
        'reward_value': reward.reward_value,
        'description': reward.description
    })

@rewards_bp.route('/api/rewards/auto-check', methods=['POST'])
@login_required
def auto_check_rewards():
    """Automatically check and unlock rewards based on user's current achievements"""
    streak = Streak.query.filter_by(user_id=current_user.id).first()
    
    if not streak:
        return jsonify({'message': 'No streak data found', 'rewards_unlocked': 0})
    
    rewards_unlocked = 0
    
    # Check for 7-day streak reward
    if streak.current_streak >= 7:
        reward = Reward.query.filter_by(
            user_id=current_user.id,
            reward_type='discount',
            reward_value=10.0,
            description__contains='7-day streak'
        ).first()
        
        if not reward:
            new_reward = Reward(
                user_id=current_user.id,
                reward_type='discount',
                reward_value=10.0,
                description='7-day streak discount: 10% off next subscription',
                unlocked_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(new_reward)
            rewards_unlocked += 1
    
    # Check for 14-day streak reward
    if streak.current_streak >= 14:
        reward = Reward.query.filter_by(
            user_id=current_user.id,
            reward_type='discount',
            reward_value=15.0,
            description__contains='14-day streak'
        ).first()
        
        if not reward:
            new_reward = Reward(
                user_id=current_user.id,
                reward_type='discount',
                reward_value=15.0,
                description='14-day streak discount: 15% off next subscription',
                unlocked_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(new_reward)
            rewards_unlocked += 1
    
    # Check for 20-day streak rewards
    if streak.current_streak >= 20:
        # Group unlock reward
        group_reward = Reward.query.filter_by(
            user_id=current_user.id,
            reward_type='feature_unlock',
            reward_value=100.0,
            description__contains='study groups'
        ).first()
        
        if not group_reward:
            new_reward = Reward(
                user_id=current_user.id,
                reward_type='feature_unlock',
                reward_value=100.0,
                description='20-day streak: Unlock study groups feature',
                unlocked_at=datetime.utcnow()
            )
            db.session.add(new_reward)
            rewards_unlocked += 1
        
        # 25% discount reward
        discount_reward = Reward.query.filter_by(
            user_id=current_user.id,
            reward_type='discount',
            reward_value=25.0,
            description__contains='20-day streak'
        ).first()
        
        if not discount_reward:
            new_reward = Reward(
                user_id=current_user.id,
                reward_type='discount',
                reward_value=25.0,
                description='20-day streak discount: 25% off next subscription',
                unlocked_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
            db.session.add(new_reward)
            rewards_unlocked += 1
    
    db.session.commit()
    
    return jsonify({
        'message': f'Unlocked {rewards_unlocked} new rewards!',
        'rewards_unlocked': rewards_unlocked
    })

@rewards_bp.route('/api/rewards/statistics', methods=['GET'])
@login_required
def get_reward_statistics():
    """Get reward statistics for the user"""
    total_rewards = Reward.query.filter_by(user_id=current_user.id).count()
    used_rewards = Reward.query.filter_by(user_id=current_user.id, is_used=True).count()
    available_rewards = Reward.query.filter_by(user_id=current_user.id, is_used=False).count()
    
    # Calculate total discount value
    discount_rewards = Reward.query.filter_by(
        user_id=current_user.id,
        reward_type='discount'
    ).all()
    
    total_discount_value = sum(reward.reward_value for reward in discount_rewards)
    
    return jsonify({
        'total_rewards': total_rewards,
        'used_rewards': used_rewards,
        'available_rewards': available_rewards,
        'total_discount_value': total_discount_value,
        'rewards_by_type': {
            'discount': len([r for r in discount_rewards if r.reward_type == 'discount']),
            'feature_unlock': len([r for r in discount_rewards if r.reward_type == 'feature_unlock']),
            'badge': len([r for r in discount_rewards if r.reward_type == 'badge'])
        }
    }) 