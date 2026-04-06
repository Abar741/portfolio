from app.extensions import db
from datetime import datetime

class TestimonialsStats(db.Model):
    """Model for managing testimonials statistics displayed on the website"""
    
    __tablename__ = 'testimonials_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Happy Clients (calculated from testimonials with permission)
    happy_clients = db.Column(db.Integer, default=0, nullable=False)
    happy_clients_label = db.Column(db.String(100), default='Happy Clients', nullable=False)
    happy_clients_icon = db.Column(db.String(50), default='fas fa-users', nullable=False)
    
    # Projects Completed (calculated from published projects)
    projects_completed = db.Column(db.Integer, default=0, nullable=False)
    projects_completed_label = db.Column(db.String(100), default='Projects Completed', nullable=False)
    projects_completed_icon = db.Column(db.String(50), default='fas fa-briefcase', nullable=False)
    
    # Average Rating (calculated from testimonials with ratings)
    average_rating = db.Column(db.Float, default=5.0, nullable=False)
    average_rating_label = db.Column(db.String(100), default='Average Rating', nullable=False)
    average_rating_icon = db.Column(db.String(50), default='fas fa-star', nullable=False)
    
    # Awards Won (manually set - not calculated)
    awards_won = db.Column(db.Integer, default=0, nullable=False)
    awards_won_label = db.Column(db.String(100), default='Awards Won', nullable=False)
    awards_won_icon = db.Column(db.String(50), default='fas fa-award', nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Auto-calculation settings
    auto_calculate_clients = db.Column(db.Boolean, default=True, nullable=False)
    auto_calculate_projects = db.Column(db.Boolean, default=True, nullable=False)
    auto_calculate_rating = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<TestimonialsStats {self.id}>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'happy_clients': self.happy_clients,
            'happy_clients_label': self.happy_clients_label,
            'happy_clients_icon': self.happy_clients_icon,
            'projects_completed': self.projects_completed,
            'projects_completed_label': self.projects_completed_label,
            'projects_completed_icon': self.projects_completed_icon,
            'average_rating': float(self.average_rating),
            'average_rating_label': self.average_rating_label,
            'average_rating_icon': self.average_rating_icon,
            'awards_won': self.awards_won,
            'awards_won_label': self.awards_won_label,
            'awards_won_icon': self.awards_won_icon,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'auto_calculate_clients': self.auto_calculate_clients,
            'auto_calculate_projects': self.auto_calculate_projects,
            'auto_calculate_rating': self.auto_calculate_rating
        }
    
    @classmethod
    def get_active_stats(cls):
        """Get the active testimonials stats"""
        return cls.query.filter_by(is_active=True).first()
    
    @classmethod
    def get_or_create_stats(cls):
        """Get existing stats or create default stats if none exist"""
        try:
            stats = cls.get_active_stats()
            if not stats:
                print("Creating new testimonials stats record...")
                stats = cls(
                    happy_clients=0,
                    happy_clients_label='Happy Clients',
                    happy_clients_icon='fas fa-users',
                    projects_completed=0,
                    projects_completed_label='Projects Completed',
                    projects_completed_icon='fas fa-briefcase',
                    average_rating=5.0,
                    average_rating_label='Average Rating',
                    average_rating_icon='fas fa-star',
                    awards_won=0,
                    awards_won_label='Awards Won',
                    awards_won_icon='fas fa-award'
                )
                db.session.add(stats)
                db.session.commit()
                print("New testimonials stats record created successfully")
            
            # Auto-calculate stats if enabled
            print("Auto-calculating stats...")
            stats.calculate_auto_stats()
            print("Stats calculation completed")
            return stats
            
        except Exception as e:
            print(f"Error in get_or_create_stats: {e}")
            db.session.rollback()
            # Return a basic stats object to prevent crashes
            return cls(
                happy_clients=0,
                happy_clients_label='Happy Clients',
                happy_clients_icon='fas fa-users',
                projects_completed=0,
                projects_completed_label='Projects Completed',
                projects_completed_icon='fas fa-briefcase',
                average_rating=5.0,
                average_rating_label='Average Rating',
                average_rating_icon='fas fa-star',
                awards_won=0,
                awards_won_label='Awards Won',
                awards_won_icon='fas fa-award'
            )
    
    def calculate_auto_stats(self):
        """Automatically calculate statistics from database"""
        try:
            print("Starting auto-calculation of stats...")
            
            # Calculate Happy Clients from active testimonials
            if self.auto_calculate_clients:
                try:
                    from app.models.testimonial import Testimonial
                    # Count all active testimonials (each testimonial represents a happy client)
                    happy_clients_count = Testimonial.query.filter_by(is_active=True).count()
                    self.happy_clients = happy_clients_count
                    print(f"Happy clients calculated: {happy_clients_count} (from active testimonials)")
                except Exception as e:
                    print(f"Error calculating happy clients: {e}")
                    self.happy_clients = 0
            
            # Calculate Projects Completed from published projects
            if self.auto_calculate_projects:
                try:
                    from app.models.project import Project
                    # Count all projects with status 'published'
                    projects_count = Project.query.filter_by(status='published').count()
                    self.projects_completed = projects_count
                    print(f"Projects completed calculated: {projects_count} (from published projects)")
                except Exception as e:
                    print(f"Error calculating projects completed: {e}")
                    self.projects_completed = 0
            
            # Average Rating - KEEP MANUAL VALUE (don't calculate from database)
            # The average_rating field will be manually set by the user
            # No automatic calculation for rating - it's now a manual field like awards
            print("Average rating kept as manual value (not calculated from database)")
            
            self.updated_at = datetime.utcnow()
            db.session.commit()
            print("Auto-calculation completed successfully")
            
        except Exception as e:
            print(f"Error calculating auto stats: {e}")
            db.session.rollback()
    
    def update_from_database(self):
        """Force update all auto-calculated statistics from database"""
        self.calculate_auto_stats()
        return self.to_dict()
    
    @classmethod
    def get_calculated_stats(cls):
        """Get stats with real-time calculation from database"""
        stats = cls.get_or_create_stats()
        
        # Real-time calculation
        calculated_stats = stats.to_dict()
        
        # Override with real-time values (only for database-calculated fields)
        try:
            # Real-time Happy Clients (count of active testimonials)
            from app.models.testimonial import Testimonial
            happy_clients_count = Testimonial.query.filter_by(is_active=True).count()
            calculated_stats['happy_clients'] = happy_clients_count
            
            # Real-time Projects Completed (count of published projects)
            from app.models.project import Project
            projects_count = Project.query.filter_by(status='published').count()
            calculated_stats['projects_completed'] = projects_count
            
            # Average Rating - KEEP MANUAL VALUE (don't calculate from database)
            # The average_rating field will be manually set by the user
            # No automatic calculation for rating - it's now a manual field like awards
            
        except Exception as e:
            print(f"Error in real-time calculation: {e}")
        
        return calculated_stats
