"""Visitor Statistics Model"""
from app.extensions import db
from datetime import datetime, date


class VisitorStats(db.Model):
    """Model for tracking website visitor statistics"""
    
    __tablename__ = 'visitor_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Date tracking
    date = db.Column(db.Date, unique=True, nullable=False, index=True)
    
    # Visitor counts
    total_visits = db.Column(db.Integer, default=0, nullable=False)
    unique_visitors = db.Column(db.Integer, default=0, nullable=False)
    
    # Page views
    page_views = db.Column(db.Integer, default=0, nullable=False)
    
    # Additional metrics
    bounce_rate = db.Column(db.Float, default=0.0, nullable=False)
    avg_session_duration = db.Column(db.Float, default=0.0, nullable=False)  # in seconds
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<VisitorStats {self.date}: {self.total_visits} visits>"
    
    def to_dict(self):
        """Convert visitor stats to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_visits': self.total_visits,
            'unique_visitors': self.unique_visitors,
            'page_views': self.page_views,
            'bounce_rate': self.bounce_rate,
            'avg_session_duration': self.avg_session_duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_or_create_today(cls):
        """Get or create visitor stats for today"""
        today = date.today()
        stats = cls.query.filter_by(date=today).first()
        
        if not stats:
            stats = cls(
                date=today,
                total_visits=0,
                unique_visitors=0,
                page_views=0
            )
            db.session.add(stats)
            db.session.commit()
        
        return stats
    
    @classmethod
    def get_total_stats(cls):
        """Get total visitor statistics"""
        total_stats = db.session.query(
            db.func.sum(cls.total_visits).label('total_visits'),
            db.func.sum(cls.unique_visitors).label('unique_visitors'),
            db.func.sum(cls.page_views).label('page_views'),
            db.func.count(cls.id).label('days_tracked')
        ).first()
        
        return {
            'total_visits': total_stats.total_visits or 0,
            'unique_visitors': total_stats.unique_visitors or 0,
            'page_views': total_stats.page_views or 0,
            'days_tracked': total_stats.days_tracked or 0
        }
    
    @classmethod
    def get_recent_stats(cls, days=7):
        """Get visitor statistics for recent days"""
        from datetime import timedelta
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        return cls.query.filter(
            cls.date >= start_date,
            cls.date <= end_date
        ).order_by(cls.date.desc()).all()
    
    @classmethod
    def get_today_stats(cls):
        """Get today's visitor statistics"""
        return cls.get_or_create_today()
    
    @classmethod
    def increment_visit(cls, ip_address=None, user_agent=None):
        """Increment visit count for today"""
        stats = cls.get_or_create_today()
        stats.total_visits += 1
        stats.page_views += 1
        
        # Simple unique visitor tracking by IP (basic implementation)
        if ip_address:
            # This is a simplified approach - in production, you'd want more sophisticated tracking
            from app.models.visit_log import VisitLog
            today_log = VisitLog.query.filter_by(
                date=date.today(),
                ip_address=ip_address
            ).first()
            
            if not today_log:
                # New unique visitor today
                stats.unique_visitors += 1
                visit_log = VisitLog(
                    date=date.today(),
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                db.session.add(visit_log)
        
        db.session.commit()
        return stats
