from app import create_app
from app.extensions import db
from app.models.testimonial import Testimonial
from app.models.project import Project

app = create_app()
with app.app_context():
    # Count testimonials
    testimonial_count = Testimonial.query.filter_by(is_active=True).count()
    print(f'Active testimonials count: {testimonial_count}')
    
    # Count projects
    project_count = Project.query.filter_by(status='published').count()
    print(f'Published projects count: {project_count}')
    
    # Check all testimonials
    all_testimonials = Testimonial.query.all()
    print(f'All testimonials in database: {len(all_testimonials)}')
    
    # Check all projects
    all_projects = Project.query.all()
    print(f'All projects in database: {len(all_projects)}')
    
    # Show some project statuses
    if all_projects:
        statuses = {}
        for project in all_projects:
            status = project.status or 'None'
            statuses[status] = statuses.get(status, 0) + 1
        print(f'Project statuses: {statuses}')
