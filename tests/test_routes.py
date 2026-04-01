"""Tests for application routes"""

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
        
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass')
        db.session.add(user)
        
        # Create test data
        project = Project(
            title='Test Project',
            description='A test project',
            status='published',
            featured=True
        )
        db.session.add(project)
        
        skill = Skill(name='Python', percentage=90)
        db.session.add(skill)
        
        db.session.commit()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def auth_client(app):
    """Create authenticated test client"""
    client = app.test_client()
    
    # Login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    return client


class TestMainRoutes:
    """Test cases for main routes"""
    
    def test_home_page(self, client):
        """Test home page loads correctly"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Test Project' in response.data
        assert b'Python' in response.data
    
    def test_contact_form_success(self, client):
        """Test successful contact form submission"""
        response = client.post('/contact', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message with sufficient length for validation.'
        })
        
        assert response.status_code == 302  # Redirect to home
        
        # Check message was created
        with client.application.app_context():
            message = Message.query.first()
            assert message is not None
            assert message.name == 'Test User'
            assert message.email == 'test@example.com'
    
    def test_contact_form_validation_error(self, client):
        """Test contact form validation errors"""
        # Invalid email
        response = client.post('/contact', data={
            'name': 'Test User',
            'email': 'invalid-email',
            'message': 'This is a test message with sufficient length for validation.'
        })
        
        assert response.status_code == 302  # Redirect to home
        
        # Check no message was created
        with client.application.app_context():
            message_count = Message.query.count()
            assert message_count == 0
    
    def test_projects_page(self, client):
        """Test projects page"""
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'Test Project' in response.data
    
    def test_project_detail_page(self, client):
        """Test individual project page"""
        with client.application.app_context():
            project = Project.query.first()
            
        response = client.get(f'/project/{project.id}')
        assert response.status_code == 200
        assert b'Test Project' in response.data
    
    def test_project_detail_not_found(self, client):
        """Test project detail page with non-existent project"""
        response = client.get('/project/999')
        assert response.status_code == 302  # Redirect to projects page
    
    def test_about_page(self, client):
        """Test about page"""
        response = client.get('/about')
        assert response.status_code == 200
    
    def test_api_projects_endpoint(self, client):
        """Test API projects endpoint"""
        response = client.get('/api/projects')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert len(data['data']) == 1
        assert data['data'][0]['title'] == 'Test Project'
    
    def test_api_stats_endpoint(self, client):
        """Test API stats endpoint"""
        response = client.get('/api/stats')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'projects' in data['data']
        assert 'messages' in data['data']


class TestAuthRoutes:
    """Test cases for authentication routes"""
    
    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Admin Login' in response.data
    
    def test_login_success(self, client):
        """Test successful login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        
        assert response.status_code == 302  # Redirect to admin dashboard
    
    def test_login_failure(self, client):
        """Test failed login"""
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpass'
        })
        
        assert response.status_code == 200  # Stay on login page
        assert b'Invalid' in response.data
    
    def test_logout(self, auth_client):
        """Test logout functionality"""
        response = auth_client.get('/logout')
        assert response.status_code == 302  # Redirect to login page
    
    def test_admin_requires_login(self, client):
        """Test that admin routes require authentication"""
        response = client.get('/admin/dashboard')
        assert response.status_code == 302  # Redirect to login page


class TestAdminRoutes:
    """Test cases for admin routes"""
    
    def test_admin_dashboard(self, auth_client):
        """Test admin dashboard loads"""
        response = auth_client.get('/admin/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data
    
    def test_add_project_get(self, auth_client):
        """Test add project page loads"""
        response = auth_client.get('/admin/projects/add')
        assert response.status_code == 200
        assert b'Add Project' in response.data
    
    def test_add_project_post(self, auth_client):
        """Test adding a new project"""
        response = auth_client.post('/admin/projects/add', data={
            'title': 'New Project',
            'description': 'A new test project',
            'github_link': 'https://github.com/test/new',
            'live_link': 'https://new-project.com',
            'featured': False,
            'status': 'published'
        })
        
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check project was created
        with auth_client.application.app_context():
            project = Project.query.filter_by(title='New Project').first()
            assert project is not None
            assert project.description == 'A new test project'
    
    def test_edit_project_get(self, auth_client):
        """Test edit project page loads"""
        with auth_client.application.app_context():
            project = Project.query.first()
        
        response = auth_client.get(f'/admin/projects/edit/{project.id}')
        assert response.status_code == 200
        assert b'Edit Project' in response.data
    
    def test_edit_project_post(self, auth_client):
        """Test editing a project"""
        with auth_client.application.app_context():
            project = Project.query.first()
        
        response = auth_client.post(f'/admin/projects/edit/{project.id}', data={
            'title': 'Updated Project',
            'description': 'Updated description',
            'github_link': 'https://github.com/test/updated',
            'live_link': 'https://updated-project.com',
            'featured': True,
            'status': 'published'
        })
        
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check project was updated
        with auth_client.application.app_context():
            updated_project = Project.query.get(project.id)
            assert updated_project.title == 'Updated Project'
            assert updated_project.description == 'Updated description'
    
    def test_delete_project(self, auth_client):
        """Test deleting a project"""
        with auth_client.application.app_context():
            project = Project.query.first()
            project_id = project.id
        
        response = auth_client.get(f'/admin/projects/delete/{project_id}')
        assert response.status_code == 302  # Redirect to dashboard
        
        # Check project was deleted
        with auth_client.application.app_context():
            deleted_project = Project.query.get(project_id)
            assert deleted_project is None
    
    def test_skills_page(self, auth_client):
        """Test skills management page"""
        response = auth_client.get('/admin/skills')
        assert response.status_code == 200
        assert b'Skills' in response.data
    
    def test_add_skill_post(self, auth_client):
        """Test adding a new skill"""
        response = auth_client.post('/admin/skills', data={
            'name': 'JavaScript',
            'percentage': 85
        })
        
        assert response.status_code == 302  # Redirect to skills page
        
        # Check skill was created
        with auth_client.application.app_context():
            skill = Skill.query.filter_by(name='JavaScript').first()
            assert skill is not None
            assert skill.percentage == 85
    
    def test_messages_page(self, auth_client):
        """Test messages page"""
        response = auth_client.get('/admin/messages')
        assert response.status_code == 200
        assert b'Messages' in response.data


class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/non-existent-page')
        assert response.status_code == 404
        assert b'Page Not Found' in response.data
    
    def test_500_error_simulation(self, app, client):
        """Test 500 error handling"""
        # This would require a route that intentionally raises an error
        # For now, we'll just check the error template exists
        with app.app_context():
            from flask import render_template
            error_page = render_template('errors/500.html')
            assert b'Server Error' in error_page
