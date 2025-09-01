from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.schema import Subscription

subscription_bp = Blueprint('subscription', __name__)

@subscription_bp.route('/subscriptions', methods=['GET'])
@login_required
def view_subscriptions():
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    return render_template('subscription.html', subscriptions=subscriptions)

@subscription_bp.route('/subscriptions/create', methods=['POST'])
@login_required
def create_subscription():
    subscription_type = request.form.get('subscription_type')
    new_subscription = Subscription(user_id=current_user.id, type=subscription_type)
    new_subscription.save()
    flash('Subscription created successfully!', 'success')
    return redirect(url_for('subscription.view_subscriptions'))

@subscription_bp.route('/subscriptions/cancel/<int:subscription_id>', methods=['POST'])
@login_required
def cancel_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    if subscription.user_id == current_user.id:
        subscription.delete()
        flash('Subscription canceled successfully!', 'success')
    else:
        flash('You do not have permission to cancel this subscription.', 'danger')
    return redirect(url_for('subscription.view_subscriptions'))