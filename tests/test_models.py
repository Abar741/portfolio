"""Tests for database models"""

import pytest
from app import create_app
from app.extensions import db
from app.models.project import Project
from app.models.message import Message
from app.models.skill import Skill
from app.models.user import User


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
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_project():
    """Create sample project for testing"""
    return Project(
        title="Test Project",
        description="A test project for unit testing",
        github_link="https://github.com/test/project",
        live_link="https://test-project.com",
        technologies='["Python", "Flask", "SQLAlchemy"]',
        featured=True,
        status="published"
    )


@pytest.fixture
def sample_message():
    """Create sample message for testing"""
    return Message(
        name="Test User",
        email="test@example.com",
        subject="Test Subject",
        message="This is a test message for unit testing.",
        ip_address="127.0.0.1",
        user_agent="Test Browser"
    )


@pytest.fixture
def sample_skill():
    """Create sample skill for testing"""
    return Skill(
        name="Python",
        percentage=90,
        category="Programming",
        description="Advanced Python programming"
    )


class TestProjectModel:
    """Test cases for Project model"""
    
    def test_project_creation(self, app, sample_project):
        """Test creating a new project"""
        with app.app_context():
            db.session.add(sample_project)
            db.session.commit()
            
            project = Project.query.first()
            assert project.title == "Test Project"
            assert project.status == "published"
            assert project.featured is True
    
    def test_project_to_dict(self, sample_project):
        """Test project serialization"""
        project_dict = sample_project.to_dict()
        
        assert project_dict['title'] == "Test Project"
        assert project_dict['description'] == "A test project for unit testing"
        assert project_dict['featured'] is True
        assert project_dict['status'] == "published"
        assert 'created_at' in project_dict
        assert 'updated_at' in project_dict
    
    def test_project_repr(self, sample_project):
        """Test project string representation"""
        repr_str = repr(sample_project)
        assert "Test Project" in repr_str


class TestMessageModel:
    """Test cases for Message model"""
    
    def test_message_creation(self, app, sample_message):
        """Test creating a new message"""
        with app.app_context():
            db.session.add(sample_message)
            db.session.commit()
            
            message = Message.query.first()
            assert message.name == "Test User"
            assert message.email == "test@example.com"
            assert message.status == "unread"
    
    def test_message_mark_as_read(self, app, sample_message):
        """Test marking message as read"""
        with app.app_context():
            db.session.add(sample_message)
            db.session.commit()
            
            message = Message.query.first()
            message.mark_as_read()
            
            assert message.status == "read"
            assert message.read_at is not None
    
    def test_message_mark_as_unread(self, app, sample_message):
        """Test marking message as unread"""
        with app.app_context():
            db.session.add(sample_message)
            db.session.commit()
            
            message = Message.query.first()
            message.mark_as_read()
            message.mark_as_unread()
            
            assert message.status == "unread"
            assert message.read_at is None
    
    def test_message_to_dict(self, sample_message):
        """Test message serialization"""
        message_dict = sample_message.to_dict()
        
        assert message_dict['name'] == "Test User"
        assert message_dict['email'] == "test@example.com"
        assert message_dict['status'] == "unread"
        assert 'created_at' in message_dict


class TestSkillModel:
    """Test cases for Skill model"""
    
    def test_skill_creation(self, app, sample_skill):
        """Test creating a new skill"""
        with app.app_context():
            db.session.add(sample_skill)
            db.session.commit()
            
            skill = Skill.query.first()
            assert skill.name == "Python"
            assert skill.percentage == 90
            assert skill.category == "Programming"
    
    def test_skill_to_dict(self, sample_skill):
        """Test skill serialization"""
        skill_dict = sample_skill.to_dict()
        
        assert skill_dict['name'] == "Python"
        assert skill_dict['percentage'] == 90
        assert skill_dict['category'] == "Programming"


class TestUserModel:
    """Test cases for User model"""
    
    def test_user_creation(self, app):
        """Test creating a new user"""
        with app.app_context():
            user = User(
                username="testuser",
                email="test@example.com"
            )
            user.set_password("testpassword")
            
            db.session.add(user)
            db.session.commit()
            
            saved_user = User.query.first()
            assert saved_user.username == "testuser"
            assert saved_user.email == "test@example.com"
            assert saved_user.check_password("testpassword")
            assert not saved_user.check_password("wrongpassword")
    
    def test_user_password_hashing(self):
        """Test password hashing and verification"""
        user = User()
        password = "testpassword123"
        
        user.set_password(password)
        assert user.password_hash is not None
        assert user.password_hash != password
        assert user.check_password(password)
        assert not user.check_password("wrongpassword")
