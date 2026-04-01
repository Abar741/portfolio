"""
Sample Flask routes for dynamic hero section management
This file demonstrates how to pass dynamic data from database to the hero section
"""

from flask import Blueprint, render_template, jsonify
import json

# Create a blueprint for portfolio routes
portfolio_bp = Blueprint('portfolio', __name__)

# Sample database models (you would replace these with your actual models)
class HeroData:
    """Hero data model for database storage"""
    def __init__(self):
        self.name = "Muhammad Abrar"
        self.subtitle = "I transform creative ideas into exceptional digital experiences through innovative web development, stunning graphic design, and compelling video editing. Let's create something extraordinary together!"
        self.profile_image = None  # URL to profile image
        self.badge = {"icon": "fas fa-sparkles", "text": "Available for Projects"}
        self.roles = [
            {"icon": "fas fa-code", "title": "Web Developer"},
            {"icon": "fas fa-palette", "title": "Graphic Designer"},
            {"icon": "fas fa-video", "title": "Video Editor"}
        ]
        self.buttons = [
            {"icon": "fas fa-briefcase", "text": "View Portfolio", "url": "#projects", "style": "primary"},
            {"icon": "fas fa-envelope", "text": "Get In Touch", "url": "#contact", "style": "secondary"}
        ]
        self.stats = [
            {"value": "50+", "label": "Projects"},
            {"value": "5+", "label": "Years"},
            {"value": "100%", "label": "Satisfaction"}
        ]
        self.floating_icons = [
            {"icon_class": "fas fa-code", "label": "Web Dev", "animation": "down", "delay": 600},
            {"icon_class": "fas fa-palette", "label": "Design", "animation": "up", "delay": 700},
            {"icon_class": "fas fa-video", "label": "Video", "animation": "down", "delay": 800},
            {"icon_class": "fas fa-mobile-alt", "label": "Mobile", "animation": "up", "delay": 900},
            {"icon_class": "fas fa-camera", "label": "Photo", "animation": "down", "delay": 1000}
        ]
        self.timeline = {"title": "5+ Years Experience", "subtitle": "Professional Development"}
        self.scroll_text = "Scroll Down"
        self.show_scroll_indicator = True

@portfolio_bp.route('/')
def index():
    """Main portfolio page with dynamic hero data"""
    
    # Option 1: Load from database
    # hero_data = HeroData.query.first()  # SQLAlchemy example
    
    # Option 2: Load from JSON file
    # with open('hero_data.json', 'r') as f:
    #     hero_data = json.load(f)
    
    # Option 3: Load from environment variables or config
    # hero_data = load_hero_from_config()
    
    # For demonstration, using sample data
    hero_data = get_hero_data_from_database()
    
    return render_template('portfolio/index.html', hero_data=hero_data)

@portfolio_bp.route('/api/hero')
def get_hero_api():
    """API endpoint to get hero data as JSON"""
    hero_data = get_hero_data_from_database()
    return jsonify(hero_data)

@portfolio_bp.route('/api/hero', methods=['POST'])
def update_hero_api():
    """API endpoint to update hero data"""
    # This would update the database
    # hero_data = request.get_json()
    # save_hero_to_database(hero_data)
    return jsonify({"status": "success", "message": "Hero data updated"})

def get_hero_data_from_database():
    """Simulate loading hero data from database"""
    # In a real application, this would query your database
    # For example:
    # hero = HeroData.query.filter_by(active=True).first()
    # return hero.to_dict() if hero else None
    
    # Sample data structure
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

# Database schema examples (SQLAlchemy models)

"""
# Example SQLAlchemy models for database integration

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy()

class HeroSection(db.Model):
    __tablename__ = 'hero_section'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.Text)
    profile_image = db.Column(db.String(500))
    badge_icon = db.Column(db.String(50))
    badge_text = db.Column(db.String(100))
    roles = db.Column(JSON)  # Store roles as JSON
    buttons = db.Column(JSON)  # Store buttons as JSON
    stats = db.Column(JSON)  # Store stats as JSON
    floating_icons = db.Column(JSON)  # Store floating icons as JSON
    timeline_title = db.Column(db.String(100))
    timeline_subtitle = db.Column(db.String(100))
    scroll_text = db.Column(db.String(50))
    show_scroll_indicator = db.Column(db.Boolean, default=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'name': self.name,
            'subtitle': self.subtitle,
            'profile_image': self.profile_image,
            'badge': {
                'icon': self.badge_icon,
                'text': self.badge_text
            } if self.badge_icon and self.badge_text else None,
            'roles': self.roles or [],
            'buttons': self.buttons or [],
            'stats': self.stats or [],
            'floating_icons': self.floating_icons or [],
            'timeline': {
                'title': self.timeline_title,
                'subtitle': self.timeline_subtitle
            } if self.timeline_title and self.timeline_subtitle else None,
            'scroll_text': self.scroll_text,
            'show_scroll_indicator': self.show_scroll_indicator
        }

# Example admin interface for managing hero data

@portfolio_bp.route('/admin/hero')
def admin_hero():
    """Admin interface for managing hero section"""
    hero_data = HeroSection.query.filter_by(active=True).first()
    return render_template('admin/hero_edit.html', hero_data=hero_data)

@portfolio_bp.route('/admin/hero', methods=['POST'])
def admin_hero_update():
    """Update hero data from admin interface"""
    data = request.form.to_dict()
    
    hero = HeroSection.query.filter_by(active=True).first()
    if not hero:
        hero = HeroSection()
    
    hero.name = data.get('name', 'Muhammad Abrar')
    hero.subtitle = data.get('subtitle', '')
    hero.profile_image = data.get('profile_image', '')
    hero.badge_icon = data.get('badge_icon', 'fas fa-sparkles')
    hero.badge_text = data.get('badge_text', 'Available for Projects')
    
    # Parse JSON fields
    hero.roles = json.loads(data.get('roles', '[]'))
    hero.buttons = json.loads(data.get('buttons', '[]'))
    hero.stats = json.loads(data.get('stats', '[]'))
    hero.floating_icons = json.loads(data.get('floating_icons', '[]'))
    
    hero.timeline_title = data.get('timeline_title', '')
    hero.timeline_subtitle = data.get('timeline_subtitle', '')
    hero.scroll_text = data.get('scroll_text', 'Scroll Down')
    hero.show_scroll_indicator = data.get('show_scroll_indicator', 'true').lower() == 'true'
    hero.active = True
    
    db.session.add(hero)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "Hero section updated successfully"})
"""

# Example JSON configuration file structure

"""
hero_config.json example:

{
    "name": "Muhammad Abrar",
    "subtitle": "I transform creative ideas into exceptional digital experiences through innovative web development, stunning graphic design, and compelling video editing. Let's create something extraordinary together!",
    "profile_image": "/static/images/profile.jpg",
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
    "show_scroll_indicator": true
}
"""
