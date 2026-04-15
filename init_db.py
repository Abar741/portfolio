#!/usr/bin/env python3
"""
Initialize production database
"""

import os
import sys
from app import create_app, db
from app.models.user import User
from app.models.project import Project
import hashlib

def init_database():
    """Initialize the production database"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            # Create admin user
            password_hash = hashlib.sha256('SecurePass123!'.encode('utf-8')).hexdigest()
            admin = User(
                username='admin',
                email='admin@portfolio.com',
                password_hash=password_hash,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("[SUCCESS] Admin user created")
        else:
            print("[INFO] Admin user already exists")
        
        print("[SUCCESS] Database initialized")

if __name__ == '__main__':
    init_database()
