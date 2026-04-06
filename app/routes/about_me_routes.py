from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.extensions import db
from app.models.about_me import AboutMe, AboutSkill, AboutHighlight
from flask_login import login_required, current_user
from datetime import datetime

about_me_bp = Blueprint('about_me', __name__, url_prefix='/admin/about-me')

@about_me_bp.route('/')
@login_required
def index():
    """About Me management page"""
    try:
        print("Loading About Me admin page...")
        
        # Get unread counts safely
        unread_count = 0
        feedback_unread_count = 0
        
        try:
            from app.routes.admin_routes import get_unread_messages_count
            unread_count = get_unread_messages_count()
            print(f"Unread messages count: {unread_count}")
        except Exception as e:
            print(f"Error getting unread messages count: {e}")
            unread_count = 0
        
        try:
            from app.routes.admin_routes import get_unread_feedback_count
            feedback_unread_count = get_unread_feedback_count()
            print(f"Feedback unread count: {feedback_unread_count}")
        except Exception as e:
            print(f"Error getting feedback count: {e}")
            feedback_unread_count = 0
        
        # Force create About Me content if it doesn't exist
        try:
            print("Getting or creating About Me content...")
            content = AboutMe.get_or_create_content()
            print(f"About Me content retrieved/created: {content}")
            if content:
                print(f"Content ID: {content.id}")
                print(f"Content title: {content.section_title}")
            else:
                print("Content is None!")
        except Exception as e:
            print(f"Error getting/creating content: {e}")
            content = None
        
        return render_template('admin/about_me.html', 
                             content=content,
                             unread_count=unread_count,
                             feedback_unread_count=feedback_unread_count)
    except Exception as e:
        print(f"Error in about_me index: {e}")
        import traceback
        traceback.print_exc()
        flash('Error loading About Me content. Please try again.', 'error')
        
        # Return with default content to prevent crashes
        try:
            content = AboutMe.get_or_create_content()
        except Exception as create_error:
            print(f"Error creating fallback content: {create_error}")
            content = None
            
        return render_template('admin/about_me.html', 
                             content=content,
                             unread_count=0,
                             feedback_unread_count=0)

@about_me_bp.route('/update', methods=['POST'])
@login_required
def update_content():
    """Update About Me content"""
    try:
        content = AboutMe.get_or_create_content()
        
        if content.update_from_form(request.form):
            return jsonify({
                'success': True, 
                'content': content.to_dict(),
                'message': 'Content updated successfully!'
            })
        else:
            return jsonify({
                'success': False, 
                'message': 'Error updating content'
            })
            
    except Exception as e:
        print(f"Error updating About Me content: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error updating About Me content: {str(e)}'
        }), 500

@about_me_bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():
    """Add a new skill"""
    try:
        content = AboutMe.get_or_create_content()
        
        skill = AboutSkill(
            about_me_id=content.id,
            name=request.form.get('name', '').strip(),
            icon=request.form.get('icon', '').strip(),
            display_order=request.form.get('display_order', type=int, default=0)
        )
        
        db.session.add(skill)
        db.session.commit()
        
        flash('Skill added successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Skill added successfully',
            'skill': skill.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding skill: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error adding skill: {str(e)}'
        }), 500

@about_me_bp.route('/skills/<int:skill_id>/update', methods=['POST'])
@login_required
def update_skill(skill_id):
    """Update a skill"""
    try:
        skill = AboutSkill.query.get_or_404(skill_id)
        
        skill.name = request.form.get('name', skill.name).strip()
        skill.icon = request.form.get('icon', skill.icon).strip()
        skill.display_order = request.form.get('display_order', type=int, default=skill.display_order)
        
        db.session.commit()
        
        flash('Skill updated successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Skill updated successfully',
            'skill': skill.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating skill: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error updating skill: {str(e)}'
        }), 500

@about_me_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    """Delete a skill"""
    try:
        skill = AboutSkill.query.get_or_404(skill_id)
        db.session.delete(skill)
        db.session.commit()
        
        flash('Skill deleted successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Skill deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting skill: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error deleting skill: {str(e)}'
        }), 500

@about_me_bp.route('/highlights/add', methods=['POST'])
@login_required
def add_highlight():
    """Add a new highlight"""
    try:
        content = AboutMe.get_or_create_content()
        
        highlight = AboutHighlight(
            about_me_id=content.id,
            title=request.form.get('title', '').strip(),
            description=request.form.get('description', '').strip(),
            icon=request.form.get('icon', '').strip(),
            display_order=request.form.get('display_order', type=int, default=0)
        )
        
        db.session.add(highlight)
        db.session.commit()
        
        flash('Highlight added successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Highlight added successfully',
            'highlight': highlight.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding highlight: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error adding highlight: {str(e)}'
        }), 500

@about_me_bp.route('/highlights/<int:highlight_id>/update', methods=['POST'])
@login_required
def update_highlight(highlight_id):
    """Update a highlight"""
    try:
        highlight = AboutHighlight.query.get_or_404(highlight_id)
        
        highlight.title = request.form.get('title', highlight.title).strip()
        highlight.description = request.form.get('description', highlight.description).strip()
        highlight.icon = request.form.get('icon', highlight.icon).strip()
        highlight.display_order = request.form.get('display_order', type=int, default=highlight.display_order)
        
        db.session.commit()
        
        flash('Highlight updated successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Highlight updated successfully',
            'highlight': highlight.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating highlight: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error updating highlight: {str(e)}'
        }), 500

@about_me_bp.route('/highlights/<int:highlight_id>/delete', methods=['POST'])
@login_required
def delete_highlight(highlight_id):
    """Delete a highlight"""
    try:
        highlight = AboutHighlight.query.get_or_404(highlight_id)
        db.session.delete(highlight)
        db.session.commit()
        
        flash('Highlight deleted successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Highlight deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting highlight: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error deleting highlight: {str(e)}'
        }), 500

@about_me_bp.route('/reset', methods=['POST'])
@login_required
def reset_content():
    """Reset all About Me content to defaults"""
    try:
        # Delete existing content
        AboutMe.query.delete()
        AboutSkill.query.delete()
        AboutHighlight.query.delete()
        db.session.commit()
        
        # Create new default content
        content = AboutMe.get_or_create_content()
        
        # Add default skills
        default_skills = [
            {'name': 'Frontend Development', 'icon': 'fas fa-code', 'display_order': 0},
            {'name': 'Backend Architecture', 'icon': 'fas fa-server', 'display_order': 1},
            {'name': 'UI/UX Design', 'icon': 'fas fa-paint-brush', 'display_order': 2},
            {'name': 'Mobile Development', 'icon': 'fas fa-mobile-alt', 'display_order': 3},
            {'name': 'Cloud Services', 'icon': 'fas fa-cloud', 'display_order': 4},
            {'name': 'Database Design', 'icon': 'fas fa-database', 'display_order': 5}
        ]
        
        for skill_data in default_skills:
            skill = AboutSkill(
                about_me_id=content.id,
                **skill_data
            )
            db.session.add(skill)
        
        # Add default highlights
        default_highlights = [
            {
                'title': '50+ Projects Delivered',
                'description': 'Successfully completed projects for startups and enterprises worldwide',
                'icon': 'fas fa-trophy',
                'display_order': 0
            },
            {
                'title': '30+ Happy Clients',
                'description': 'Built long-term relationships with satisfied clients across various industries',
                'icon': 'fas fa-users',
                'display_order': 1
            },
            {
                'title': '5+ Years Experience',
                'description': 'Proven track record in delivering high-quality digital solutions',
                'icon': 'fas fa-clock',
                'display_order': 2
            },
            {
                'title': '100% Satisfaction',
                'description': 'Committed to excellence and client success in every project',
                'icon': 'fas fa-heart',
                'display_order': 3
            }
        ]
        
        for highlight_data in default_highlights:
            highlight = AboutHighlight(
                about_me_id=content.id,
                **highlight_data
            )
            db.session.add(highlight)
        
        db.session.commit()
        
        flash('Content reset to defaults successfully!', 'success')
        return jsonify({
            'success': True,
            'message': 'Content reset to defaults successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error resetting content: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error resetting content: {str(e)}'
        }), 500

@about_me_bp.route('/api/content')
@login_required
def get_content_api():
    """API endpoint to get current About Me content"""
    try:
        content = AboutMe.get_or_create_content()
        return jsonify({
            'success': True,
            'content': content.to_dict()
        })
    except Exception as e:
        print(f"Error getting content API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error getting content: {str(e)}'
        }), 500

@about_me_bp.route('/api/skills')
@login_required
def get_skills_api():
    """API endpoint to get all skills"""
    try:
        content = AboutMe.get_or_create_content()
        skills = AboutSkill.query.filter_by(about_me_id=content.id, is_active=True).order_by(AboutSkill.display_order).all()
        return jsonify({
            'success': True,
            'skills': [skill.to_dict() for skill in skills]
        })
    except Exception as e:
        print(f"Error getting skills API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error getting skills: {str(e)}'
        }), 500

@about_me_bp.route('/api/highlights')
@login_required
def get_highlights_api():
    """API endpoint to get all highlights"""
    try:
        content = AboutMe.get_or_create_content()
        highlights = AboutHighlight.query.filter_by(about_me_id=content.id, is_active=True).order_by(AboutHighlight.display_order).all()
        return jsonify({
            'success': True,
            'highlights': [highlight.to_dict() for highlight in highlights]
        })
    except Exception as e:
        print(f"Error getting highlights API: {e}")
        return jsonify({
            'success': False,
            'message': f'Error getting highlights: {str(e)}'
        }), 500

@about_me_bp.route('/skills/reorder', methods=['POST'])
@login_required
def reorder_skills():
    """Reorder skills based on provided order"""
    try:
        skill_order = request.json.get('skill_order', [])
        
        for index, skill_id in enumerate(skill_order):
            skill = AboutSkill.query.get(skill_id)
            if skill:
                skill.display_order = index
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Skills reordered successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error reordering skills: {e}")
        return jsonify({
            'success': False,
            'message': f'Error reordering skills: {str(e)}'
        }), 500

@about_me_bp.route('/highlights/reorder', methods=['POST'])
@login_required
def reorder_highlights():
    """Reorder highlights based on provided order"""
    try:
        highlight_order = request.json.get('highlight_order', [])
        
        for index, highlight_id in enumerate(highlight_order):
            highlight = AboutHighlight.query.get(highlight_id)
            if highlight:
                highlight.display_order = index
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Highlights reordered successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error reordering highlights: {e}")
        return jsonify({
            'success': False,
            'message': f'Error reordering highlights: {str(e)}'
        }), 500
