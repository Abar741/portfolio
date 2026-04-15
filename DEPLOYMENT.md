# PRODUCTION DEPLOYMENT GUIDE

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
