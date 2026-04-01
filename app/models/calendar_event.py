from app.extensions import db
from datetime import datetime


class CalendarEvent(db.Model):
    """Calendar Event model for notes, tasks, and learning goals"""
    
    __tablename__ = 'calendar_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(20), nullable=False, default='note')  # note, task, skill
    event_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed
    priority = db.Column(db.String(10), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CalendarEvent {self.title} - {self.event_date}>'
    
    def to_dict(self):
        """Convert event to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_events_by_date_range(cls, start_date, end_date):
        """Get events within a date range"""
        return cls.query.filter(
            cls.event_date >= start_date,
            cls.event_date <= end_date
        ).order_by(cls.event_date, cls.created_at).all()
    
    @classmethod
    def get_today_events(cls):
        """Get today's events"""
        today = datetime.now().date()
        return cls.query.filter_by(event_date=today).order_by(cls.created_at).all()
    
    @classmethod
    def get_upcoming_events(cls, days=7):
        """Get upcoming events for next N days"""
        today = datetime.now().date()
        end_date = datetime.now().date()
        from datetime import timedelta
        end_date = today + timedelta(days=days)
        return cls.query.filter(
            cls.event_date >= today,
            cls.event_date <= end_date,
            cls.status == 'pending'
        ).order_by(cls.event_date, cls.priority.desc()).all()
    
    @classmethod
    def get_events_by_type(cls, event_type):
        """Get events by type (note, task, skill)"""
        return cls.query.filter_by(event_type=event_type).order_by(cls.event_date.desc()).all()
    
    def mark_completed(self):
        """Mark event as completed"""
        self.status = 'completed'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def mark_pending(self):
        """Mark event as pending"""
        self.status = 'pending'
        self.updated_at = datetime.utcnow()
        db.session.commit()
