#!/usr/bin/env python3
"""
Script to test the /recent-projects API endpoint
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.project import Project

def test_api_endpoint():
    """Test the /recent-projects API endpoint"""
    app = create_app()
    
    with app.test_client() as client:
        try:
            # Test the API endpoint
            response = client.get('/recent-projects')
            print(f"API Response Status: {response.status_code}")
            print(f"API Response Data: {response.get_json()}")
            
            # Also check database directly
            with app.app_context():
                projects = Project.query.filter_by(status='published').order_by(Project.created_at.desc()).limit(7).all()
                print(f"\nDirect database query found {len(projects)} projects:")
                for project in projects:
                    print(f"- {project.title} (ID: {project.id}, Category: {project.category}, Status: {project.status})")
                    print(f"  Image: {project.image}")
                    print(f"  Live Link: {project.live_link}")
                    print(f"  Created: {project.created_at}")
                    print()
                    
        except Exception as e:
            print(f"Error testing API: {e}")

if __name__ == '__main__':
    test_api_endpoint()
