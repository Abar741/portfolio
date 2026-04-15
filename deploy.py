#!/usr/bin/env python3
"""
Production deployment script for Portfolio Application
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n[INFO] {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        return None

def setup_production():
    """Setup production environment"""
    print("=" * 60)
    print("PRODUCTION DEPLOYMENT SETUP")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app'):
        print("[ERROR] Please run this script from the project root directory")
        sys.exit(1)
    
    # Create production requirements
    print("\n[1/5] Creating production requirements...")
    requirements = """Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-Mail==0.9.1
Flask-Limiter==3.5.0
Werkzeug==2.3.7
email-validator==2.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.7
redis==4.6.0
python-dotenv==1.0.0
Pillow==10.0.1
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("[SUCCESS] requirements.txt created")
    
    # Create production startup script
    print("\n[2/5] Creating production startup script...")
    startup_script = """#!/usr/bin/env python3
import os
from app import create_app

# Create the app
app = create_app()

if __name__ == '__main__':
    # Use port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
    
    with open('run.py', 'w') as f:
        f.write(startup_script)
    
    print("[SUCCESS] run.py created")
    
    # Create .env template for production
    print("\n[3/5] Creating production .env template...")
    env_template = """# Production Environment Variables
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-production-secret-key-here-change-this

# Database Configuration (for production)
DATABASE_URL=sqlite:///portfolio.db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Security Settings
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=Strict
RATE_LIMIT_ENABLED=True
RATELIMIT_DEFAULT=200 per day, 50 per hour

# File Upload Settings
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,doc,docx

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/portfolio.log
"""
    
    with open('.env.production', 'w') as f:
        f.write(env_template)
    
    print("[SUCCESS] .env.production created")
    
    # Create database initialization script
    print("\n[4/5] Creating database initialization script...")
    db_init_script = '''#!/usr/bin/env python3
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
        admin_user = User.query.filter_by(username=\'admin\').first()
        
        if not admin_user:
            # Create admin user
            password_hash = hashlib.sha256(\'SecurePass123!\'.encode(\'utf-8\')).hexdigest()
            admin = User(
                username=\'admin\',
                email=\'admin@portfolio.com\',
                password_hash=password_hash,
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("[SUCCESS] Admin user created")
        else:
            print("[INFO] Admin user already exists")
        
        print("[SUCCESS] Database initialized")

if __name__ == \'__main__\':
    init_database()
'''
    
    with open('init_db.py', 'w') as f:
        f.write(db_init_script)
    
    print("[SUCCESS] init_db.py created")
    
    # Create deployment guide
    print("\n[5/5] Creating deployment guide...")
    guide = '''# PRODUCTION DEPLOYMENT GUIDE

## FREE HOSTING OPTIONS

### Option 1: PythonAnywhere (Recommended)
- Free tier available
- Built-in Flask support
- SQLite database supported
- URL: yourusername.pythonanywhere.com

### Option 2: Vercel + Render
- Vercel: Free frontend hosting
- Render: Free backend hosting
- Custom domain support

## DEPLOYMENT STEPS

### Step 1: Choose Platform
Select PythonAnywhere for easiest deployment

### Step 2: Upload Files
1. Create a PythonAnywhere account
2. Go to Web tab
3. Create new web app
4. Select Flask framework
5. Upload your project files

### Step 3: Configure Environment
1. Set up virtual environment
2. Install requirements: pip install -r requirements.txt
3. Set environment variables
4. Initialize database: python init_db.py

### Step 4: Test Deployment
1. Start web app
2. Test admin login: admin / SecurePass123!
3. Verify all features work

### Step 5: Custom Domain (Optional)
1. Upgrade to paid plan
2. Point custom domain to hosting
3. Update SSL certificate

## IMPORTANT NOTES

- Database: SQLite file will be created automatically
- Admin credentials: admin / SecurePass123!
- Files uploaded: stored in app/static/uploads/
- Backups: Regular database backups recommended
- Security: Update SECRET_KEY in production

## TROUBLESHOOTING

- 500 errors: Check logs for database issues
- Login issues: Verify admin user exists
- File uploads: Check permissions on uploads folder
- Performance: Consider PostgreSQL for high traffic
'''
    
    with open('DEPLOYMENT.md', 'w') as f:
        f.write(guide)
    
    print("[SUCCESS] DEPLOYMENT.md created")
    
    print("\n" + "=" * 60)
    print("PRODUCTION SETUP COMPLETED!")
    print("=" * 60)
    print("\nFiles created:")
    print("- requirements.txt: Production dependencies")
    print("- run.py: Production startup script")
    print("- .env.production: Environment variables template")
    print("- init_db.py: Database initialization script")
    print("- DEPLOYMENT.md: Complete deployment guide")
    
    print("\nNEXT STEPS:")
    print("1. Read DEPLOYMENT.md for detailed instructions")
    print("2. Choose your hosting platform")
    print("3. Upload files to hosting platform")
    print("4. Configure environment variables")
    print("5. Initialize database with python init_db.py")
    print("6. Test your deployment")
    
    print("\nADMIN ACCESS:")
    print("- Username: admin")
    print("- Password: SecurePass123!")
    print("- Change password after first login")

if __name__ == '__main__':
    setup_production()
