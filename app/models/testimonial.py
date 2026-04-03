"""Testimonial Model"""
from datetime import datetime
from app import db

class Testimonial(db.Model):
    """Testimonial model for client testimonials"""
    __tablename__ = 'testimonial'
    
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_position = db.Column(db.String(100), nullable=True)
    client_company = db.Column(db.String(100), nullable=True)
    client_avatar = db.Column(db.String(200), nullable=True)  # URL or filename
    quote = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)  # 1-5 stars
    project_type = db.Column(db.String(50), nullable=True)  # e.g., "Web Development"
    project_type_icon = db.Column(db.String(30), default='fa-laptop-code')  # FontAwesome icon
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Testimonial {self.client_name}>"
    
    def to_dict(self):
        """Convert testimonial to dictionary"""
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_position': self.client_position,
            'client_company': self.client_company,
            'client_avatar': self.client_avatar,
            'quote': self.quote,
            'rating': self.rating,
            'project_type': self.project_type,
            'project_type_icon': self.project_type_icon,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
