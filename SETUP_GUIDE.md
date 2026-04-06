# Smart Library Request Workflow - Setup Guide

## Quick Start

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment (Optional)
Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
FLASK_ENV=development
DATABASE_URL=sqlite:///library_requests.db
ADMIN_EMAIL=admin@library.com
SERVICENOW_URL=https://dev.service-now.com
SERVICENOW_USER=integration_user
```

### Step 3: Run the Application
```bash
python app.py
```

The API will start on `http://localhost:5000`

### Step 4: Verify Installation
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Smart Library Request Workflow"
}
```

## Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### Specific Test File
```bash
python -m pytest tests/test_services.py -v
```

### With Coverage
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## Project Initialization

### Initialize Database
The database is automatically initialized on first run with SQLite. For production, configure DATABASE_URL in config.py:

```python
# PostgreSQL example
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/library_requests'

# MySQL example
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost:3306/library_requests'
```

## Creating Initial Data

```python
# Run this in Python shell or create a script
from app import create_app
from services import UserService
from models import UserRole

app = create_app()
db = app.SessionLocal()
user_service = UserService(db)

# Create admin
admin = user_service.create_user(
    username='admin',
    email='admin@library.com',
    full_name='Administrator',
    role=UserRole.ADMIN
)

# Create sample approver
approver = user_service.create_user(
    username='approver',
    email='approver@library.com',
    full_name='Approval Manager',
    role=UserRole.APPROVER
)

db.close()
print("Initial users created successfully!")
```

## Development Workflow

1. **Make Changes**: Edit source files in the package
2. **Run Tests**: `python -m pytest tests/`
3. **Check Errors**: Application will report any errors
4. **Test Manually**: Use cURL or Postman with API endpoints

## Production Deployment

### Environment Setup
```bash
export FLASK_ENV=production
export DATABASE_URL=your_production_db_url
export SECRET_KEY=your_secret_key_here
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

Build and run:
```bash
docker build -t library-request-workflow .
docker run -p 5000:5000 library-request-workflow
```

## Troubleshooting

### Issue: Database Connection Error
**Solution**: Check DATABASE_URL in config.py or .env file

### Issue: Module Import Errors
**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port 5000 Already in Use
**Solution**: Use a different port:
```bash
python -c "from app import create_app; app = create_app(); app.run(port=5001)"
```

### Issue: Tests Failing
**Solution**: Make sure SQLAlchemy and test dependencies are installed:
```bash
pip install pytest pytest-cov
python -m pytest tests/ -v
```

## Architecture Overview

```
Request Lifecycle:
  1. User creates Request (DRAFT)
  2. User adds RequestItems
  3. User submits Request
  4. System evaluates if approval needed
  5. if: -> PENDING_APPROVAL -> Approver reviews -> APPROVED/REJECTED
     else: -> IN_PROGRESS
  6. APPROVED -> IN_PROGRESS
  7. IN_PROGRESS -> COMPLETED

Approval Rules:
  - Items >= 5: Requires approval
  - Priority 1-2: Requires approval
  - Budget > $10,000: Requires approval
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  email VARCHAR(100) UNIQUE,
  full_name VARCHAR(200),
  role VARCHAR(20),  -- admin, librarian, requester, approver
  department VARCHAR(100),
  is_active BOOLEAN,
  created_at DATETIME,
  updated_at DATETIME
);
```

### Requests Table
```sql
CREATE TABLE requests (
  id INTEGER PRIMARY KEY,
  request_number VARCHAR(50) UNIQUE,
  requester_id INTEGER FK users,
  status VARCHAR(20),
  title VARCHAR(200),
  description TEXT,
  priority INTEGER,
  department VARCHAR(100),
  budget INTEGER,
  created_at DATETIME,
  submitted_at DATETIME,
  completed_at DATETIME,
  updated_at DATETIME
);
```

### RequestItems Table
```sql
CREATE TABLE request_items (
  id INTEGER PRIMARY KEY,
  request_id INTEGER FK requests,
  title VARCHAR(300),
  item_type VARCHAR(50),
  author VARCHAR(200),
  isbn VARCHAR(20),
  quantity INTEGER,
  unit_cost INTEGER,
  justification TEXT,
  created_at DATETIME
);
```

## Configuration Reference

### config.py Settings
```python
DEBUG = False  # Set True for development
TESTING = False  # Set True for testing

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///library_requests.db'

# Request defaults
REQUEST_TIMEOUT = timedelta(days=30)
APPROVAL_REQUIRED_THRESHOLD = 5

# Notifications
NOTIFICATION_ENABLED = True
ADMIN_EMAIL = 'admin@library.com'

# ServiceNow
SERVICENOW_URL = 'https://dev.service-now.com'
```

## API Testing

### Using Postman
1. Import API endpoints into Postman collection
2. Create environment variables for base_url, requester_id, etc.
3. Test each endpoint with sample data

### Using Python Requests
```python
import requests

BASE_URL = 'http://localhost:5000/api/v1'

# Create request
response = requests.post(f'{BASE_URL}/requests', json={
    'requester_id': 1,
    'title': 'Test Request',
    'budget': 5000
})

print(response.json())
```

## Next Steps

1. [ ] Set up authentication (JWT)
2. [ ] Configure email notifications
3. [ ] Integrate with ServiceNow
4. [ ] Deploy to production environment
5. [ ] Set up monitoring and logging
6. [ ] Create admin dashboard UI

## Support & Documentation

- **API Docs**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **README**: See [README.md](README.md)
- **Issues**: Check troubleshooting section above

---
Last Updated: April 6, 2024
