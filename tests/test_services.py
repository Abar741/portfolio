"""Tests for service layer"""

import pytest
from app import create_app
from app.extensions import db
from app.services.project_service import ProjectService
from app.services.message_service import MessageService
from app.services.skill_service import SkillService
from app.utils.exceptions import ValidationError, DatabaseError


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def sample_project_data():
    """Sample project data for testing"""
    return {
        'title': 'Test Project',
        'description': 'A test project for unit testing',
        'github_link': 'https://github.com/test/project',
        'live_link': 'https://test-project.com',
        'technologies': ['Python', 'Flask', 'SQLAlchemy'],
        'featured': True,
        'status': 'published'
    }


@pytest.fixture
def sample_message_data():
    """Sample message data for testing"""
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'subject': 'Test Subject',
        'message': 'This is a test message for unit testing.',
        'ip_address': '127.0.0.1',
        'user_agent': 'Test Browser'
    }


@pytest.fixture
def sample_skill_data():
    """Sample skill data for testing"""
    return {
        'name': 'Python',
        'percentage': 90,
        'category': 'Programming',
        'description': 'Advanced Python programming'
    }


class TestProjectService:
    """Test cases for ProjectService"""
    
    def test_create_project(self, app, sample_project_data):
        """Test creating a new project"""
        with app.app_context():
            project = ProjectService.create_project(sample_project_data)
            
            assert project.title == 'Test Project'
            assert project.status == 'published'
            assert project.featured is True
            assert project.technologies == '["Python", "Flask", "SQLAlchemy"]'
    
    def test_create_project_validation_error(self, app, sample_project_data):
        """Test project creation with invalid data"""
        with app.app_context():
            # Missing title
            invalid_data = sample_project_data.copy()
            invalid_data['title'] = ''
            
            with pytest.raises(ValidationError):
                ProjectService.create_project(invalid_data)
    
    def test_get_all_projects(self, app, sample_project_data):
        """Test getting all projects"""
        with app.app_context():
            # Create test projects
            ProjectService.create_project(sample_project_data)
            
            draft_data = sample_project_data.copy()
            draft_data['title'] = 'Draft Project'
            draft_data['status'] = 'draft'
            ProjectService.create_project(draft_data)
            
            # Get published projects
            published_projects = ProjectService.get_all_projects('published')
            assert len(published_projects) == 1
            assert published_projects[0].title == 'Test Project'
            
            # Get all projects
            all_projects = ProjectService.get_all_projects('all')
            assert len(all_projects) == 2
    
    def test_get_featured_projects(self, app, sample_project_data):
        """Test getting featured projects"""
        with app.app_context():
            # Create featured project
            ProjectService.create_project(sample_project_data)
            
            # Create non-featured project
            regular_data = sample_project_data.copy()
            regular_data['title'] = 'Regular Project'
            regular_data['featured'] = False
            ProjectService.create_project(regular_data)
            
            featured_projects = ProjectService.get_featured_projects()
            assert len(featured_projects) == 1
            assert featured_projects[0].featured is True
    
    def test_update_project(self, app, sample_project_data):
        """Test updating a project"""
        with app.app_context():
            project = ProjectService.create_project(sample_project_data)
            
            update_data = {
                'title': 'Updated Project',
                'description': 'Updated description',
                'featured': False
            }
            
            updated_project = ProjectService.update_project(project.id, update_data)
            
            assert updated_project.title == 'Updated Project'
            assert updated_project.description == 'Updated description'
            assert updated_project.featured is False
    
    def test_delete_project(self, app, sample_project_data):
        """Test deleting a project"""
        with app.app_context():
            project = ProjectService.create_project(sample_project_data)
            project_id = project.id
            
            result = ProjectService.delete_project(project_id)
            assert result is True
            
            # Verify project is deleted
            deleted_project = ProjectService.get_project_by_id(project_id)
            assert deleted_project is None
    
    def test_search_projects(self, app, sample_project_data):
        """Test searching projects"""
        with app.app_context():
            project = ProjectService.create_project(sample_project_data)
            
            # Search by title
            results = ProjectService.search_projects('Test')
            assert len(results) == 1
            assert results[0].id == project.id
            
            # Search by technology
            results = ProjectService.search_projects('Python')
            assert len(results) == 1
            
            # Search with no results
            results = ProjectService.search_projects('Nonexistent')
            assert len(results) == 0


class TestMessageService:
    """Test cases for MessageService"""
    
    def test_create_message(self, app, sample_message_data):
        """Test creating a new message"""
        with app.app_context():
            message = MessageService.create_message(sample_message_data)
            
            assert message.name == 'Test User'
            assert message.email == 'test@example.com'
            assert message.status == 'unread'
    
    def test_create_message_validation_error(self, app, sample_message_data):
        """Test message creation with invalid data"""
        with app.app_context():
            # Invalid email
            invalid_data = sample_message_data.copy()
            invalid_data['email'] = 'invalid-email'
            
            with pytest.raises(ValidationError):
                MessageService.create_message(invalid_data)
            
            # Message too short
            invalid_data = sample_message_data.copy()
            invalid_data['message'] = 'Short'
            
            with pytest.raises(ValidationError):
                MessageService.create_message(invalid_data)
    
    def test_get_unread_count(self, app, sample_message_data):
        """Test getting unread message count"""
        with app.app_context():
            # Create messages
            MessageService.create_message(sample_message_data)
            
            second_data = sample_message_data.copy()
            second_data['email'] = 'second@example.com'
            MessageService.create_message(second_data)
            
            unread_count = MessageService.get_unread_count()
            assert unread_count == 2
    
    def test_mark_as_read(self, app, sample_message_data):
        """Test marking message as read"""
        with app.app_context():
            message = MessageService.create_message(sample_message_data)
            message_id = message.id
            
            result = MessageService.mark_as_read(message_id)
            assert result is True
            
            # Verify message is marked as read
            updated_message = MessageService.get_message_by_id(message_id)
            assert updated_message.status == 'read'
            assert updated_message.read_at is not None


class TestSkillService:
    """Test cases for SkillService"""
    
    def test_create_skill(self, app, sample_skill_data):
        """Test creating a new skill"""
        with app.app_context():
            skill = SkillService.create_skill(sample_skill_data)
            
            assert skill.name == 'Python'
            assert skill.percentage == 90
            assert skill.category == 'Programming'
    
    def test_create_skill_validation_error(self, app, sample_skill_data):
        """Test skill creation with invalid data"""
        with app.app_context():
            # Invalid percentage
            invalid_data = sample_skill_data.copy()
            invalid_data['percentage'] = 150
            
            with pytest.raises(ValidationError):
                SkillService.create_skill(invalid_data)
            
            # Name too short
            invalid_data = sample_skill_data.copy()
            invalid_data['name'] = 'P'
            
            with pytest.raises(ValidationError):
                SkillService.create_skill(invalid_data)
    
    def test_get_skills_by_category(self, app, sample_skill_data):
        """Test getting skills by category"""
        with app.app_context():
            # Create skills in different categories
            SkillService.create_skill(sample_skill_data)
            
            web_data = sample_skill_data.copy()
            web_data['name'] = 'JavaScript'
            web_data['category'] = 'Web Development'
            SkillService.create_skill(web_data)
            
            programming_skills = SkillService.get_skills_by_category('Programming')
            assert len(programming_skills) == 1
            assert programming_skills[0].name == 'Python'
            
            web_skills = SkillService.get_skills_by_category('Web Development')
            assert len(web_skills) == 1
            assert web_skills[0].name == 'JavaScript'
    
    def test_get_skill_stats(self, app, sample_skill_data):
        """Test getting skill statistics"""
        with app.app_context():
            # Create multiple skills
            SkillService.create_skill(sample_skill_data)
            
            second_data = sample_skill_data.copy()
            second_data['name'] = 'JavaScript'
            second_data['percentage'] = 80
            SkillService.create_skill(second_data)
            
            stats = SkillService.get_skill_stats()
            
            assert stats['total'] == 2
            assert stats['average_percentage'] == 85.0
            assert len(stats['top_skills']) == 2
