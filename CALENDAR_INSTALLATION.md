# Calendar & Productivity Manager Installation Guide

## 📋 OVERVIEW
Complete Calendar & Productivity Manager system integrated into your Admin Dashboard with:
- ✅ FullCalendar.js integration
- ✅ MySQL database storage
- ✅ Notes, Tasks, and Skills management
- ✅ Professional AdminLTE-style UI
- ✅ Responsive design
- ✅ Real-time statistics

---

## 🗄️ DATABASE SETUP

### Step 1: Create Database Table
Run this SQL command in your MySQL database:

```sql
CREATE TABLE calendar_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    event_type VARCHAR(20) NOT NULL DEFAULT 'note',
    event_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(10) DEFAULT 'medium',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_event_date (event_date),
    INDEX idx_event_type (event_type),
    INDEX idx_status (status)
);
```

### Step 2: Run Flask Migration
```bash
# Initialize migration if not done
flask db init

# Create migration
flask db migrate -m "Add calendar_events table"

# Apply migration
flask db upgrade
```

---

## 📁 FILE STRUCTURE

```
portfolio_project/
├── app/
│   ├── models/
│   │   └── calendar_event.py          # ✅ Database model
│   ├── routes/
│   │   └── calendar_routes.py         # ✅ Flask routes
│   └── templates/
│       └── admin/
│           └── calendar_pro.html       # ✅ Calendar template
├── app/__init__.py                     # ✅ Updated with calendar blueprint
└── app/templates/admin/base_new.html   # ✅ Updated sidebar
```

---

## 🛠️ DEPENDENCIES

### Install Required Packages
```bash
# FullCalendar.js is loaded from CDN (no install needed)
# But ensure you have these packages:

pip install flask flask-sqlalchemy flask-login
pip install python-dateutil  # For date handling
```

### CDN Dependencies (Already in template)
- FullCalendar.js 5.11.3
- Bootstrap 5
- Font Awesome 5

---

## 🚀 ACTIVATION STEPS

### Step 1: Restart Flask App
```bash
python run.py
```

### Step 2: Access Calendar
Navigate to: `http://127.0.0.1:5000/admin/calendar`

### Step 3: Test Features
1. ✅ Click any date to add event
2. ✅ Add notes, tasks, or skills
3. ✅ Edit/delete events
4. ✅ Mark as completed
5. ✅ Filter by type
6. ✅ View statistics

---

## 🎨 FEATURES INCLUDED

### ✅ Calendar View
- **Monthly calendar** with FullCalendar.js
- **Color coding**: Blue=Notes, Red=Tasks, Green=Skills
- **Today's date** auto-highlighted
- **Click any date** to add events
- **Event tooltips** with descriptions

### ✅ Event Management
- **Add Events**: Modal form with validation
- **Edit Events**: Click any event to edit
- **Delete Events**: Confirmation dialog
- **Complete/Undo**: Toggle completion status
- **Priority Levels**: Low, Medium, High

### ✅ Dashboard Widgets
- **Today's Tasks**: Pending vs completed
- **Statistics Cards**: Notes, tasks, skills count
- **Upcoming Events**: Next 7 days
- **Quick Filters**: Filter by event type

### ✅ Advanced Features
- **Search Events**: By keyword
- **Filter by Type**: Notes, tasks, skills only
- **Filter by Status**: Completed items
- **Responsive Design**: Works on mobile/tablet
- **Professional UI**: AdminLTE-style theming

---

## 🔧 API ENDPOINTS

### Calendar Routes
```
GET  /admin/calendar/              # Main calendar page
GET  /admin/calendar/events        # Get events (JSON)
POST /admin/calendar/add           # Add new event
POST /admin/calendar/edit/<id>     # Edit event
POST /admin/calendar/delete/<id>   # Delete event
POST /admin/calendar/complete/<id> # Toggle completion
GET  /admin/calendar/list          # List with filters
GET  /admin/calendar/dashboard-stats # Dashboard statistics
```

### API Response Format
```json
{
    "success": true,
    "message": "Event added successfully",
    "event": {
        "id": 1,
        "title": "Learn Flask",
        "description": "Complete Flask tutorial",
        "event_type": "skill",
        "event_date": "2024-01-15",
        "status": "pending",
        "priority": "medium"
    }
}
```

---

## 🎯 USAGE EXAMPLES

### Adding a Learning Goal
1. Click any date on calendar
2. Fill form:
   - Title: "Learn React.js"
   - Type: "Skill to Learn"
   - Priority: "High"
   - Description: "Complete React tutorial"

### Managing Daily Tasks
1. View "Today's Events" sidebar
2. Click checkmark to complete task
3. Click edit to modify
4. Click trash to delete

### Tracking Progress
1. View statistics cards
2. Monitor completed vs pending
3. Filter by "Completed" to see progress

---

## 🔍 TROUBLESHOOTING

### Common Issues
1. **Calendar not loading**: Check FullCalendar CDN
2. **Events not saving**: Check database connection
3. **Route not found**: Ensure blueprint registered
4. **Permission denied**: Check @login_required decorator

### Debug Mode
```python
# In run.py or config
app.debug = True
```

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
flask db downgrade base
flask db upgrade
```

---

## 🎨 CUSTOMIZATION

### Change Colors
Edit `calendar_pro.html` CSS:
```css
.event-note { background: #3b82f6; }  /* Blue */
.event-task { background: #ef4444; }  /* Red */
.event-skill { background: #10b981; } /* Green */
```

### Add Event Types
1. Update model `event_type` choices
2. Add color in CSS
3. Update form dropdown

### Customize Calendar View
```javascript
// In calendar_pro.html
calendar.setOption('initialView', 'timeGridWeek'); // Week view
calendar.setOption('weekends', false); // Hide weekends
```

---

## 📱 MOBILE RESPONSIVENESS

The calendar automatically adapts to:
- 📱 **Mobile**: Touch-friendly, compact view
- 💻 **Desktop**: Full-featured interface
- 📋 **Tablet**: Optimized layout

---

## 🚀 PRODUCTION TIPS

### Security
- ✅ CSRF protection enabled
- ✅ Login required for all routes
- ✅ SQL injection protection via SQLAlchemy
- ✅ Input validation and sanitization

### Performance
- ✅ Database indexes on event_date, event_type, status
- ✅ Efficient queries with date ranges
- ✅ Lazy loading for large datasets

### Backup
```bash
# Backup calendar data
mysqldump -u username -p database_name calendar_events > calendar_backup.sql
```

---

## 🎉 READY TO USE! 🎉

Your Calendar & Productivity Manager is now fully integrated! 

**Access it at:** `/admin/calendar`

**Features available:**
- ✅ Professional calendar interface
- ✅ Complete CRUD operations
- ✅ Real-time statistics
- ✅ Mobile responsive design
- ✅ AdminLTE integration
- ✅ MySQL persistence
- ✅ Advanced filtering and search

**Start boosting your productivity today!** 🚀
