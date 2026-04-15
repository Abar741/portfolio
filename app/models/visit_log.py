"""Visit Log Model"""
from app.extensions import db
from datetime import date


class VisitLog(db.Model):
    """Model for tracking individual visits for unique visitor counting"""
    
    __tablename__ = 'visit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Visitor identification
    ip_address = db.Column(db.String(45), nullable=False, index=True)  # IPv6 compatible
    user_agent = db.Column(db.Text)
    
    # Visit tracking
    date = db.Column(db.Date, nullable=False, index=True)
    first_visit = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_visit = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Visit counts
    visit_count = db.Column(db.Integer, default=1, nullable=False)
    page_views = db.Column(db.Integer, default=1, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    def __repr__(self):
        return f"<VisitLog {self.ip_address} on {self.date}>"
    
    @classmethod
    def get_or_create_visit(cls, ip_address, user_agent=None):
        """Get or create visit log for today"""
        today = date.today()
        visit = cls.query.filter_by(
            ip_address=ip_address,
            date=today
        ).first()
        
        if visit:
            # Returning visitor
            visit.visit_count += 1
            visit.page_views += 1
            visit.last_visit = db.func.current_timestamp()
        else:
            # New visitor today
            visit = cls(
                ip_address=ip_address,
                user_agent=user_agent,
                date=today,
                visit_count=1,
                page_views=1
            )
            db.session.add(visit)
        
        db.session.commit()
        return visit
