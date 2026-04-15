from app import create_app
from app.extensions import db
from app.models.testimonial import Testimonial
from app.models.project import Project
from app.models.testimonials_stats import TestimonialsStats

app = create_app()
with app.app_context():
    print("=== Testing Stats Calculation ===")
    
    # Test direct database queries
    print("1. Direct database queries:")
    testimonial_count = Testimonial.query.filter_by(is_active=True).count()
    project_count = Project.query.filter_by(status='published').count()
    print(f"   Active testimonials: {testimonial_count}")
    print(f"   Published projects: {project_count}")
    
    # Test get_calculated_stats method
    print("\n2. Using get_calculated_stats method:")
    stats = TestimonialsStats.get_calculated_stats()
    print(f"   Stats object: {stats}")
    print(f"   Stats type: {type(stats)}")
    
    if isinstance(stats, dict):
        print(f"   Happy clients: {stats.get('happy_clients', 'NOT_FOUND')}")
        print(f"   Projects completed: {stats.get('projects_completed', 'NOT_FOUND')}")
        print(f"   Average rating: {stats.get('average_rating', 'NOT_FOUND')}")
        print(f"   Awards won: {stats.get('awards_won', 'NOT_FOUND')}")
    else:
        print("   Stats is not a dictionary!")
        print(f"   Stats attributes: {dir(stats)}")
        if hasattr(stats, 'happy_clients'):
            print(f"   Stats.happy_clients: {stats.happy_clients}")
        if hasattr(stats, 'projects_completed'):
            print(f"   Stats.projects_completed: {stats.projects_completed}")
    
    print("\n3. Testing get_or_create_stats:")
    stats2 = TestimonialsStats.get_or_create_stats()
    print(f"   get_or_create_stats result: {stats2}")
    print(f"   Type: {type(stats2)}")
    
    print("\n=== Test Complete ===")
