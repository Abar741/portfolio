from app.extensions import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))
    video = db.Column(db.String(200))  # Support for video uploads
    github_link = db.Column(db.String(200))
    live_link = db.Column(db.String(200))
    technologies = db.Column(db.Text)  # JSON string of technologies
    category = db.Column(db.String(20), default='web_dev')  # web_dev, graphic_design, video_editing
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='published')  # published, draft, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'video': self.video,
            'github_link': self.github_link,
            'live_link': self.live_link,
            'technologies': self.technologies,
            'category': self.category,
            'featured': self.featured,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }