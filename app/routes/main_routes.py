from flask import Blueprint, render_template, request, redirect, flash, jsonify, current_app, url_for
from app.services.project_service import ProjectService
from app.services.message_service import MessageService
from app.services.analytics_service import AnalyticsService
from app.services.skill_service import SkillService
from app.utils.logger import log_security_event, log_user_action
from app.utils.exceptions import ValidationError, DatabaseError
from flask_limiter.util import get_remote_address

main = Blueprint("main", __name__)

import os
import json
import time

def get_hero_data():
    """Get hero data from JSON file or return default data"""
    hero_data_file = os.path.join(current_app.root_path, 'static', 'data', 'hero_data.json')
    
    if os.path.exists(hero_data_file):
        try:
            with open(hero_data_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            current_app.logger.error(f"Error loading hero data: {str(e)}")
    
    # Return default data if file doesn't exist or error occurred
    return {
        "name": "Muhammad Abrar",
        "subtitle": "I transform creative ideas into exceptional digital experiences through innovative web development, stunning graphic design, and compelling video editing. Let's create something extraordinary together!",
        "profile_image": None,
        "badge": {
            "icon": "fas fa-sparkles",
            "text": "Available for Projects"
        },
        "roles": [
            {"icon": "fas fa-code", "title": "Web Developer"},
            {"icon": "fas fa-palette", "title": "Graphic Designer"},
            {"icon": "fas fa-video", "title": "Video Editor"}
        ],
        "buttons": [
            {"icon": "fas fa-briefcase", "text": "View Portfolio", "url": "#projects", "style": "primary"},
            {"icon": "fas fa-envelope", "text": "Get In Touch", "url": "#contact", "style": "secondary"}
        ],
        "stats": [
            {"value": "50+", "label": "Projects"},
            {"value": "5+", "label": "Years"},
            {"value": "100%", "label": "Satisfaction"}
        ],
        "floating_icons": [
            {"icon_class": "fas fa-code", "label": "Web Dev", "animation": "down", "delay": 600},
            {"icon_class": "fas fa-palette", "label": "Design", "animation": "up", "delay": 700},
            {"icon_class": "fas fa-video", "label": "Video", "animation": "down", "delay": 800},
            {"icon_class": "fas fa-mobile-alt", "label": "Mobile", "animation": "up", "delay": 900},
            {"icon_class": "fas fa-camera", "label": "Photo", "animation": "down", "delay": 1000}
        ],
        "timeline": {
            "title": "5+ Years Experience",
            "subtitle": "Professional Development"
        },
        "scroll_text": "Scroll Down",
        "show_scroll_indicator": True
    }

# HOME PAGE
@main.route("/")
def home():
    """Home page with portfolio content"""
    try:
        # Get portfolio data
        projects = ProjectService.get_all_projects('published')
        featured_projects = ProjectService.get_featured_projects(6)
        skills = SkillService.get_all_skills()
        
        # Get hero data
        hero_data = get_hero_data()
        
        # Get active testimonials ordered by display_order
        from app.models.testimonial import Testimonial
        testimonials = Testimonial.query.filter_by(is_active=True)\
            .order_by(Testimonial.display_order.asc(), Testimonial.created_at.desc())\
            .all()
        
        # Log analytics
        AnalyticsService.track_page_view('home', get_remote_address())
        
        return render_template("portfolio/index.html",
                             projects=projects,
                             featured_projects=featured_projects,
                             skills=skills,
                             hero_data=hero_data,
                             testimonials=testimonials)
    
    except DatabaseError as e:
        current_app.logger.error(f"Database error on home page: {str(e)}")
        flash("Unable to load portfolio content. Please try again.", "error")
        return render_template("portfolio/index.html", 
                             projects=[], 
                             featured_projects=[], 
                             skills=[],
                             hero_data=get_hero_data(),
                             testimonials=[])
    except Exception as e:
        current_app.logger.error(f"Unexpected error on home page: {str(e)}")
        flash("An unexpected error occurred.", "error")
        return render_template("portfolio/index.html", 
                             projects=[], 
                             featured_projects=[], 
                             skills=[],
                             hero_data=get_hero_data(),
                             testimonials=[])


# CONTACT FORM
@main.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submissions"""
    try:
        # Get request metadata for security logging
        ip_address = get_remote_address()
        user_agent = request.headers.get('User-Agent')
        
        # Prepare message data
        message_data = {
            'name': request.form.get("name", "").strip(),
            'email': request.form.get("email", "").strip(),
            'subject': request.form.get("subject", "").strip(),
            'message': request.form.get("message", "").strip(),
            'ip_address': ip_address,
            'user_agent': user_agent
        }
        
        # Create message using service layer
        message = MessageService.create_message(message_data)
        
        # Log successful submission
        log_security_event('contact_form_submitted', ip_address, user_agent, 
                         f"Message from {message.name}")
        
        flash("Message sent successfully! ✅", "success")
        
        # Track analytics
        AnalyticsService.track_contact_form_submission(ip_address)
        
    except ValidationError as e:
        flash(str(e), "error")
        log_security_event('contact_form_validation_failed', ip_address, user_agent, str(e))
        
    except DatabaseError as e:
        flash("An error occurred while saving your message. Please try again.", "error")
        current_app.logger.error(f"Database error in contact form: {str(e)}")
        
    except Exception as e:
        flash("An unexpected error occurred. Please try again.", "error")
        current_app.logger.error(f"Unexpected error in contact form: {str(e)}")
        
    return redirect("/")


# LEGAL PAGES
@main.route("/privacy-policy")
def privacy_policy():
    """Privacy Policy page"""
    return render_template("portfolio/privacy_policy.html")


@main.route("/terms-of-service")
def terms_of_service():
    """Terms of Service page"""
    return render_template("portfolio/terms_of_service.html")


@main.route("/cookie-policy")
def cookie_policy():
    """Cookie Policy page"""
    return render_template("portfolio/cookie_policy.html")


@main.route("/sitemap")
def sitemap():
    """Sitemap page"""
    return render_template("portfolio/sitemap.html")


# ALL PROJECTS PAGE
@main.route("/portfolio")
def portfolio():
    """All Projects page with category filtering"""
    try:
        from app.models.project import Project
        
        # Get all published projects ordered by created_at DESC
        projects = Project.query.filter_by(status='published')\
            .order_by(Project.created_at.desc())\
            .all()
        
        return render_template("portfolio/projects.html",
                             projects=projects,
                             hero_data=get_hero_data())
    except Exception as e:
        current_app.logger.error(f"Error fetching projects for portfolio page: {str(e)}")
        return render_template("portfolio/projects.html",
                             projects=[],
                             hero_data=get_hero_data())


# API: RECENT PROJECTS FOR NEWS SLIDER
@main.route("/recent-projects")
def recent_projects():
    """API endpoint to get recent published projects for news slider"""
    try:
        from app.models.project import Project
        
        # Get latest 7 published projects ordered by created_at DESC
        projects = Project.query.filter_by(status='published')\
            .order_by(Project.created_at.desc())\
            .limit(7)\
            .all()
        
        # Format projects for JSON response
        projects_data = []
        for project in projects:
            # Truncate description to 80 chars
            desc = project.description or ""
            short_desc = desc[:80] + "..." if len(desc) > 80 else desc
            
            projects_data.append({
                'id': project.id,
                'title': project.title,
                'description': short_desc,
                'full_description': project.description,
                'image': project.image,
                'video': project.video,  # ✅ Add video field
                'github_link': project.github_link,
                'live_link': project.live_link,
                'technologies': project.technologies,
                'category': project.category,
                'featured': project.featured,
                'created_at': project.created_at.strftime('%b %d, %Y') if project.created_at else None,
                'updated_at': project.updated_at.strftime('%b %d, %Y') if project.updated_at else None
            })
        
        return jsonify({
            'success': True,
            'projects': projects_data,
            'count': len(projects_data)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching recent projects: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch projects',
            'projects': []
        }), 500


# API: GET PROJECTS BY CATEGORY
@main.route("/api/projects")
def get_projects_api():
    """API endpoint to get projects with optional category filter"""
    try:
        from app.models.project import Project
        
        category = request.args.get('category', 'all')
        limit = request.args.get('limit', 12, type=int)
        
        # Base query
        query = Project.query.filter_by(status='published')
        
        # Filter by category if specified and not 'all'
        if category and category != 'all':
            query = query.filter_by(category=category)
        
        # Order by created_at DESC and limit
        projects = query.order_by(Project.created_at.desc()).limit(limit).all()
        
        # Format projects for JSON response
        projects_data = []
        for project in projects:
            projects_data.append({
                'id': project.id,
                'title': project.title,
                'description': project.description,
                'short_description': project.description[:120] + "..." if len(project.description) > 120 else project.description,
                'image': project.image,
                'github_link': project.github_link,
                'live_link': project.live_link,
                'technologies': project.technologies,
                'category': project.category,
                'featured': project.featured,
                'created_at': project.created_at.strftime('%b %d, %Y') if project.created_at else None
            })
        
        return jsonify({
            'success': True,
            'projects': projects_data,
            'count': len(projects_data),
            'category': category
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching projects: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch projects',
            'projects': []
        }), 500# FEEDBACK ROUTE
@main.route("/feedback", methods=["POST"])
def feedback():
    """Handle feedback form submissions and convert to testimonials"""
    try:
        from app.models.testimonial import Testimonial
        from app.extensions import db
        
        # Get form data
        client_name = request.form.get("client_name", "").strip()
        email = request.form.get("email", "").strip()
        client_position = request.form.get("client_position", "").strip()
        client_company = request.form.get("client_company", "").strip()
        project_type = request.form.get("project_type", "").strip()
        rating = int(request.form.get("rating", 5))
        quote = request.form.get("quote", "").strip()
        permission = request.form.get("permission") == "on"
        
        # Handle file upload
        avatar_filename = None
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename != '':
                # Import secure_filename for file handling
                from werkzeug.utils import secure_filename
                import os
                
                # Ensure the uploads directory exists
                upload_folder = current_app.config.get("UPLOAD_FOLDER", os.path.join(current_app.root_path, 'static', 'uploads'))
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                # Generate unique filename
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                filename = f"feedback_{name}_{int(time.time())}{ext}"
                filepath = os.path.join(upload_folder, filename)
                
                # Save the file
                file.save(filepath)
                avatar_filename = filename
        
        # Validate required fields
        if not client_name or not email or not quote:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("main.home") + "#feedback")
        
        # Map project type to icon
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
        
        project_type_icon = project_type_icons.get(project_type, "fa-laptop-code")
        
        # Create testimonial if permission granted
        if permission:
            testimonial = Testimonial(
                client_name=client_name,
                client_position=client_position,
                client_company=client_company,
                quote=quote,
                rating=rating,
                project_type=project_type,
                project_type_icon=project_type_icon,
                client_avatar=avatar_filename,
                is_active=False,  # Admin needs to approve first
                display_order=0
            )
            
            db.session.add(testimonial)
            db.session.commit()
            
            # Create admin notification message
            from app.models.message import Message
            notification = Message(
                name="System Notification",
                email="system@portfolio.com",
                subject=f"New Feedback Submission from {client_name}",
                message=f"""Client: {client_name}
Email: {email}
Position: {client_position or 'Not provided'}
Company: {client_company or 'Not provided'}
Project Type: {project_type or 'Not provided'}
Rating: {'⭐' * rating}
Avatar: {'✅ Uploaded' if avatar_filename else '❌ Not uploaded'}

Feedback:
"{quote}"

Permission to display as testimonial: {'✅ Yes' if permission else '❌ No'}

This feedback has been {'automatically converted to a testimonial and is pending admin approval.' if permission else 'received but not converted to testimonial due to permission settings.'}""".strip(),
                status="unread"
            )
            
            db.session.add(notification)
            db.session.commit()
            
            flash("Thank you for your feedback! It has been submitted and will be reviewed.", "success")
        else:
            # Just create a message notification
            from app.models.message import Message
            notification = Message(
                name="System Notification",
                email="system@portfolio.com",
                subject=f"New Feedback Submission from {client_name}",
                message=f"""Client: {client_name}
Email: {email}
Position: {client_position or 'Not provided'}
Company: {client_company or 'Not provided'}
Project Type: {project_type or 'Not provided'}
Rating: {'⭐' * rating}

Feedback:
"{quote}"

Permission to display as testimonial: {'✅ Yes' if permission else '❌ No'}

This feedback has been received but not converted to testimonial due to permission settings.""".strip(),
                status="unread"
            )
            
            db.session.add(notification)
            db.session.commit()
            
            flash("Thank you for your feedback! It has been submitted.", "success")
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            # Return JSON response for AJAX
            return jsonify({
                "success": True,
                "message": "Thank you for your feedback! It has been submitted and will be reviewed."
            })
        
        # Regular form submission - redirect with flash message
        return redirect(url_for("main.home") + "#feedback")
        
    except Exception as e:
        current_app.logger.error(f"Error processing feedback: {str(e)}")
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            # Return JSON error response for AJAX
            return jsonify({
                "success": False,
                "message": "An error occurred while submitting your feedback. Please try again."
            }), 500
        
        # Regular form submission - redirect with flash message
        flash("An error occurred while submitting your feedback. Please try again.", "error")
        return redirect(url_for("main.home") + "#feedback")
