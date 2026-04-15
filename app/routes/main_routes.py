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
import re

# Favicon route
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def track_visitor():
    """Track visitor statistics"""
    try:
        from app.models.visitor_stats import VisitorStats
        from app.models.visit_log import VisitLog
        from flask_limiter.util import get_remote_address
        
        ip_address = get_remote_address()
        user_agent = request.headers.get('User-Agent', '')
        
        # Track visit
        VisitorStats.increment_visit(ip_address, user_agent)
        
    except Exception as e:
        current_app.logger.error(f"Error tracking visitor: {str(e)}")

def get_navbar_data():
    """Get navbar data from JSON file or return default data with active states"""
    from flask import request
    
    navbar_data_file = os.path.join(current_app.root_path, 'static', 'data', 'navbar_data.json')
    
    # Base navbar data
    base_data = {
        "brand": {
            "logo": "/static/images/logo.png",
            "alt": "Graphic Nest",
            "url": "/#hero"
        },
        "links": [
            {"text": "Home", "url": "/#hero", "active": False},
            {"text": "About", "url": "/#about", "active": False},
            {"text": "Services", "url": "/#services", "active": False},
            {"text": "Projects", "url": "/#projects", "active": False},
            {"text": "Skills", "url": "/#skills", "active": False},
            {"text": "Testimonials", "url": "/#testimonials", "active": False},
            {"text": "Contact", "url": "/#feedback-contact-section", "active": False}
        ]
    }
    
    # Load from JSON file if exists
    if os.path.exists(navbar_data_file):
        try:
            with open(navbar_data_file, 'r') as f:
                loaded_data = json.load(f)
                # Update brand data from JSON
                if 'brand' in loaded_data:
                    base_data['brand'].update(loaded_data['brand'])
                # Update links data from JSON but preserve active states
                if 'links' in loaded_data:
                    # Replace all links with JSON data
                    base_data['links'] = []
                    for loaded_link in loaded_data['links']:
                        base_data['links'].append({
                            'text': loaded_link.get('text', ''),
                            'url': loaded_link.get('url', ''),
                            'active': False  # Will be set dynamically
                        })
        except Exception as e:
            current_app.logger.error(f"Error loading navbar data: {str(e)}")
    
    # Set active state based on current endpoint and URL hash
    if request and hasattr(request, 'endpoint') and request.endpoint:
        current_route = request.endpoint
        current_url = request.url if hasattr(request, 'url') else ''
        
        # Extract hash fragment from URL
        url_hash = ''
        if '#' in current_url:
            url_hash = current_url.split('#')[-1]
            url_hash = '#' + url_hash
        
        # Default active section based on route
        active_section = None
        
        # Map routes to navbar sections
        if current_route == 'main.home':
            # Check URL hash for home page sections
            if url_hash in ['/#about', '#about']:
                active_section = '/#about'
            elif url_hash in ['/#services', '#services']:
                active_section = '/#services'
            elif url_hash in ['/#projects', '#projects']:
                active_section = '/#projects'
            elif url_hash in ['/#skills', '#skills']:
                active_section = '/#skills'
            elif url_hash in ['/#testimonials', '#testimonials']:
                active_section = '/#testimonials'
            elif url_hash in ['/#feedback-contact-section', '#feedback-contact-section']:
                active_section = '/#feedback-contact-section'
            else:
                active_section = '/#hero'  # Default for home page
        elif current_route == 'main.portfolio':
            active_section = '/#projects'  # Portfolio page maps to projects section
        # Legal pages have no navbar sections
        
        # Set active state for matching link
        if active_section:
            for link in base_data['links']:
                if link['url'] == active_section:
                    link['active'] = True
                    break
    
    return base_data

def get_hero_data():
    """Get hero data from JSON file or return default data with dynamic stats"""
    hero_data_file = os.path.join(current_app.root_path, 'static', 'data', 'hero_data.json')
    
    # Load custom data from file if exists
    if os.path.exists(hero_data_file):
        try:
            with open(hero_data_file, 'r') as f:
                custom_data = json.load(f)
                # Return custom data if file exists and is valid
                return custom_data
        except Exception as e:
            current_app.logger.error(f"Error loading hero data: {str(e)}")
    
    # Return default data only if file doesn't exist
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
        "stats": [
            {"value": "50+", "label": "Projects"},
            {"value": "5+", "label": "Years"},
            {"value": "100%", "label": "Satisfaction"}
        ],
        "buttons": [
            {"icon": "fas fa-briefcase", "text": "View Portfolio", "url": url_for('main.portfolio'), "style": "primary"},
            {"icon": "fas fa-envelope", "text": "Get In Touch", "url": url_for('main.home') + "#feedback-contact-section", "style": "secondary"}
        ]
    }

# HOME PAGE
@main.route("/")
def home():
    """Home page with portfolio content"""
    try:
        # Import Project model
        from app.models.project import Project
        
        # Get featured projects for home page (client view)
        featured_projects = Project.query.filter_by(status='published', featured=True).order_by(Project.created_at.desc()).limit(6).all()
        
        # Use featured projects as the main projects for home page
        projects = featured_projects
        skills = SkillService.get_all_skills()
        
        # Get dynamic data
        hero_data = get_hero_data()
        navbar_data = get_navbar_data()
        
        # Get active testimonials ordered by display_order
        from app.models.testimonial import Testimonial
        testimonials = Testimonial.query.filter_by(is_active=True)\
            .order_by(Testimonial.display_order.asc(), Testimonial.created_at.desc())\
            .all()
        
        # Get testimonials stats (real-time calculation)
        from app.models.testimonials_stats import TestimonialsStats
        testimonials_stats = TestimonialsStats.get_calculated_stats()
        
        # Get About Me content
        from app.models.about_me import AboutMe
        about_me_content = AboutMe.get_active_content()
        
        # Log analytics and track visitor
        AnalyticsService.track_page_view('home', get_remote_address())
        track_visitor()
        
        return render_template("portfolio/index.html",
                             projects=projects,
                             featured_projects=featured_projects,
                             skills=skills,
                             hero_data=hero_data,
                             navbar_data=navbar_data,
                             testimonials=testimonials,
                             testimonials_stats=testimonials_stats,
                             about_me_content=about_me_content)
    
    except DatabaseError as e:
        current_app.logger.error(f"Database error on home page: {str(e)}")
        flash("Unable to load portfolio content. Please try again.", "error")
        return render_template("portfolio/index.html", 
                             projects=[], 
                             featured_projects=[], 
                             skills=[],
                             hero_data=get_hero_data(),
                             navbar_data=get_navbar_data(),
                             testimonials=[])
    except Exception as e:
        current_app.logger.error(f"Unexpected error on home page: {str(e)}")
        flash("An unexpected error occurred.", "error")
        return render_template("portfolio/index.html", 
                             projects=[], 
                             featured_projects=[], 
                             skills=[],
                             hero_data=get_hero_data(),
                             navbar_data=get_navbar_data(),
                             testimonials=[])


# CONTACT FORM
@main.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submissions"""
    try:
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
                 request.headers.get('Content-Type') == 'application/json'
        
        # Get request metadata for security logging
        ip_address = get_remote_address()
        user_agent = request.headers.get('User-Agent', '')
        
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message_text = request.form.get('message', '').strip()
        budget = request.form.get('budget', '').strip()
        newsletter = request.form.get('newsletter') == 'on'
        
        # Validate required fields
        if not name or not email or not subject or not message_text:
            error_msg = "Please fill in all required fields."
            if is_ajax:
                return jsonify({"success": False, "message": error_msg})
            flash(error_msg, "error")
            return redirect("/")
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            error_msg = "Please enter a valid email address."
            if is_ajax:
                return jsonify({"success": False, "message": error_msg})
            flash(error_msg, "error")
            return redirect("/")
        
        # Create message data
        message_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message_text,
            'budget': budget,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'newsletter_signup': newsletter
        }
        
        # Save message to database
        message = MessageService.create_message(message_data)
        
        # Log successful submission
        log_security_event('contact_form_submitted', ip_address, user_agent, 
                         f"Message from {message.name}")
        
        # Track analytics
        AnalyticsService.track_contact_form_submission(ip_address)
        
        success_msg = "Message sent successfully! We'll get back to you soon."
        if is_ajax:
            return jsonify({"success": True, "message": success_msg})
        
        flash("Message sent successfully! ", "success")
        
    except ValidationError as e:
        error_msg = str(e)
        if is_ajax:
            return jsonify({"success": False, "message": error_msg})
        flash(error_msg, "error")
        log_security_event('contact_form_validation_failed', ip_address, user_agent, str(e))
        
    except DatabaseError as e:
        error_msg = "An error occurred while saving your message. Please try again."
        if is_ajax:
            return jsonify({"success": False, "message": error_msg})
        flash(error_msg, "error")
        current_app.logger.error(f"Database error in contact form: {str(e)}")
        
    except Exception as e:
        error_msg = "An unexpected error occurred. Please try again."
        if is_ajax:
            return jsonify({"success": False, "message": error_msg})
        flash(error_msg, "error")
        current_app.logger.error(f"Unexpected error in contact form: {str(e)}")
        
    # Only redirect for non-AJAX requests
    if not is_ajax:
        return redirect("/")
    else:
        return jsonify({"success": False, "message": "Request failed"})


# LEGAL PAGES
@main.route("/privacy-policy")
def privacy_policy():
    """Privacy Policy page"""
    navbar_data = get_navbar_data()
    return render_template("portfolio/privacy_policy.html", navbar_data=navbar_data)


@main.route("/terms-of-service")
def terms_of_service():
    """Terms of Service page"""
    navbar_data = get_navbar_data()
    return render_template("portfolio/terms_of_service.html", navbar_data=navbar_data)


@main.route("/cookie-policy")
def cookie_policy():
    """Cookie Policy page"""
    navbar_data = get_navbar_data()
    return render_template("portfolio/cookie_policy.html", navbar_data=navbar_data)


@main.route("/sitemap")
def sitemap():
    """Sitemap page"""
    navbar_data = get_navbar_data()
    return render_template("portfolio/sitemap.html", navbar_data=navbar_data)


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
        
        # Track visitor
        track_visitor()
        
        return render_template("portfolio/projects.html",
                             projects=projects,
                             hero_data=get_hero_data(),
                             navbar_data=get_navbar_data())
    except Exception as e:
        current_app.logger.error(f"Error fetching projects for portfolio page: {str(e)}")
        return render_template("portfolio/projects.html",
                             projects=[],
                             hero_data=get_hero_data(),
                             navbar_data=get_navbar_data())

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
        mobile = request.form.get("mobile", "").strip()
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
                
                # Generate unique filename with message ID for proper tracking
                filename = secure_filename(file.filename)
                name, ext = os.path.splitext(filename)
                timestamp = int(time.time())
                filename = f"feedback_{name}_{timestamp}{ext}"
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
Mobile: {mobile or 'Not provided'}
Position: {client_position or 'Not provided'}
Company: {client_company or 'Not provided'}
Project Type: {project_type or 'Not provided'}
Rating: {'\u2b50' * rating}
Avatar: {avatar_filename if avatar_filename else '\u274c Not uploaded'}

Feedback:
"{quote}"

Permission to display as testimonial: {'\u2705 Yes' if permission else '\u274c No'}

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
Mobile: {mobile or 'Not provided'}
Position: {client_position or 'Not provided'}
Company: {client_company or 'Not provided'}
Project Type: {project_type or 'Not provided'}
Rating: {'⭐' * rating}
Avatar: {avatar_filename if avatar_filename else '❌ Not uploaded'}

Feedback:
"{quote}"

Permission to display as testimonial: {'✅ Yes' if permission else '❌ No'}

This feedback has been received but not converted to testimonial due to permission settings.""""".strip(),
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


# API: PAKISTAN NEWS
@main.route("/api/pakistan-news")
def get_pakistan_news():
    """API endpoint to get Pakistan news (mock data for now)"""
    try:
        # Mock news data - in production, this would fetch from a real news API
        news_data = [
            {
                "id": 1,
                "title": "Pakistan Tech Industry Sees Growth in IT Exports",
                "description": "The IT sector in Pakistan shows remarkable growth with increased exports in the current fiscal year.",
                "source": "Tech News Pakistan",
                "published_at": "2024-01-15",
                "url": "#",
                "image": "/static/images/news/tech-growth.jpg"
            },
            {
                "id": 2,
                "title": "Local Startups Receive International Funding",
                "description": "Several Pakistani startups have secured significant international investment rounds.",
                "source": "Startup Daily",
                "published_at": "2024-01-14",
                "url": "#",
                "image": "/static/images/news/startup-funding.jpg"
            },
            {
                "id": 3,
                "title": "Government Announces New Digital Initiatives",
                "description": "New policies aimed at digital transformation and e-governance have been announced.",
                "source": "Government Gazette",
                "published_at": "2024-01-13",
                "url": "#",
                "image": "/static/images/news/digital-initiatives.jpg"
            }
        ]
        
        return jsonify({
            'success': True,
            'news': news_data,
            'total': len(news_data)
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching Pakistan news: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch news',
            'news': []
        }), 500