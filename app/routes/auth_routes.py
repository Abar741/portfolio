from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app.models.user import User
from app.extensions import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    # Import the helper functions
    from app.routes.admin_routes import get_unread_messages_count, get_unread_feedback_count

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("admin.dashboard"))

        flash("Invalid credentials")

    # Pass counts to prevent template errors (will be 0 since not logged in)
    return render_template("admin/login.html", 
                         unread_count=0, 
                         feedback_unread_count=0)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))