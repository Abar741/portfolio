#!/usr/bin/env python3
"""
Script to add sample projects to the database for testing the Latest Projects slider
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.project import Project
from app.extensions import db

def add_sample_projects():
    """Add sample projects to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if projects already exist
        existing_projects = Project.query.filter_by(status='published').count()
        print(f"Existing published projects: {existing_projects}")
        
        if existing_projects > 0:
            print("Projects already exist. Skipping sample data creation.")
            return
        
        # Sample projects
        sample_projects = [
            {
                'title': 'E-Commerce Platform Redesign',
                'description': 'Complete overhaul of online shopping experience with modern UI/UX and improved performance. Features include responsive design, payment integration, and admin dashboard.',
                'category': 'web_dev',
                'image': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=200&fit=crop&crop=entropy&auto=format',
                'live_link': 'https://example.com/ecommerce',
                'github_link': 'https://github.com/example/ecommerce',
                'technologies': 'React, Node.js, MongoDB, Stripe',
                'featured': True,
                'status': 'published'
            },
            {
                'title': 'Mobile Banking App',
                'description': 'Secure and intuitive mobile banking solution with biometric authentication, real-time transactions, and comprehensive financial management features.',
                'category': 'mobile_dev',
                'image': 'https://images.unsplash.com/photo-1512941937609-1baa9321f0ac?w=400&h=200&fit=crop&crop=entropy&auto=format',
                'live_link': 'https://example.com/banking',
                'github_link': 'https://github.com/example/banking',
                'technologies': 'React Native, Firebase, JWT',
                'featured': True,
                'status': 'published'
            },
            {
                'title': 'Healthcare Dashboard',
                'description': 'Real-time patient monitoring system with advanced analytics and reporting. Includes appointment scheduling, medical records management, and telemedicine features.',
                'category': 'web_dev',
                'image': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400&h=200&fit=crop&crop=entropy&auto=format',
                'live_link': 'https://example.com/healthcare',
                'github_link': 'https://github.com/example/healthcare',
                'technologies': 'Vue.js, Python, PostgreSQL, Docker',
                'featured': False,
                'status': 'published'
            },
            {
                'title': 'Social Media Campaign',
                'description': 'Brand identity and digital marketing campaign for tech startup. Includes logo design, social media templates, and marketing strategy.',
                'category': 'graphic_design',
                'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=200&fit=crop&crop=entropy&auto=format',
                'live_link': 'https://example.com/campaign',
                'github_link': 'https://github.com/example/campaign',
                'technologies': 'Figma, Adobe Creative Suite, CSS',
                'featured': False,
                'status': 'published'
            },
            {
                'title': 'Video Production Suite',
                'description': 'Professional video editing and production services for corporate clients. Includes motion graphics, color grading, and post-production.',
                'category': 'video_editing',
                'image': 'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=400&h=200&fit=crop&crop=entropy&auto=format',
                'live_link': 'https://example.com/video',
                'github_link': 'https://github.com/example/video',
                'technologies': 'Premiere Pro, After Effects, DaVinci Resolve',
                'featured': False,
                'status': 'published'
            }
        ]
        
        try:
            # Add projects to database
            for project_data in sample_projects:
                project = Project(**project_data)
                db.session.add(project)
                print(f"Added project: {project.title}")
            
            db.session.commit()
            print(f"Successfully added {len(sample_projects)} sample projects to the database!")
            
            # Verify the projects were added
            total_projects = Project.query.count()
            published_projects = Project.query.filter_by(status='published').count()
            print(f"Total projects in database: {total_projects}")
            print(f"Published projects: {published_projects}")
            
        except Exception as e:
            print(f"Error adding sample projects: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_sample_projects()
