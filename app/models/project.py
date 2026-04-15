from app.extensions import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200))  # Primary/featured image
    video = db.Column(db.String(200))  # Primary/featured video
    images = db.Column(db.Text)  # JSON array of additional images
    videos = db.Column(db.Text)  # JSON array of additional videos
    github_link = db.Column(db.String(200))
    live_link = db.Column(db.String(200))
    technologies = db.Column(db.Text)  # JSON string of technologies
    category = db.Column(db.String(20), default='web_dev')  # web_dev, graphic_design, video_editing
    project_type = db.Column(db.String(50))  # e.g., 'E-commerce', 'Portfolio', 'Social Media', 'Logo Design', 'Music Video', etc.
    software_used = db.Column(db.Text)  # Comma-separated list of software/tools used
    web_dev_stack = db.Column(db.Text)  # JSON: frontend, backend, database, etc.
    graphic_design_type = db.Column(db.String(50))  # Logo, Branding, Poster, etc.
    graphic_design_tools = db.Column(db.Text)  # JSON array of design tools
    video_editing_type = db.Column(db.String(50))  # Music Video, Documentary, etc.
    video_editing_software = db.Column(db.Text)  # JSON array of video editing software
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
            'images': self.images,
            'videos': self.videos,
            'github_link': self.github_link,
            'live_link': self.live_link,
            'technologies': self.technologies,
            'category': self.category,
            'project_type': self.project_type,
            'software_used': self.software_used,
            'web_dev_stack': self.web_dev_stack,
            'graphic_design_type': self.graphic_design_type,
            'graphic_design_tools': self.graphic_design_tools,
            'video_editing_type': self.video_editing_type,
            'video_editing_software': self.video_editing_software,
            'featured': self.featured,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }