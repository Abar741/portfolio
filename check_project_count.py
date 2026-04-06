#!/usr/bin/env python3
"""
Script to check the number of projects in the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.project import Project

def check_project_count():
    """Check how many projects exist in the database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get all projects
            all_projects = Project.query.all()
            print(f"Total projects in database: {len(all_projects)}")
            
            # Get published projects
            published_projects = Project.query.filter_by(status='published').all()
            print(f"Published projects: {len(published_projects)}")
            
            # Get featured projects
            featured_projects = Project.query.filter_by(featured=True, status='published').all()
            print(f"Featured projects: {len(featured_projects)}")
            
            # Show project details
            print("\nProject Details:")
            print("-" * 50)
            for i, project in enumerate(all_projects, 1):
                print(f"{i}. {project.title}")
                print(f"   Status: {project.status}")
                print(f"   Featured: {project.featured}")
                print(f"   Category: {project.category}")
                print(f"   Created: {project.created_at}")
                print()
                
        except Exception as e:
            print(f"Error checking projects: {str(e)}")

if __name__ == "__main__":
    check_project_count()
