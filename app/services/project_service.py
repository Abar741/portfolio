from typing import List, Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.project import Project
from app.utils.logger import logger
from app.utils.exceptions import DatabaseError, ValidationError
import json
import os
from werkzeug.utils import secure_filename


class ProjectService:
    """Service layer for project management operations"""
    
    @staticmethod
    def get_all_projects(status: str = 'published') -> List[Project]:
        """Get all projects with optional status filter"""
        try:
            query = Project.query
            if status != 'all':
                query = query.filter_by(status=status)
            return query.order_by(Project.created_at.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching projects: {str(e)}")
            raise DatabaseError("Failed to fetch projects")
    
    @staticmethod
    def get_featured_projects(limit: int = 6) -> List[Project]:
        """Get featured projects"""
        try:
            return Project.query.filter_by(
                featured=True, 
                status='published'
            ).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching featured projects: {str(e)}")
            raise DatabaseError("Failed to fetch featured projects")
    
    @staticmethod
    def get_project_by_id(project_id: int) -> Optional[Project]:
        """Get a single project by ID"""
        try:
            return Project.query.get(project_id)
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching project {project_id}: {str(e)}")
            raise DatabaseError("Failed to fetch project")
    
    @staticmethod
    def create_project(data: Dict[str, Any], image_file=None) -> Project:
        """Create a new project"""
        try:
            # Validate required fields
            if not data.get('title') or not data.get('description'):
                raise ValidationError("Title and description are required")
            
            # Handle image upload
            image_filename = None
            if image_file and image_file.filename:
                image_filename = ProjectService._handle_image_upload(image_file)
            
            # Parse technologies
            technologies = data.get('technologies', [])
            if isinstance(technologies, list):
                technologies = json.dumps(technologies)
            
            project = Project(
                title=data['title'],
                description=data['description'],
                github_link=data.get('github_link'),
                live_link=data.get('live_link'),
                image=image_filename,
                technologies=technologies,
                featured=data.get('featured', False),
                status=data.get('status', 'published')
            )
            
            db.session.add(project)
            db.session.commit()
            
            logger.info(f"Created new project: {project.title}")
            return project
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error creating project: {str(e)}")
            raise DatabaseError("Failed to create project")
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}")
            raise
    
    @staticmethod
    def update_project(project_id: int, data: Dict[str, Any], image_file=None) -> Project:
        """Update an existing project"""
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValidationError("Project not found")
            
            # Update fields
            if 'title' in data:
                project.title = data['title']
            if 'description' in data:
                project.description = data['description']
            if 'github_link' in data:
                project.github_link = data['github_link']
            if 'live_link' in data:
                project.live_link = data['live_link']
            if 'featured' in data:
                project.featured = data['featured']
            if 'status' in data:
                project.status = data['status']
            
            # Handle technologies
            if 'technologies' in data:
                technologies = data['technologies']
                if isinstance(technologies, list):
                    technologies = json.dumps(technologies)
                project.technologies = technologies
            
            # Handle image update
            if image_file and image_file.filename:
                # Delete old image
                if project.image:
                    ProjectService._delete_image(project.image)
                
                # Upload new image
                project.image = ProjectService._handle_image_upload(image_file)
            
            db.session.commit()
            
            logger.info(f"Updated project: {project.title}")
            return project
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error updating project {project_id}: {str(e)}")
            raise DatabaseError("Failed to update project")
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {str(e)}")
            raise
    
    @staticmethod
    def delete_project(project_id: int) -> bool:
        """Delete a project"""
        try:
            project = Project.query.get(project_id)
            if not project:
                raise ValidationError("Project not found")
            
            # Delete associated image
            if project.image:
                ProjectService._delete_image(project.image)
            
            db.session.delete(project)
            db.session.commit()
            
            logger.info(f"Deleted project: {project.title}")
            return True
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error deleting project {project_id}: {str(e)}")
            raise DatabaseError("Failed to delete project")
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {str(e)}")
            raise
    
    @staticmethod
    def search_projects(query: str, limit: int = 10) -> List[Project]:
        """Search projects by title or description"""
        try:
            return Project.query.filter(
                Project.status == 'published',
                db.or_(
                    Project.title.contains(query),
                    Project.description.contains(query),
                    Project.technologies.contains(query)
                )
            ).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Database error searching projects: {str(e)}")
            raise DatabaseError("Failed to search projects")
    
    @staticmethod
    def _handle_image_upload(image_file) -> str:
        """Handle image file upload"""
        try:
            filename = secure_filename(image_file.filename)
            upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            file_path = os.path.join(upload_folder, filename)
            image_file.save(file_path)
            
            return filename
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            raise ValidationError("Failed to upload image")
    
    @staticmethod
    def _delete_image(filename: str) -> bool:
        """Delete an image file"""
        try:
            upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
            file_path = os.path.join(upload_folder, filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting image {filename}: {str(e)}")
            return False
    
    @staticmethod
    def get_project_stats() -> Dict[str, Any]:
        """Get project statistics"""
        try:
            total = Project.query.count()
            published = Project.query.filter_by(status='published').count()
            featured = Project.query.filter_by(featured=True).count()
            
            return {
                'total': total,
                'published': published,
                'drafts': total - published,
                'featured': featured
            }
        except SQLAlchemyError as e:
            logger.error(f"Database error getting project stats: {str(e)}")
            raise DatabaseError("Failed to get project statistics")
