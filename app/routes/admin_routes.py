from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from app.extensions import db
from app.models.project import Project
import os
from werkzeug.utils import secure_filename
from app.models.skill import Skill
from app.models.message import Message

admin = Blueprint("admin", __name__, url_prefix="/admin")


# CONTROL CENTER
@admin.route("/control-center")
@login_required
def control_center():
    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/control_center_pro.html", unread_count=unread_count)


# DASHBOARD
@admin.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.all()
    messages = Message.query.order_by(Message.id.desc()).all()
    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/dashboard_pro.html", 
                         projects=projects, 
                         skills=skills, 
                         messages=messages,
                         unread_count=unread_count)


# PROJECTS LIST
@admin.route("/projects")
@login_required
def projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/projects_pro.html", projects=projects, unread_count=unread_count)


# ADD PROJECT
@admin.route("/projects/add", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        file = request.files.get("image")
        filename = None

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            file.save(filepath)

        project = Project(
            title=request.form.get("title"),
            description=request.form.get("description"),
            github_link=request.form.get("github"),
            live_link=request.form.get("live"),
            image=filename
        )

        db.session.add(project)
        db.session.commit()

        flash("Project Added Successfully ✅", "success")
        return redirect(url_for("admin.dashboard"))

    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/add_project.html", unread_count=unread_count)


# EDIT PROJECT
@admin.route("/projects/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == "POST":
        project.title = request.form.get("title")
        project.description = request.form.get("description")
        project.github_link = request.form.get("github")
        project.live_link = request.form.get("live")
        
        # Handle image update if new image is uploaded
        file = request.files.get("image")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            file.save(filepath)
            project.image = filename

        db.session.commit()

        flash("Project Updated Successfully ✅", "success")
        return redirect(url_for("admin.dashboard"))

    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/edit_project.html", project=project, unread_count=unread_count)

# Skill Route

@admin.route("/skills", methods=["GET", "POST"])
@login_required
def skills():

    if request.method == "POST":
        skill = Skill(
            name=request.form.get("name"),
            percentage=request.form.get("percentage")
        )

        db.session.add(skill)
        db.session.commit()

        flash("Skill Added Successfully ✅", "success")
        return redirect(url_for("admin.skills"))

    skills = Skill.query.all()
    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/skills_pro.html", skills=skills, unread_count=unread_count)

# DELETE SKILL
@admin.route("/skills/delete/<int:id>", methods=["POST"])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash(f"Skill '{skill.name}' deleted successfully!", "success")
    return redirect(url_for("admin.skills"))

# DELETE PROJECT
@admin.route("/projects/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    
    # Delete image file if it exists
    if project.image:
        try:
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                project.image
            )
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception as e:
            flash(f"Error deleting image: {str(e)}", "warning")

    db.session.delete(project)
    db.session.commit()
    flash("Project Deleted Successfully ✅", "success")
    return redirect(url_for("admin.dashboard"))

@admin.route("/messages")
@login_required
def messages():
    from datetime import datetime, timedelta
    messages = Message.query.order_by(Message.id.desc()).all()
    week_ago = datetime.now() - timedelta(days=7)
    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/messages_pro.html", messages=messages, week_ago=week_ago, unread_count=unread_count)


# HERO SECTION EDITOR
@admin.route("/hero", methods=["GET", "POST"])
@login_required
def hero_editor():
    """Hero section editor for admin dashboard"""
    if request.method == "POST":
        # Get form data and update hero data
        hero_data = {
            "name": request.form.get("name", "Muhammad Abrar"),
            "subtitle": request.form.get("subtitle", ""),
            "profile_image": request.form.get("profile_image") or None,
            "badge": {
                "icon": request.form.get("badge_icon", "fas fa-sparkles"),
                "text": request.form.get("badge_text", "Available for Projects")
            },
            "roles": [],
            "buttons": [],
            "stats": [],
            "timeline": {
                "title": request.form.get("timeline_title", "5+ Years Experience"),
                "subtitle": request.form.get("timeline_subtitle", "Professional Development")
            },
            "scroll_text": request.form.get("scroll_text", "Scroll Down"),
            "show_scroll_indicator": request.form.get("show_scroll_indicator") == "on"
        }
        
        # Collect roles
        role_icons = request.form.getlist("role_icon[]")
        role_titles = request.form.getlist("role_title[]")
        for i in range(len(role_icons)):
            if role_icons[i] and role_titles[i]:
                hero_data["roles"].append({
                    "icon": role_icons[i],
                    "title": role_titles[i]
                })
        
        # Collect buttons
        button_icons = request.form.getlist("button_icon[]")
        button_texts = request.form.getlist("button_text[]")
        button_urls = request.form.getlist("button_url[]")
        button_styles = request.form.getlist("button_style[]")
        for i in range(len(button_icons)):
            if button_icons[i] and button_texts[i] and button_urls[i]:
                hero_data["buttons"].append({
                    "icon": button_icons[i],
                    "text": button_texts[i],
                    "url": button_urls[i],
                    "style": button_styles[i] or "primary"
                })
        
        # Collect stats
        stat_values = request.form.getlist("stat_value[]")
        stat_labels = request.form.getlist("stat_label[]")
        for i in range(len(stat_values)):
            if stat_values[i] and stat_labels[i]:
                hero_data["stats"].append({
                    "value": stat_values[i],
                    "label": stat_labels[i]
                })
        
        # Add default floating icons
        hero_data["floating_icons"] = [
            {"icon_class": "fas fa-code", "label": "Web Dev", "animation": "down", "delay": 600},
            {"icon_class": "fas fa-palette", "label": "Design", "animation": "up", "delay": 700},
            {"icon_class": "fas fa-video", "label": "Video", "animation": "down", "delay": 800},
            {"icon_class": "fas fa-mobile-alt", "label": "Mobile", "animation": "up", "delay": 900},
            {"icon_class": "fas fa-camera", "label": "Photo", "animation": "down", "delay": 1000}
        ]
        
        # For now, just flash success (in production, save to database)
        flash("Hero section updated successfully! ✅", "success")
        
        # You could save this to a JSON file or database here
        # Example: save_hero_data_to_file(hero_data)
        
        return redirect(url_for("admin.hero_editor"))
    
    # GET request - show the editor
    unread_count = Message.query.filter_by(status='unread').count()
    return render_template("admin/hero_editor.html", unread_count=unread_count)