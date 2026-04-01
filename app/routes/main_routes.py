from flask import Blueprint, render_template, request, redirect, flash, jsonify, current_app
from app.services.project_service import ProjectService
from app.services.message_service import MessageService
from app.services.analytics_service import AnalyticsService
from app.services.skill_service import SkillService
from app.utils.logger import log_security_event, log_user_action
from app.utils.exceptions import ValidationError, DatabaseError
from flask_limiter.util import get_remote_address

main = Blueprint("main", __name__)

def get_hero_data():
    """Get hero data for the portfolio homepage"""
    # For now, return static data. In production, this would come from database
    return {
        "name": "Muhammad Abrar",
        "subtitle": "I transform creative ideas into exceptional digital experiences through innovative web development, stunning graphic design, and compelling video editing. Let's create something extraordinary together!",
        "profile_image": None,  # Set to URL or None for default
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
        
        # Log analytics
        AnalyticsService.track_page_view('home', get_remote_address())
        
        return render_template("portfolio/index.html",
                             projects=projects,
                             featured_projects=featured_projects,
                             skills=skills,
                             hero_data=hero_data)
    
    except DatabaseError as e:
        current_app.logger.error(f"Database error on home page: {str(e)}")
        flash("Unable to load portfolio content. Please try again.", "error")
        return render_template("portfolio/index.html", 
                             projects=[], 
                             featured_projects=[], 
                             skills=[],
                             hero_data=get_hero_data())
    except Exception as e:
        current_app.logger.error(f"Unexpected error on home page: {str(e)}")
        flash("An unexpected error occurred.", "error")
        return render_template("portfolio/index.html", 
                             projects=[], 
                             featured_projects=[], 
                             skills=[],
                             hero_data=get_hero_data())


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