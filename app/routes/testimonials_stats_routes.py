from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.extensions import db
from app.models.testimonials_stats import TestimonialsStats
from flask_login import login_required, current_user
from datetime import datetime

testimonials_stats_bp = Blueprint('testimonials_stats', __name__, url_prefix='/admin/testimonials-stats')

@testimonials_stats_bp.route('/')
@login_required
def index():
    """Testimonials stats management page"""
    try:
        # Get unread counts safely with better error handling
        unread_count = 0
        feedback_unread_count = 0
        
        # Get unread messages count (using correct field)
        try:
            from app.models.message import Message
            unread_count = Message.query.filter_by(status='unread').count()
            print(f"Unread messages count: {unread_count}")
        except Exception as e:
            print(f"Error getting unread messages count: {e}")
            unread_count = 0
        
        # Get feedback count (messages with "Feedback Submission" in subject)
        try:
            from app.models.message import Message
            feedback_unread_count = Message.query.filter_by(status='unread').filter(
                Message.subject.like("%Feedback Submission%")
            ).count()
            print(f"Unread feedback count: {feedback_unread_count}")
        except Exception as e:
            print(f"Error getting feedback count: {e}")
            feedback_unread_count = 0
        
        # Get real-time stats (not cached)
        print("Getting testimonials stats...")
        stats = TestimonialsStats.get_calculated_stats()
        print(f"Stats retrieved successfully: {stats}")
        print(f"Stats type: {type(stats)}")
        
        # Ensure stats is a dictionary for template
        if hasattr(stats, 'to_dict'):
            stats_dict = stats.to_dict()
        elif isinstance(stats, dict):
            stats_dict = stats
        else:
            print(f"ERROR: Stats is unexpected type: {type(stats)}")
            # Create fallback dictionary
            stats_dict = {
                'happy_clients': 0,
                'projects_completed': 0,
                'average_rating': 5.0,
                'awards_won': 0
            }
        
        print(f"Final stats dict: {stats_dict}")
        return render_template('admin/testimonials_stats.html', 
                             stats=stats_dict,
                             unread_count=unread_count,
                             feedback_unread_count=feedback_unread_count)
                             
    except Exception as e:
        print(f"Error in testimonials stats index: {e}")
        import traceback
        traceback.print_exc()
        
        # Return default stats to prevent crashes
        default_stats = {
            'happy_clients': 0,
            'happy_clients_label': 'Happy Clients',
            'happy_clients_icon': 'fas fa-users',
            'projects_completed': 0,
            'projects_completed_label': 'Projects Completed',
            'projects_completed_icon': 'fas fa-briefcase',
            'average_rating': 5.0,
            'average_rating_label': 'Average Rating',
            'average_rating_icon': 'fas fa-star',
            'awards_won': 0,
            'awards_won_label': 'Awards Won',
            'awards_won_icon': 'fas fa-award'
        }
        
        return render_template('admin/testimonials_stats.html', 
                             stats=default_stats,
                             unread_count=0,
                             feedback_unread_count=0)

@testimonials_stats_bp.route('/update', methods=['POST'])
@login_required
def update_stats():
    """Update testimonials statistics"""
    try:
        # Get form data (only manual fields)
        average_rating = request.form.get('average_rating', type=float)
        average_rating_label = request.form.get('average_rating_label', '').strip()
        average_rating_icon = request.form.get('average_rating_icon', '').strip()
        
        awards_won = request.form.get('awards_won', type=int)
        awards_won_label = request.form.get('awards_won_label', '').strip()
        awards_won_icon = request.form.get('awards_won_icon', '').strip()
        
        print(f"🔍 DEBUG: Form data received:")
        print(f"   average_rating: {average_rating}")
        print(f"   awards_won: {awards_won}")
        print(f"   awards_won_label: {awards_won_label}")
        print(f"   awards_won_icon: {awards_won_icon}")
        
        # Get or create stats
        stats = TestimonialsStats.get_or_create_stats()
        
        # Store original awards value for debugging
        original_awards = stats.awards_won
        
        # Update ONLY manual fields (don't update database-calculated fields)
        # Happy Clients and Projects Completed remain database-calculated
        
        stats.average_rating = average_rating or 5.0
        stats.average_rating_label = average_rating_label or 'Average Rating'
        stats.average_rating_icon = average_rating_icon or 'fas fa-star'
        
        # ADD or REDUCE awards to existing value
        if awards_won is not None and awards_won != 0:
            new_total = original_awards + awards_won
            # Ensure awards don't go below 0
            if new_total < 0:
                new_total = 0
                print(f"🔍 DEBUG: Awards cannot go below 0, setting to 0")
            
            stats.awards_won = new_total
            
            if awards_won > 0:
                print(f"🔍 DEBUG: Adding {awards_won} awards to existing {original_awards} = {stats.awards_won}")
            else:
                print(f"🔍 DEBUG: Reducing {abs(awards_won)} awards from existing {original_awards} = {stats.awards_won}")
        else:
            # Keep original value if no change requested
            stats.awards_won = original_awards
            print(f"🔍 DEBUG: No change requested, keeping original value: {stats.awards_won}")
        
        stats.awards_won_label = awards_won_label or 'Awards Won'
        stats.awards_won_icon = awards_won_icon or 'fas fa-award'
        
        print(f"🔍 DEBUG: Values being saved:")
        print(f"   original_awards: {original_awards}")
        print(f"   new_awards_added: {awards_won}")
        print(f"   total_awards: {stats.awards_won}")
        print(f"   stats.average_rating: {stats.average_rating}")
        
        # Save to database
        db.session.commit()
        
        print(f"🔍 DEBUG: Values after save:")
        print(f"   stats.awards_won: {stats.awards_won}")
        print(f"   stats.average_rating: {stats.average_rating}")
        
        flash('Testimonials statistics updated successfully!', 'success')
        return jsonify({'success': True, 'message': 'Statistics updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating testimonials stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error updating statistics: {str(e)}'}), 500

@testimonials_stats_bp.route('/refresh', methods=['POST'])
@login_required
def refresh_stats():
    """Refresh testimonials statistics by recalculating from database"""
    try:
        # Get stats and force recalculation
        stats = TestimonialsStats.get_or_create_stats()
        updated_stats = stats.update_from_database()
        
        flash('Testimonials statistics refreshed successfully!', 'success')
        return jsonify({'success': True, 'message': 'Statistics refreshed', 'stats': updated_stats})
        
    except Exception as e:
        print(f"Error refreshing testimonials stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error refreshing statistics: {str(e)}'}), 500

@testimonials_stats_bp.route('/reset', methods=['POST'])
@login_required
def reset_stats():
    """Reset testimonials statistics to default values"""
    try:
        # Get or create stats
        stats = TestimonialsStats.get_or_create_stats()
        
        # Reset to default values
        stats.happy_clients = 0
        stats.happy_clients_label = 'Happy Clients'
        stats.happy_clients_icon = 'fas fa-users'
        
        stats.projects_completed = 0
        stats.projects_completed_label = 'Projects Completed'
        stats.projects_completed_icon = 'fas fa-briefcase'
        
        stats.average_rating = 5.0
        stats.average_rating_label = 'Average Rating'
        stats.average_rating_icon = 'fas fa-star'
        
        stats.awards_won = 0
        stats.awards_won_label = 'Awards Won'
        stats.awards_won_icon = 'fas fa-award'
        
        # Save to database
        db.session.commit()
        
        flash('Testimonials statistics reset to defaults!', 'success')
        return jsonify({'success': True, 'message': 'Statistics reset successfully'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error resetting testimonials stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error resetting statistics: {str(e)}'}), 500

@testimonials_stats_bp.route('/api/stats')
def get_stats_api():
    """API endpoint to get current statistics"""
    try:
        stats = TestimonialsStats.get_calculated_stats()
        return jsonify({'success': True, 'stats': stats})
        
    except Exception as e:
        print(f"Error getting stats API: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Error getting statistics: {str(e)}'}), 500
