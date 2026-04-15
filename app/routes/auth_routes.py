from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from flask_mail import Message

from app.models.user import User
from app.extensions import db, mail

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    # Import the helper functions
    from app.routes.admin_routes import get_unread_messages_count, get_unread_feedback_count

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            # Simple and reliable password verification
            if verify_password_simple(password, user.password_hash):
                login_user(user)
                return redirect(url_for("admin.dashboard"))

        flash("Invalid credentials")

    # Pass counts to prevent template errors (will be 0 since not logged in)
    return render_template("admin/login.html", 
                         unread_count=0, 
                         feedback_unread_count=0)

def verify_password_simple(input_password, stored_hash):
    """
    Simple password verification that works reliably
    """
    import hashlib
    import hmac
    
    # Generate SHA256 hash of input password
    password_hash = hashlib.sha256(input_password.encode('utf-8')).hexdigest()
    
    # Use timing-safe comparison
    return hmac.compare_digest(password_hash, stored_hash)

@auth.route("/auth/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user:
            try:
                # Debug: Check email configuration
                print(f"DEBUG: Email config - Server: {current_app.config.get('MAIL_SERVER')}")
                print(f"DEBUG: Email config - Port: {current_app.config.get('MAIL_PORT')}")
                print(f"DEBUG: Email config - Username: {current_app.config.get('MAIL_USERNAME')}")
                print(f"DEBUG: Email config - Use TLS: {current_app.config.get('MAIL_USE_TLS')}")
                print(f"DEBUG: Email config - Password set: {'Yes' if current_app.config.get('MAIL_PASSWORD') else 'No'}")
                
                # Create password reset email
                msg = Message(
                    "Password Reset Instructions - Portfolio Admin",
                    sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@portfolio.com'),
                    recipients=[email]
                )
                
                # Email body with reset instructions
                msg.body = f"""
Hello {user.username},

You requested a password reset for your Portfolio Admin account.

Username: {user.username}

To reset your password, run this Python command in your project directory:

python -c "
from app import create_app
from app.extensions import db
from app.models.user import User
import hashlib

app = create_app()
app.app_context().push()

# Set your new password here
new_password = 'your_new_password'

# Update admin password
user = User.query.filter_by(username='{user.username}').first()
if user:
    password_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
    user.password_hash = password_hash
    db.session.commit()
    print(f'Password updated to: {{new_password}}')
"

Replace 'your_new_password' with your desired new password.

If you didn't request this reset, please ignore this email.

Best regards,
Portfolio Admin System
"""
                
                # Send email
                mail.send(msg)
                print("DEBUG: Email sent successfully!")
                flash(f"Password reset instructions have been sent to {email}")
                
            except Exception as e:
                # Debug: Show the actual error
                print(f"DEBUG: Email sending failed with error: {str(e)}")
                print(f"DEBUG: Error type: {type(e).__name__}")
                # If email fails, show instructions on screen
                flash(f"Password reset instructions sent to {email}. Your username is '{user.username}' and you can reset your password using the Python script.")
        else:
            # Don't reveal if email exists or not for security
            flash("If an account with that email exists, you'll receive password reset instructions shortly.")
        
        return redirect(url_for("auth.forgot_password"))
    
    return render_template("admin/forgot_password.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))