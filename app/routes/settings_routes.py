from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings')
@login_required
def settings():
    """Settings page with comprehensive admin options"""
    return render_template('admin/settings.html',
                        title='Settings')

@settings_bp.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def profile_settings():
    """Profile settings management"""
    if request.method == 'POST':
        # Handle profile update logic here
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('settings.profile_settings'))
    
    return render_template('admin/settings/profile.html',
                        title='Profile Settings')

@settings_bp.route('/settings/security', methods=['GET', 'POST'])
@login_required
def security_settings():
    """Security settings management"""
    if request.method == 'POST':
        # Handle security settings update logic here
        flash('Security settings updated successfully!', 'success')
        return redirect(url_for('settings.security_settings'))
    
    return render_template('admin/settings/security.html',
                        title='Security Settings')

@settings_bp.route('/settings/notifications', methods=['GET', 'POST'])
@login_required
def notification_settings():
    """Notification settings management"""
    if request.method == 'POST':
        # Handle notification settings update logic here
        flash('Notification preferences updated successfully!', 'success')
        return redirect(url_for('settings.notification_settings'))
    
    return render_template('admin/settings/notifications.html',
                        title='Notification Settings')

@settings_bp.route('/settings/appearance', methods=['GET', 'POST'])
@login_required
def appearance_settings():
    """Appearance settings management"""
    if request.method == 'POST':
        # Handle appearance settings update logic here
        flash('Appearance settings updated successfully!', 'success')
        return redirect(url_for('settings.appearance_settings'))
    
    return render_template('admin/settings/appearance.html',
                        title='Appearance Settings')

@settings_bp.route('/settings/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio_settings():
    """Portfolio-specific settings management"""
    if request.method == 'POST':
        # Handle portfolio settings update logic here
        flash('Portfolio settings updated successfully!', 'success')
        return redirect(url_for('settings.portfolio_settings'))
    
    return render_template('admin/settings/portfolio.html',
                        title='Portfolio Settings')
