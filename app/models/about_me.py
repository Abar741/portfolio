from app.extensions import db
from datetime import datetime

class AboutMe(db.Model):
    """Model for managing About Me section content"""
    
    __tablename__ = 'about_me'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Section Header
    section_title = db.Column(db.String(200), default='About Me', nullable=False)
    section_subtitle = db.Column(db.Text, default='Passionate about creating innovative digital solutions that make a difference', nullable=False)
    
    # Main Content
    main_title = db.Column(db.String(200), default='Hi, I\'m a Full-Stack Developer', nullable=False)
    main_description = db.Column(db.Text, default='I transform creative ideas into powerful digital experiences with clean code and stunning design.', nullable=False)
    
    # Story Content
    story_paragraph1 = db.Column(db.Text, default='With over 5 years of experience in web development and design, I specialize in building modern, scalable applications that solve real-world problems. My passion lies in creating intuitive user interfaces and robust backend systems that deliver exceptional results.', nullable=False)
    story_paragraph2 = db.Column(db.Text, default='I believe in the power of technology to transform businesses and improve lives. Whether it\'s a startup MVP or an enterprise solution, I bring dedication, creativity, and technical expertise to every project.', nullable=False)
    
    # Skills Section
    skills_title = db.Column(db.String(200), default='Core Expertise', nullable=False)
    skills_enabled = db.Column(db.Boolean, default=True, nullable=False)
    
    # CTA Button
    cta_text = db.Column(db.String(100), default='Let\'s Work Together', nullable=False)
    cta_icon = db.Column(db.String(50), default='fas fa-envelope', nullable=False)
    cta_link = db.Column(db.String(200), default='#contact', nullable=False)
    cta_enabled = db.Column(db.Boolean, default=True, nullable=False)
    
    # Highlights Section
    highlights_enabled = db.Column(db.Boolean, default=True, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<AboutMe {self.id}>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'section_title': self.section_title,
            'section_subtitle': self.section_subtitle,
            'main_title': self.main_title,
            'main_description': self.main_description,
            'story_paragraph1': self.story_paragraph1,
            'story_paragraph2': self.story_paragraph2,
            'skills_title': self.skills_title,
            'skills_enabled': self.skills_enabled,
            'cta_text': self.cta_text,
            'cta_icon': self.cta_icon,
            'cta_link': self.cta_link,
            'cta_enabled': self.cta_enabled,
            'highlights_enabled': self.highlights_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'skills': [skill.to_dict() for skill in self.skills],
            'highlights': [highlight.to_dict() for highlight in self.highlights]
        }
    
    @classmethod
    def get_active_content(cls):
        """Get the active About Me content"""
        return cls.query.filter_by(is_active=True).first()
    
    @classmethod
    def get_or_create_content(cls):
        """Get existing content or create default content if none exists"""
        try:
            print("AboutMe.get_or_create_content() called...")
            content = cls.get_active_content()
            print(f"Active content found: {content}")
            
            if not content:
                print("No active content found, creating new content...")
                content = cls(
                    section_title='About Me',
                    section_subtitle='Passionate about creating innovative digital solutions that make a difference',
                    main_title='Hi, I\'m a Full-Stack Developer',
                    main_description='I transform creative ideas into powerful digital experiences with clean code and stunning design.',
                    story_paragraph1='With over 5 years of experience in web development and design, I specialize in building modern, scalable applications that solve real-world problems. My passion lies in creating intuitive user interfaces and robust backend systems that deliver exceptional results.',
                    story_paragraph2='I believe in the power of technology to transform businesses and improve lives. Whether it\'s a startup MVP or an enterprise solution, I bring dedication, creativity, and technical expertise to every project.',
                    skills_title='Core Expertise',
                    skills_enabled=True,
                    cta_text='Let\'s Work Together',
                    cta_icon='fas fa-envelope',
                    cta_link='#contact',
                    cta_enabled=True,
                    highlights_enabled=True
                )
                print("Content object created, adding to session...")
                db.session.add(content)
                print("Committing to database...")
                db.session.commit()
                print(f"New content created with ID: {content.id}")
            else:
                print(f"Using existing content with ID: {content.id}")
            
            return content
            
        except Exception as e:
            print(f"Error in get_or_create_content: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            # Return a basic content object to prevent crashes
            return cls(
                section_title='About Me',
                section_subtitle='Passionate about creating innovative digital solutions that make a difference',
                main_title='Hi, I\'m a Full-Stack Developer',
                main_description='I transform creative ideas into powerful digital experiences with clean code and stunning design.',
                story_paragraph1='With over 5 years of experience in web development and design, I specialize in building modern, scalable applications that solve real-world problems. My passion lies in creating intuitive user interfaces and robust backend systems that deliver exceptional results.',
                story_paragraph2='I believe in the power of technology to transform businesses and improve lives. Whether it\'s a startup MVP or an enterprise solution, I bring dedication, creativity, and technical expertise to every project.',
                skills_title='Core Expertise',
                skills_enabled=True,
                cta_text='Let\'s Work Together',
                cta_icon='fas fa-envelope',
                cta_link='#contact',
                cta_enabled=True,
                highlights_enabled=True
            )
    
    def update_from_form(self, form_data):
        """Update content from form data"""
        try:
            # Update main content
            self.section_title = form_data.get('section_title', self.section_title)
            self.section_subtitle = form_data.get('section_subtitle', self.section_subtitle)
            self.main_title = form_data.get('main_title', self.main_title)
            self.main_description = form_data.get('main_description', self.main_description)
            self.story_paragraph1 = form_data.get('story_paragraph1', self.story_paragraph1)
            self.story_paragraph2 = form_data.get('story_paragraph2', self.story_paragraph2)
            
            # Update skills section
            self.skills_title = form_data.get('skills_title', self.skills_title)
            self.skills_enabled = form_data.get('skills_enabled', 'off') == 'on'
            
            # Update CTA
            self.cta_text = form_data.get('cta_text', self.cta_text)
            self.cta_icon = form_data.get('cta_icon', self.cta_icon)
            self.cta_link = form_data.get('cta_link', self.cta_link)
            self.cta_enabled = form_data.get('cta_enabled', 'off') == 'on'
            
            # Update highlights
            self.highlights_enabled = form_data.get('highlights_enabled', 'off') == 'on'
            
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating AboutMe: {e}")
            return False


class AboutSkill(db.Model):
    """Model for About Me skills"""
    
    __tablename__ = 'about_skills'
    
    id = db.Column(db.Integer, primary_key=True)
    about_me_id = db.Column(db.Integer, db.ForeignKey('about_me.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    about_me = db.relationship('AboutMe', backref=db.backref('skills', lazy=True, cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<AboutSkill {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'display_order': self.display_order,
            'is_active': self.is_active
        }


class AboutHighlight(db.Model):
    """Model for About Me highlights"""
    
    __tablename__ = 'about_highlights'
    
    id = db.Column(db.Integer, primary_key=True)
    about_me_id = db.Column(db.Integer, db.ForeignKey('about_me.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    about_me = db.relationship('AboutMe', backref=db.backref('highlights', lazy=True, cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f'<AboutHighlight {self.title}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'display_order': self.display_order,
            'is_active': self.is_active
        }
