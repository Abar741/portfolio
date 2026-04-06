from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required
from app.extensions import db
from app.models.project import Project
import os
import json
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models.skill import Skill
from app.models.message import Message
from app.models.testimonial import Testimonial

admin = Blueprint("admin", __name__, url_prefix="/admin")


# Helper functions for counts
def get_unread_messages_count():
    """Get count of unread regular messages (excluding feedback)"""
    return Message.query.filter_by(status='unread').filter(
        ~Message.subject.like("%Feedback Submission%")
    ).count()

def get_unread_feedback_count():
    """Get count of unread feedback submissions"""
    return Message.query.filter(Message.subject.contains('Feedback Submission')).filter_by(status='unread').count()

def get_navbar_data():
    """Get navbar data from JSON file"""
    navbar_data_file = os.path.join(current_app.root_path, 'static', 'data', 'navbar_data.json')
    
    if os.path.exists(navbar_data_file):
        try:
            with open(navbar_data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            current_app.logger.error(f"Error loading navbar data: {str(e)}")
    
    # Return default data if file doesn't exist or error occurred
    return {
        "brand": {
            "logo": "/static/images/logo.png",
            "alt": "Graphic Nest",
            "url": "#hero"
        },
        "links": [
            {"text": "Home", "url": "#hero", "active": True},
            {"text": "About", "url": "#about", "active": False},
            {"text": "Services", "url": "#services", "active": False},
            {"text": "Projects", "url": "#projects", "active": False},
            {"text": "Skills", "url": "#skills", "active": False},
            {"text": "Testimonials", "url": "#testimonials", "active": False},
            {"text": "Feedback", "url": "#feedback-contact-section", "active": False},
            {"text": "Contact", "url": "#feedback-contact-section", "active": False}
        ]
    }

def save_navbar_data(navbar_data):
    """Save navbar data to JSON file"""
    try:
        # Use absolute path to avoid any path issues
        navbar_data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'navbar_data.json'))
        
        # Debug: Log the file path and data
        current_app.logger.info(f"Saving navbar data to: {navbar_data_file}")
        current_app.logger.info(f"Navbar data to save: {navbar_data}")
        current_app.logger.info(f"Current working directory: {os.getcwd()}")
        current_app.logger.info(f"Current app root path: {current_app.root_path}")
        
        # Ensure directory exists
        dir_path = os.path.dirname(navbar_data_file)
        os.makedirs(dir_path, exist_ok=True)
        current_app.logger.info(f"Directory created/verified: {dir_path}")
        
        # Debug: Check if file is writable
        if os.path.exists(navbar_data_file):
            current_app.logger.info(f"File exists and is writable: {os.access(navbar_data_file, os.W_OK)}")
        else:
            current_app.logger.info(f"File does not exist, will be created")
        
        # Write the file
        with open(navbar_data_file, 'w') as f:
            json.dump(navbar_data, f, indent=2)
        
        # Debug: Verify file was saved
        if os.path.exists(navbar_data_file):
            current_app.logger.info(f"File saved successfully at: {navbar_data_file}")
            # Read it back to verify
            with open(navbar_data_file, 'r') as f:
                verify_data = json.load(f)
            current_app.logger.info(f"File verification successful: {len(verify_data)} keys")
        else:
            current_app.logger.error(f"File was not created!")
            return False
            
        return True
    except Exception as e:
        current_app.logger.error(f"Error saving navbar data: {str(e)}")
        current_app.logger.error(f"Exception type: {type(e).__name__}")
        current_app.logger.error(f"Exception args: {e.args}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return False


# ADMIN ROOT - Redirect to Dashboard
@admin.route("/")
@login_required
def admin_root():
    """Admin root route - redirect to dashboard"""
    return redirect(url_for("admin.dashboard"))


# CONTROL CENTER
@admin.route("/control-center")
@login_required
def control_center():
    unread_count = get_unread_messages_count()
    feedback_unread_count = get_unread_feedback_count()
    return render_template("admin/control_center_pro.html", unread_count=unread_count, feedback_unread_count=feedback_unread_count)


# DASHBOARD
@admin.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.all()
    
    # Get regular messages (excluding feedback)
    messages = Message.query.filter(
        ~Message.subject.like("%Feedback Submission%")
    ).order_by(Message.id.desc()).all()
    
    testimonials = Testimonial.query.filter_by(is_active=True).order_by(Testimonial.created_at.desc()).all()
    
    # Get feedback submissions (messages)
    feedback_messages = Message.query.filter(
        Message.subject.like("%Feedback Submission%")
    ).order_by(Message.id.desc()).all()
    
    # Count unread messages (excluding feedback)
    unread_count = Message.query.filter_by(status='unread').filter(
        ~Message.subject.like("%Feedback Submission%")
    ).count()
    
    return render_template("admin/dashboard_pro.html", 
                         projects=projects, 
                         skills=skills, 
                         messages=messages,
                         testimonials=testimonials,
                         feedback_messages=feedback_messages,
                         unread_count=unread_count,
                         feedback_unread_count=get_unread_feedback_count())


# PROJECTS LIST
@admin.route("/projects")
@login_required
def projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    unread_count = get_unread_messages_count()
    return render_template("admin/projects_pro.html", projects=projects, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


# ADD PROJECT
@admin.route("/projects/add", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        image_file = request.files.get("image")
        video_file = request.files.get("video")
        image_filename = None
        video_filename = None

        # Handle image upload
        if image_file and image_file.filename != "":
            image_filename = secure_filename(image_file.filename)
            image_filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                image_filename
            )
            image_file.save(image_filepath)

        # Handle video upload
        if video_file and video_file.filename != "":
            video_filename = secure_filename(video_file.filename)
            video_filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                video_filename
            )
            video_file.save(video_filepath)

        project = Project(
            title=request.form.get("title"),
            description=request.form.get("description"),
            github_link=request.form.get("github_link"),
            live_link=request.form.get("live_link"),
            image=image_filename,
            video=video_filename,
            category=request.form.get("category", "web_dev")
        )

        db.session.add(project)
        db.session.commit()

        flash("Project Added Successfully ✅", "success")
        return redirect(url_for("admin.dashboard"))

    unread_count = get_unread_messages_count()
    return render_template("admin/add_project.html", unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


# EDIT PROJECT
@admin.route("/projects/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == "POST":
        project.title = request.form.get("title")
        project.description = request.form.get("description")
        project.github_link = request.form.get("github_link")
        project.live_link = request.form.get("live_link")
        project.category = request.form.get("category", "web_dev")
        
        # Handle image update if new image is uploaded
        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            image_file.save(filepath)
            project.image = filename
            
        # Handle video update if new video is uploaded
        video_file = request.files.get("video")
        if video_file and video_file.filename != "":
            video_filename = secure_filename(video_file.filename)
            video_filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                video_filename
            )
            video_file.save(video_filepath)
            project.video = video_filename

        db.session.commit()

        flash("Project Updated Successfully ✅", "success")
        return redirect(url_for("admin.dashboard"))

    unread_count = get_unread_messages_count()
    return render_template("admin/edit_project.html", project=project, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())

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
    unread_count = get_unread_messages_count()
    return render_template("admin/skills_pro.html", skills=skills, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())

# DELETE SKILL
@admin.route("/skills/delete/<int:id>", methods=["POST"])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    skill_name = skill.name
    
    try:
        db.session.delete(skill)
        db.session.commit()
        flash(f"Skill '{skill_name}' deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting skill: {str(e)}", "error")
    
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

# DELETE MESSAGE
@admin.route("/messages/delete/<int:id>", methods=["POST"])
@login_required
def delete_message(id):
    """Delete regular message"""
    try:
        # Simple test to see if route is being called
        print(f"DEBUG: delete_message called with id={id}")
        
        message = Message.query.get_or_404(id)
        print(f"DEBUG: Found message: {message.subject}")
        
        # Ensure it's not a feedback message
        if "Feedback Submission" in message.subject:
            print("DEBUG: This is a feedback message, redirecting")
            flash("Cannot delete feedback message from this endpoint. Use feedback management instead.", "error")
            return redirect(url_for("admin.messages"))
        
        print("DEBUG: Deleting regular message")
        db.session.delete(message)
        db.session.commit()
        print("DEBUG: Message deleted successfully")
        flash("Message Deleted Successfully!", "success")
        return redirect(url_for("admin.messages"))
        
    except Exception as e:
        print(f"DEBUG: Error in delete_message: {e}")
        db.session.rollback()
        flash(f"Error deleting message: {str(e)}", "error")
        return redirect(url_for("admin.messages"))

# TEST ROUTE - Simple debug route
@admin.route("/test-delete/<int:id>", methods=["POST"])
@login_required
def test_delete(id):
    """Test route to debug routing issues"""
    print(f"DEBUG: test_delete called with id={id}")
    return f"Test delete route called with id={id}"

@admin.route("/messages")
@login_required
def messages():
    from datetime import datetime, timedelta
    
    # Get only regular messages, exclude feedback submissions
    messages = Message.query.filter(
        ~Message.subject.like("%Feedback Submission%")
    ).order_by(Message.id.desc()).all()
    
    week_ago = datetime.now() - timedelta(days=7)
    
    # Count unread messages (excluding feedback)
    unread_count = Message.query.filter_by(status='unread').filter(
        ~Message.subject.like("%Feedback Submission%")
    ).count()
    
    return render_template("admin/messages_pro.html", messages=messages, week_ago=week_ago, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


# HERO SECTION EDITOR
@admin.route("/hero", methods=["GET", "POST"])
@login_required
def hero_editor():
    """Hero section editor for admin dashboard"""
    
    # Load existing hero data if available
    hero_data = None
    hero_data_file = os.path.join(current_app.root_path, 'static', 'data', 'hero_data.json')
    if os.path.exists(hero_data_file):
        try:
            with open(hero_data_file, 'r') as f:
                hero_data = json.load(f)
        except:
            pass
    
    if request.method == "POST":
        # Handle profile image upload
        profile_image_filename = None
        if hero_data and hero_data.get('profile_image'):
            profile_image_filename = hero_data.get('profile_image')
            
        file = request.files.get("profile_image_file")
        if file and file.filename != "":
            # Ensure the uploads directory exists
            upload_folder = current_app.config.get("UPLOAD_FOLDER", os.path.join(current_app.root_path, 'static', 'uploads'))
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                
            # Save the file with a unique filename
            filename = secure_filename(file.filename)
            # Add timestamp to make filename unique
            name, ext = os.path.splitext(filename)
            filename = f"hero_{name}_{int(time.time())}{ext}"
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            profile_image_filename = filename
            
            # Delete old image if exists
            if hero_data and hero_data.get('profile_image'):
                try:
                    old_image_path = os.path.join(upload_folder, hero_data.get('profile_image'))
                    if os.path.exists(old_image_path) and hero_data.get('profile_image') != filename:
                        os.remove(old_image_path)
                except:
                    pass
        
        # Get form data and update hero data
        hero_data = {
            "name": request.form.get("name", "Muhammad Abrar"),
            "subtitle": request.form.get("subtitle", ""),
            "profile_image": profile_image_filename,
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
        
        # Save hero data to JSON file
        data_dir = os.path.join(current_app.root_path, 'static', 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        try:
            with open(hero_data_file, 'w') as f:
                json.dump(hero_data, f, indent=2)
            flash("Hero section updated successfully! ✅", "success")
        except Exception as e:
            flash(f"Error saving hero data: {str(e)}", "error")
        
        return redirect(url_for("admin.hero_editor"))
    
    # GET request - show the editor
    unread_count = get_unread_messages_count()
    
    # Get dynamic projects count
    try:
        from app.models.project import Project
        projects_count = Project.query.filter_by(status='published').count()
    except:
        projects_count = 0
    
    return render_template("admin/hero_editor.html", hero_data=hero_data, projects_count=projects_count, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


# TESTIMONIALS MANAGEMENT
@admin.route("/testimonials")
@login_required
def testimonials():
    """List all testimonials"""
    testimonials = Testimonial.query.filter_by(is_active=True).order_by(Testimonial.display_order.asc(), Testimonial.created_at.desc()).all()
    unread_count = get_unread_messages_count()
    return render_template("admin/testimonials_pro.html", testimonials=testimonials, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


@admin.route("/testimonials/add", methods=["GET", "POST"])
@login_required
def add_testimonial():
    """Add new testimonial"""
    if request.method == "POST":
        # Handle avatar upload
        file = request.files.get("avatar")
        avatar_filename = None
        
        if file and file.filename != "":
            avatar_filename = secure_filename(file.filename)
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                avatar_filename
            )
            file.save(filepath)
        
        testimonial = Testimonial(
            client_name=request.form.get("client_name"),
            client_position=request.form.get("client_position"),
            client_company=request.form.get("client_company"),
            client_avatar=avatar_filename,
            quote=request.form.get("quote"),
            rating=int(request.form.get("rating", 5)),
            project_type=request.form.get("project_type"),
            project_type_icon=request.form.get("project_type_icon", "fa-laptop-code"),
            is_active=request.form.get("is_active") == "on",
            display_order=int(request.form.get("display_order", 0))
        )
        
        db.session.add(testimonial)
        db.session.commit()
        
        flash("Testimonial Added Successfully!", "success")
        return redirect(url_for("admin.testimonials"))
    
    unread_count = get_unread_messages_count()
    return render_template("admin/add_testimonial.html", unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


@admin.route("/testimonials/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_testimonial(id):
    """Edit testimonial"""
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == "POST":
        testimonial.client_name = request.form.get("client_name")
        testimonial.client_position = request.form.get("client_position")
        testimonial.client_company = request.form.get("client_company")
        testimonial.quote = request.form.get("quote")
        testimonial.rating = int(request.form.get("rating", 5))
        testimonial.project_type = request.form.get("project_type")
        testimonial.project_type_icon = request.form.get("project_type_icon", "fa-laptop-code")
        testimonial.is_active = request.form.get("is_active") == "on"
        testimonial.display_order = int(request.form.get("display_order", 0))
        
        # Handle avatar update
        file = request.files.get("avatar")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            file.save(filepath)
            testimonial.client_avatar = filename
        
        db.session.commit()
        flash("Testimonial Updated Successfully!", "success")
        return redirect(url_for("admin.testimonials"))
    
    unread_count = get_unread_messages_count()
    return render_template("admin/edit_testimonial.html", testimonial=testimonial, unread_count=unread_count, feedback_unread_count=get_unread_feedback_count())


@admin.route("/testimonials/delete/<int:id>", methods=["POST"])
@login_required
def delete_testimonial(id):
    """Delete testimonial"""
    testimonial = Testimonial.query.get_or_404(id)
    
    # Delete avatar if exists
    if testimonial.client_avatar:
        try:
            avatar_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                testimonial.client_avatar
            )
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        except:
            pass
    
    db.session.delete(testimonial)
    db.session.commit()
    flash("Testimonial Deleted Successfully!", "success")
    return redirect(url_for("admin.testimonials"))


# FEEDBACK MANAGEMENT ROUTES
@admin.route("/feedback")
@login_required
def feedback():
    """Manage all feedback submissions"""
    # Get all messages that are feedback submissions
    feedback_messages = Message.query.filter(
        Message.subject.like("%Feedback Submission%")
    ).order_by(Message.id.desc()).all()
    
    # Get associated testimonials for avatar images
    testimonials = {}
    for message in feedback_messages:
        # Try to find a testimonial that matches this feedback message by client name
        testimonial = Testimonial.query.filter_by(
            client_name=message.name
        ).first()
        if testimonial:
            testimonials[message.id] = testimonial
    
    unread_count = get_unread_messages_count()
    feedback_unread_count = get_unread_feedback_count()
    
    return render_template("admin/feedback_pro.html", 
                         feedback_messages=feedback_messages, 
                         testimonials=testimonials,
                         unread_count=unread_count,
                         feedback_unread_count=feedback_unread_count)


@admin.route("/feedback/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_feedback(id):
    """Edit feedback message"""
    message = Message.query.get_or_404(id)
    
    if request.method == "POST":
        message.message = request.form.get("message", message.message)
        message.status = request.form.get("status", message.status)
        
        db.session.commit()
        flash("Feedback Updated Successfully!", "success")
        return redirect(url_for("admin.feedback"))
    
    unread_count = get_unread_messages_count()
    feedback_unread_count = get_unread_feedback_count()
    return render_template("admin/edit_feedback.html", 
                         message=message, 
                         unread_count=unread_count,
                         feedback_unread_count=feedback_unread_count)


@admin.route("/feedback/approve/<int:id>", methods=["POST"])
@login_required
def approve_feedback(id):
    """Convert feedback to testimonial and approve it"""
    message = Message.query.get_or_404(id)
    
    try:
        # Parse the feedback message to extract details
        feedback_data = parse_feedback_message(message.message)
        
        # Create or update testimonial
        testimonial = Testimonial(
            client_name=feedback_data.get('client_name', 'Anonymous'),
            client_position=feedback_data.get('position', ''),
            client_company=feedback_data.get('company', ''),
            quote=feedback_data.get('quote', ''),
            rating=feedback_data.get('rating', 5),
            project_type=feedback_data.get('project_type', ''),
            project_type_icon=feedback_data.get('project_type_icon', 'fa-laptop-code'),
            is_active=True,  # Auto-approve
            display_order=0
        )
        
        db.session.add(testimonial)
        
        # Update message status
        message.status = 'approved'
        
        db.session.commit()
        flash("Feedback Approved and Converted to Testimonial!", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error approving feedback: {str(e)}", "error")
    
    return redirect(url_for("admin.feedback"))


@admin.route("/feedback/reject/<int:id>", methods=["POST"])
@login_required
def reject_feedback(id):
    """Reject feedback submission"""
    message = Message.query.get_or_404(id)
    
    message.status = 'rejected'
    db.session.commit()
    
    flash("Feedback Rejected!", "success")
    return redirect(url_for("admin.feedback"))


@admin.route("/feedback/delete/<int:id>", methods=["POST"])
@login_required
def delete_feedback(id):
    """Delete feedback message"""
    message = Message.query.get_or_404(id)
    
    db.session.delete(message)
    db.session.commit()

    flash("Feedback Deleted Successfully!", "success")
    return redirect(url_for("admin.feedback"))


# NAVBAR MANAGEMENT
@admin.route("/navbar")
@login_required
def navbar():
    """Navbar management page"""
    navbar_data = get_navbar_data()
    unread_count = get_unread_messages_count()
    return render_template("admin/navbar_pro.html", 
                         navbar_data=navbar_data, 
                         unread_count=unread_count, 
                         feedback_unread_count=get_unread_feedback_count())

@admin.route("/navbar-management")
@login_required
def navbar_management():
    """Navbar management overview page"""
    navbar_data = get_navbar_data()
    unread_count = get_unread_messages_count()
    return render_template("admin/navbar_management.html", 
                         navbar_data=navbar_data, 
                         unread_count=unread_count,
                         feedback_unread_count=get_unread_feedback_count())

@admin.route("/test-navbar-save")
@login_required
def test_navbar_save():
    """Test navbar save functionality"""
    try:
        # Direct file update - bypass the save_navbar_data function
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'navbar_data.json'))
        
        # Create test data
        test_data = {
            "brand": {
                "logo": "/static/images/logo.png",
                "alt": "Graphic Nest",
                "url": "#hero"
            },
            "links": [
                {"text": "Home", "url": "#hero", "active": True},
                {"text": "About", "url": "#about", "active": False},
                {"text": "Services", "url": "#services", "active": False},
                {"text": "Projects", "url": "#projects", "active": False},
                {"text": "Skills", "url": "#skills", "active": False},
                {"text": "Testimonials", "url": "#testimonials", "active": False},
                {"text": "Feedback", "url": "#feedback-contact-section", "active": False},
                {"text": "Contact", "url": "#feedback-contact-section", "active": False},
                {"text": "TEST LINK", "url": "#test", "active": True}
            ]
        }
        
        # Write directly to file
        with open(file_path, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        flash("Direct file update successful! TEST LINK added to navbar", "success")
        current_app.logger.info(f"Direct file update successful at: {file_path}")
        
    except Exception as e:
        flash(f"Direct file update error: {str(e)}", "error")
        current_app.logger.error(f"Direct file update error: {str(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
    
    return redirect(url_for("admin.navbar"))

@admin.route("/navbar/update", methods=["POST"])
@login_required
def update_navbar():
    """Update navbar data - Respects form data"""
    try:
        # Get form data
        brand_logo = request.form.get("brand_logo", "/static/images/logo.png")
        brand_alt = request.form.get("brand_alt", "Graphic Nest")
        brand_url = request.form.get("brand_url", "#hero")
        
        # Get links data
        link_texts = request.form.getlist("link_text")
        link_urls = request.form.getlist("link_url")
        link_actives = request.form.getlist("link_active")
        
        # Build navbar data structure from form data
        navbar_data = {
            "brand": {
                "logo": brand_logo,
                "alt": brand_alt,
                "url": brand_url
            },
            "links": []
        }
        
        # Build links array from form data
        for i in range(len(link_texts)):
            if link_texts[i] and link_texts[i].strip():  # Only add if text is not empty
                navbar_data["links"].append({
                    "text": link_texts[i].strip(),
                    "url": link_urls[i] if link_urls[i] else "#",
                    "active": link_actives[i] == "on" if i < len(link_actives) else False
                })
        
        # Direct file write
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'data', 'navbar_data.json'))
        with open(file_path, 'w') as f:
            json.dump(navbar_data, f, indent=2)
        
        flash("Navbar updated successfully! Changes saved", "success")
        current_app.logger.info(f"Form-based navbar update successful at: {file_path}")
        
    except Exception as e:
        flash(f"Update error: {str(e)}", "error")
        current_app.logger.error(f"Form-based update error: {str(e)}")
    
    return redirect(url_for("admin.navbar"))


def parse_feedback_message(message_text):
    """Parse feedback message to extract structured data"""
    data = {}
    
    lines = message_text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'Client':
                data['client_name'] = value
            elif key == 'Position':
                data['position'] = value
            elif key == 'Company':
                data['company'] = value
            elif key == 'Project Type':
                data['project_type'] = value
            elif key == 'Rating':
                # Count stars
                data['rating'] = value.count('⭐')
            elif key.startswith('Feedback:') and '"' in value:
                # Extract quote
                start = value.find('"') + 1
                end = value.find('"', start)
                if end > start:
                    data['quote'] = value[start:end]
    
    # Set project type icon based on project type
    project_type_icons = {
        "Web Development": "fa-laptop-code",
        "Mobile App": "fa-mobile-alt", 
        "Backend Development": "fa-server",
        "Full Stack Development": "fa-code",
        "UI/UX Design": "fa-paint-brush",
        "Graphic Design": "fa-palette",
        "Video Editing": "fa-video",
        "Cloud Architecture": "fa-cloud",
        "Database": "fa-database",
        "Security": "fa-shield-alt"
    }
    
    if data.get('project_type'):
        data['project_type_icon'] = project_type_icons.get(data['project_type'], "fa-laptop-code")
    
    return data


# MARK MESSAGE AS READ
@admin.route("/messages/<int:id>/read", methods=["POST"])
@login_required
def mark_message_as_read(id):
    """Mark a specific message as read"""
    try:
        message = Message.query.get_or_404(id)
        
        # Ensure it's not a feedback message
        if "Feedback Submission" in message.subject:
            return jsonify({
                "success": False,
                "message": "Cannot mark feedback message as read from this endpoint"
            })
        
        if message.status == 'unread':
            message.status = 'read'
            message.read_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Message marked as read"
            })
        else:
            return jsonify({
                "success": True,
                "message": "Message was already read"
            })
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error marking message as read: {str(e)}"
        })


# MARK ALL MESSAGES AS READ
@admin.route("/messages/mark-all-read", methods=["POST"])
@login_required
def mark_all_messages_as_read():
    """Mark all unread messages as read"""
    try:
        # Get all unread messages (excluding feedback)
        unread_messages = Message.query.filter_by(status='unread').filter(
            ~Message.subject.like("%Feedback Submission%")
        ).all()
        
        if not unread_messages:
            return jsonify({
                "success": False,
                "message": "No unread messages to mark as read"
            })
        
        # Mark all as read
        for message in unread_messages:
            message.status = 'read'
            message.read_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Marked {len(unread_messages)} messages as read"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error marking messages as read: {str(e)}"
        })


# DELETE ALL READ MESSAGES
@admin.route("/messages/delete-all-read", methods=["POST"])
@login_required
def delete_all_read_messages():
    """Delete all read messages"""
    try:
        # Get all read messages (excluding feedback)
        read_messages = Message.query.filter_by(status='read').filter(
            ~Message.subject.like("%Feedback Submission%")
        ).all()
        
        if not read_messages:
            return jsonify({
                "success": False,
                "message": "No read messages to delete"
            })
        
        # Delete all read messages
        for message in read_messages:
            db.session.delete(message)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Deleted {len(read_messages)} read messages"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error deleting read messages: {str(e)}"
        })


# CONTACT MANAGEMENT ROUTES
@admin.route("/contact")
@login_required
def contact():
    """Manage all contact form submissions"""
    from datetime import datetime, timedelta
    
    # Get contact messages (excluding feedback submissions)
    contact_messages = Message.query.filter(
        ~Message.subject.like("%Feedback Submission%")
    ).order_by(Message.created_at.desc()).all()
    
    # Get unread count
    unread_count = get_unread_messages_count()
    feedback_unread_count = get_unread_feedback_count()
    
    # Calculate statistics
    total_contacts = len(contact_messages)
    recent_contacts = len([msg for msg in contact_messages if msg.created_at > datetime.utcnow() - timedelta(days=7)])
    
    return render_template("admin/contact_pro.html", 
                         messages=contact_messages, 
                         unread_count=unread_count,
                         feedback_unread_count=feedback_unread_count,
                         total_contacts=total_contacts,
                         recent_contacts=recent_contacts)


@admin.route("/contact/delete/<int:id>", methods=["POST"])
@login_required
def delete_contact(id):
    """Delete contact message"""
    try:
        message = Message.query.get_or_404(id)
        
        # Don't allow deletion of feedback submissions through this route
        if "Feedback Submission" in message.subject:
            return jsonify({
                "success": False,
                "message": "Please use feedback management to delete feedback submissions"
            })
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Contact message deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error deleting contact message: {str(e)}"
        })