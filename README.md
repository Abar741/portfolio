# Professional Portfolio Application

A modern, feature-rich portfolio website built with Flask that showcases professional web development skills and best practices.

## 🌟 Features

### Client-Facing Portfolio
- **Modern UI/UX**: Professional design with smooth animations and responsive layout
- **Comprehensive Sections**: About, Projects, Skills, Testimonials, Services, Contact
- **Project Showcase**: Filterable project gallery with live demos and GitHub links
- **Interactive Elements**: Animated skill bars, hover effects, and micro-interactions
- **Contact Form**: Secure form with validation and spam protection
- **SEO Optimized**: Meta tags, structured data, and search-friendly URLs

### Admin Dashboard
- **Professional Interface**: Modern admin panel with sidebar navigation
- **Content Management**: Full CRUD operations for projects, skills, and messages
- **Analytics Dashboard**: Real-time statistics and performance metrics
- **Security Features**: Rate limiting, session management, and audit logging
- **Media Management**: Secure file uploads with image optimization
- **Export Functionality**: CSV/JSON export for data analysis

### Technical Excellence
- **Service Layer Architecture**: Clean separation of concerns
- **Comprehensive Error Handling**: Graceful error management and logging
- **Security Best Practices**: Input validation, CSRF protection, secure headers
- **Testing Suite**: Unit and integration tests with pytest
- **Production Ready**: Docker containerization and deployment configs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for frontend assets, optional)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio-project.git
   cd portfolio-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_new.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   
   # Create admin user
   python create_admin.py
   ```

6. **Run the application**
   ```bash
   # Development
   python run.py
   
   # Production
   gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
   ```

7. **Access the application**
   - Portfolio: http://localhost:5000
   - Admin Panel: http://localhost:5000/login

## 📁 Project Structure

```
portfolio_project/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration management
│   ├── extensions.py            # Flask extensions
│   ├── models/                  # Database models
│   │   ├── project.py
│   │   ├── message.py
│   │   ├── skill.py
│   │   └── user.py
│   ├── routes/                  # Application routes
│   │   ├── main_routes.py
│   │   ├── admin_routes.py
│   │   └── auth_routes.py
│   ├── services/                # Business logic layer
│   │   ├── project_service.py
│   │   ├── message_service.py
│   │   ├── skill_service.py
│   │   └── analytics_service.py
│   ├── utils/                   # Utility functions
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   └── validators.py
│   ├── templates/               # Jinja2 templates
│   │   ├── portfolio/          # Client-facing templates
│   │   ├── admin/               # Admin panel templates
│   │   └── errors/              # Error pages
│   └── static/                  # Static assets
│       ├── css/
│       ├── js/
│       └── uploads/
├── tests/                       # Test suite
│   ├── test_models.py
│   ├── test_services.py
│   └── test_routes.py
├── migrations/                  # Database migrations
├── logs/                        # Application logs
├── requirements_new.txt         # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose setup
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///database.db
# For production use PostgreSQL:
# DATABASE_URL=postgresql://user:pass@localhost/dbname

# Email (for contact forms)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Analytics
GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX

# Security
RATE_LIMIT_ENABLED=True
SESSION_TIMEOUT=3600
```

### Database Setup

**SQLite (Development)**
```bash
# Default configuration works out of the box
DATABASE_URL=sqlite:///database.db
```

**PostgreSQL (Production)**
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb portfolio_db

# Create user
sudo -u postgres createuser --interactive

# Update .env
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

### Test Coverage
- Models: Database models and relationships
- Services: Business logic and validation
- Routes: HTTP endpoints and responses
- Error Handling: Exception scenarios

## 🚀 Deployment

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Database migration**
   ```bash
   docker-compose exec web flask db upgrade
   ```

### Manual Deployment

1. **Install dependencies**
   ```bash
   pip install -r requirements_new.txt
   ```

2. **Set up production environment**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret
   ```

3. **Configure web server**
   ```bash
   # Using Gunicorn
   gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
   
   # Using Nginx (reverse proxy)
   # Configure nginx.conf to proxy to Gunicorn
   ```

### Cloud Deployment

**Heroku**
```bash
# Install Heroku CLI
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret

# Deploy
git push heroku main
```

**Vercel**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

## 📊 Analytics & Monitoring

### Google Analytics
Add your GA tracking ID to `.env`:
```bash
GOOGLE_ANALYTICS_ID=GA-XXXXXXXXX
```

### Error Tracking
```bash
# Install Sentry
pip install sentry-sdk[flask]

# Add to .env
SENTRY_DSN=https://your-sentry-dsn
```

### Performance Monitoring
Built-in analytics dashboard tracks:
- Page views and unique visitors
- Contact form submissions
- Project views and interactions
- Traffic sources and device breakdown

## 🔒 Security Features

- **Input Validation**: Comprehensive form validation and sanitization
- **Rate Limiting**: Configurable rate limits to prevent abuse
- **CSRF Protection**: Cross-site request forgery prevention
- **Secure Headers**: Security headers for production
- **Session Management**: Secure session handling with timeout
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **File Upload Security**: Secure file handling and validation

## 🎨 Customization

### Theming
Edit the CSS variables in `templates/portfolio/index.html`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --dark-color: #1a202c;
    --light-color: #f7fafc;
}
```

### Adding New Sections
1. Create route in `routes/main_routes.py`
2. Add service method in `services/`
3. Create template in `templates/portfolio/`
4. Update navigation in base template

### Custom Components
- Add new models in `models/`
- Create corresponding services
- Add admin routes for management
- Update templates and styling

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Write comprehensive tests
- Update documentation

## 📝 API Documentation

### Endpoints

**Public API**
- `GET /api/projects` - Get all published projects
- `GET /api/stats` - Get portfolio statistics

**Admin API** (Requires authentication)
- `POST /admin/projects` - Create project
- `PUT /admin/projects/<id>` - Update project
- `DELETE /admin/projects/<id>` - Delete project

### Response Format
```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check database URL in .env
echo $DATABASE_URL

# Reset database
flask db reset
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements_new.txt

# Check virtual environment
which python
```

**Permission Errors**
```bash
# Fix file permissions
chmod +x run.py
chmod -R 755 static/uploads/
```

### Debug Mode
```bash
# Enable debug mode
export FLASK_DEBUG=True
export FLASK_ENV=development
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask framework and ecosystem
- Bootstrap for responsive design
- Font Awesome for icons
- AOS for scroll animations
- Contributors and testers

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: your-email@example.com
- Documentation: [Link to docs]

---

**Built with ❤️ using Flask and modern web technologies**
