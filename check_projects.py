#!/usr/bin/env python3
"""
Debug script to check project data in the database
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.project import Project

def check_projects():
    """Check all projects in the database"""
    app = create_app()
    
    with app.app_context():
        projects = Project.query.all()
        
        print(f"Found {len(projects)} projects in database:")
        print("=" * 50)
        
        for i, project in enumerate(projects, 1):
            print(f"\nProject {i}: {project.title}")
            print(f"  ID: {project.id}")
            print(f"  Status: {project.status}")
            print(f"  Category: {project.category}")
            print(f"  Image: {project.image}")
            print(f"  Video: {project.video}")
            print(f"  Featured: {project.featured}")
            print(f"  Created: {project.created_at}")
            
            # Check if image file exists
            if project.image:
                image_path = os.path.join('app', 'static', 'uploads', project.image)
                if os.path.exists(image_path):
                    print(f"  ✅ Image file exists: {image_path}")
                else:
                    print(f"  ❌ Image file missing: {image_path}")
            else:
                print(f"  ⚠️  No image in database")
            
            # Check if video file exists
            if project.video:
                video_path = os.path.join('app', 'static', 'uploads', project.video)
                if os.path.exists(video_path):
                    print(f"  ✅ Video file exists: {video_path}")
                else:
                    print(f"  ❌ Video file missing: {video_path}")
            else:
                print(f"  ⚠️  No video in database")

if __name__ == "__main__":
    check_projects()
