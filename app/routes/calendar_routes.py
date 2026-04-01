from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.extensions import db
from app.models.calendar_event import CalendarEvent
from app.models.message import Message
from datetime import datetime, date, timedelta
import json

calendar_bp = Blueprint('calendar', __name__, url_prefix='/admin/calendar')


@calendar_bp.route("/")
@login_required
def calendar():
    """Main calendar page"""
    # Get statistics
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get various event counts
    today_events = CalendarEvent.get_today_events()
    upcoming_events = CalendarEvent.get_upcoming_events(7)
    completed_today = len([e for e in today_events if e.status == 'completed'])
    pending_today = len([e for e in today_events if e.status == 'pending'])
    
    # Get events by type
    total_notes = len(CalendarEvent.get_events_by_type('note'))
    total_tasks = len(CalendarEvent.get_events_by_type('task'))
    total_skills = len(CalendarEvent.get_events_by_type('skill'))
    
    # Get unread messages count
    unread_count = Message.query.filter_by(status='unread').count()
    
    return render_template('admin/calendar_pro.html',
                         today_events=today_events,
                         upcoming_events=upcoming_events,
                         completed_today=completed_today,
                         pending_today=pending_today,
                         total_notes=total_notes,
                         total_tasks=total_tasks,
                         total_skills=total_skills,
                         unread_count=unread_count)


@calendar_bp.route("/events")
@login_required
def get_events():
    """API endpoint to get events for calendar"""
    try:
        # Get date range from query parameters
        start = request.args.get('start')
        end = request.args.get('end')
        
        if start and end:
            start_date = datetime.fromisoformat(start.replace('Z', '+00:00')).date()
            end_date = datetime.fromisoformat(end.replace('Z', '+00:00')).date()
        else:
            # Default to current month
            today = date.today()
            start_date = today.replace(day=1)
            if today.month == 12:
                end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        events = CalendarEvent.get_events_by_date_range(start_date, end_date)
        
        # Convert to FullCalendar format
        calendar_events = []
        for event in events:
            # Color coding based on event type and status
            color = {
                'note': '#3b82f6',  # Blue
                'task': '#ef4444',  # Red
                'skill': '#10b981'  # Green
            }.get(event.event_type, '#6b7280')
            
            # Adjust opacity for completed events
            if event.status == 'completed':
                color = color + '80'  # Add transparency
            
            calendar_events.append({
                'id': event.id,
                'title': event.title,
                'start': event.event_date.isoformat(),
                'description': event.description or '',
                'backgroundColor': color,
                'borderColor': color,
                'textColor': '#ffffff',
                'extendedProps': {
                    'event_type': event.event_type,
                    'status': event.status,
                    'priority': event.priority,
                    'description': event.description
                }
            })
        
        return jsonify(calendar_events)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calendar_bp.route("/add", methods=["POST"])
@login_required
def add_event():
    """Add new calendar event"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('event_date'):
            return jsonify({'success': False, 'message': 'Title and date are required'})
        
        # Parse date
        event_date = datetime.fromisoformat(data['event_date']).date()
        
        # Create new event
        event = CalendarEvent(
            title=data['title'],
            description=data.get('description', ''),
            event_type=data.get('event_type', 'note'),
            event_date=event_date,
            priority=data.get('priority', 'medium')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event added successfully',
            'event': event.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@calendar_bp.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    """Edit calendar event"""
    event = CalendarEvent.query.get_or_404(event_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Update event
            event.title = data.get('title', event.title)
            event.description = data.get('description', event.description)
            event.event_type = data.get('event_type', event.event_type)
            event.priority = data.get('priority', event.priority)
            
            if data.get('event_date'):
                event.event_date = datetime.fromisoformat(data['event_date']).date()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Event updated successfully',
                'event': event.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    
    return jsonify(event.to_dict())


@calendar_bp.route("/delete/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    """Delete calendar event"""
    try:
        event = CalendarEvent.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@calendar_bp.route("/complete/<int:event_id>", methods=["POST"])
@login_required
def complete_event(event_id):
    """Mark event as completed/pending"""
    try:
        event = CalendarEvent.query.get_or_404(event_id)
        
        if event.status == 'completed':
            event.mark_pending()
            message = 'Event marked as pending'
        else:
            event.mark_completed()
            message = 'Event marked as completed'
        
        return jsonify({
            'success': True,
            'message': message,
            'event': event.to_dict()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@calendar_bp.route("/list")
@login_required
def list_events():
    """List events with filtering"""
    try:
        event_type = request.args.get('type')
        status = request.args.get('status')
        search = request.args.get('search', '')
        
        # Build query
        query = CalendarEvent.query
        
        if event_type:
            query = query.filter_by(event_type=event_type)
        
        if status:
            query = query.filter_by(status=status)
        
        if search:
            query = query.filter(CalendarEvent.title.contains(search))
        
        events = query.order_by(CalendarEvent.event_date.desc()).all()
        
        return jsonify({
            'success': True,
            'events': [event.to_dict() for event in events]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@calendar_bp.route("/dashboard-stats")
@login_required
def dashboard_stats():
    """Get dashboard statistics"""
    try:
        today = date.today()
        
        # Today's stats
        today_events = CalendarEvent.get_today_events()
        today_completed = len([e for e in today_events if e.status == 'completed'])
        today_pending = len([e for e in today_events if e.status == 'pending'])
        
        # Week stats
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        week_events = CalendarEvent.get_events_by_date_range(week_start, week_end)
        week_completed = len([e for e in week_events if e.status == 'completed'])
        
        # Overall stats
        total_notes = len(CalendarEvent.get_events_by_type('note'))
        total_tasks = len(CalendarEvent.get_events_by_type('task'))
        total_skills = len(CalendarEvent.get_events_by_type('skill'))
        
        return jsonify({
            'success': True,
            'stats': {
                'today_completed': today_completed,
                'today_pending': today_pending,
                'week_completed': week_completed,
                'total_notes': total_notes,
                'total_tasks': total_tasks,
                'total_skills': total_skills
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
