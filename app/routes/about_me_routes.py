from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app.models.about_me import AboutMe, AboutSkill, AboutHighlight
from app.extensions import db

about_me_bp = Blueprint('about_me', __name__)

@about_me_bp.route('/admin/about-me', methods=['GET'])
@login_required
def about_me_admin():
    """About Me management page"""
    about_me = AboutMe.get_or_create_content()
    return render_template('admin/about_me.html', about_me=about_me)

@about_me_bp.route('/admin/about-me/update', methods=['POST'])
@login_required
def update_about_me():
    """Update About Me content"""
    about_me = AboutMe.get_or_create_content()
    
    if request.method == 'POST':
        if about_me.update_from_form(request.form):
            flash('About Me content updated successfully!', 'success')
        else:
            flash('Error updating About Me content', 'error')
    
    return redirect(url_for('about_me.about_me_admin'))

@about_me_bp.route('/admin/about-me/skills/add', methods=['POST'])
@login_required
def add_skill():
    """Add new skill"""
    about_me = AboutMe.get_or_create_content()
    
    try:
        skill_name = request.form.get('name', '').strip()
        skill_icon = request.form.get('icon', '').strip()
        
        if skill_name:
            skill = AboutSkill(
                about_me_id=about_me.id,
                name=skill_name,
                icon=skill_icon,
                display_order=len(about_me.skills)
            )
            db.session.add(skill)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Skill added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Skill name is required'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@about_me_bp.route('/admin/about-me/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    """Delete skill"""
    try:
        skill = AboutSkill.query.get(skill_id)
        if skill:
            db.session.delete(skill)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Skill deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Skill not found'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@about_me_bp.route('/admin/about-me/highlights/add', methods=['POST'])
@login_required
def add_highlight():
    """Add new highlight"""
    about_me = AboutMe.get_or_create_content()
    
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        icon = request.form.get('icon', '').strip()
        
        if title:
            highlight = AboutHighlight(
                about_me_id=about_me.id,
                title=title,
                description=description,
                icon=icon,
                display_order=len(about_me.highlights)
            )
            db.session.add(highlight)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Highlight added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Title is required'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@about_me_bp.route('/admin/about-me/highlights/<int:highlight_id>/delete', methods=['POST'])
@login_required
def delete_highlight(highlight_id):
    """Delete highlight"""
    try:
        highlight = AboutHighlight.query.get(highlight_id)
        if highlight:
            db.session.delete(highlight)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Highlight deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Highlight not found'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@about_me_bp.route('/api/about-me')
def get_about_me_api():
    """Get About Me content for frontend"""
    try:
        about_me = AboutMe.get_or_create_content()
        if about_me:
            return jsonify(about_me.to_dict())
        else:
            return jsonify({'error': 'About Me content not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

@about_me_bp.route('/api/about-me-stats')
def get_about_me_stats():
    """Get About Me statistics for frontend"""
    try:
        from app.models.project import Project
        from app.models.testimonials_stats import TestimonialsStats
        
        # Get real counts from database
        projects_count = Project.query.count()
        
        # Use TestimonialsStats model for consistency with admin panel
        testimonials_stats = TestimonialsStats.get_active_stats()
        testimonials_count = testimonials_stats.happy_clients if testimonials_stats else 0
        
        # Get About Me content if exists
        about_me = AboutMe.get_or_create_content()
        if about_me:
            stats = {
                'skills_count': testimonials_count,  # Use TestimonialsStats count
                'highlights_count': projects_count,  # Use actual projects count
                'content_enabled': {
                    'skills': about_me.skills_enabled if about_me else False,
                    'highlights': about_me.highlights_enabled if about_me else False,
                    'cta': about_me.cta_enabled if about_me else False
                },
                'last_updated': about_me.updated_at.isoformat() if about_me.updated_at else None
            }
            return jsonify(stats)
        else:
            return jsonify({
                'skills_count': testimonials_count,  # Use TestimonialsStats count
                'highlights_count': projects_count,  # Use actual projects count
                'content_enabled': {
                    'skills': False,
                    'highlights': False,
                    'cta': False
                },
                'last_updated': None
            })
    except Exception as e:
        return jsonify({'error': str(e)})
