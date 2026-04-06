from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.extensions import db
from app.models.about_me import AboutMe
from datetime import datetime
import json

about_me_bp = Blueprint('about_me', __name__, url_prefix='/admin/about-me')

@about_me_bp.route("/")
@login_required
def index():
    """About Me management page"""
    try:
        # Get all About Me sections
        about_sections = AboutMe.query.order_by(AboutMe.display_order.asc(), AboutMe.created_at.desc()).all()
        
        # Get statistics
        total_sections = len(about_sections)
        active_sections = len([section for section in about_sections if section.is_active])
        
        return render_template("admin/about_me.html", 
                            about_sections=about_sections,
                            total_sections=total_sections,
                            active_sections=active_sections)
        
    except Exception as e:
        flash(f"Error loading About Me data: {str(e)}", "error")
        return render_template("admin/about_me.html", 
                            about_sections=[],
                            total_sections=0,
                            active_sections=0)

@about_me_bp.route("/create", methods=["POST"])
@login_required
def create_section():
    """Create new About Me section"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('section_title') or not data.get('section_content'):
            return jsonify({'success': False, 'message': 'Title and content are required'})
        
        # Create new section
        section = AboutMe(
            section_title=data['section_title'],
            section_content=data['section_content'],
            display_order=data.get('display_order', 0),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(section)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'About Me section created successfully',
            'section': section.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@about_me_bp.route("/update/<int:section_id>", methods=["POST"])
@login_required
def update_section(section_id):
    """Update About Me section"""
    try:
        section = AboutMe.query.get_or_404(section_id)
        data = request.get_json()
        
        # Update section
        if data.get('section_title'):
            section.section_title = data['section_title']
        if data.get('section_content'):
            section.section_content = data['section_content']
        if 'display_order' in data:
            section.display_order = data['display_order']
        if 'is_active' in data:
            section.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'About Me section updated successfully',
            'section': section.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@about_me_bp.route("/delete/<int:section_id>", methods=["POST"])
@login_required
def delete_section(section_id):
    """Delete About Me section"""
    try:
        section = AboutMe.query.get_or_404(section_id)
        db.session.delete(section)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'About Me section deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@about_me_bp.route("/toggle/<int:section_id>", methods=["POST"])
@login_required
def toggle_section(section_id):
    """Toggle About Me section active status"""
    try:
        section = AboutMe.query.get_or_404(section_id)
        section.is_active = not section.is_active
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'About Me section {"activated" if section.is_active else "deactivated"} successfully',
            'section': section.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
