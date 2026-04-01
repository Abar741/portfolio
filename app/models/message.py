from app.extensions import db
from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # unread, read, archived
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.Text)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.name} - {self.subject}>'
    
    def mark_as_read(self):
        """Mark message as read"""
        self.status = 'read'
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def mark_as_unread(self):
        """Mark message as unread"""
        self.status = 'unread'
        self.read_at = None
        db.session.commit()
    
    def archive(self):
        """Archive message"""
        self.status = 'archived'
        db.session.commit()
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }