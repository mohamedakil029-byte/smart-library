# Quick Reference Guide

## Installation & Running

```bash
# Install
pip install -r requirements.txt

# Run app
python app.py

# Run tests
python -m pytest tests/

# Run example
python example_usage.py
```

## Common API Calls

### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@lib.com","full_name":"John","role":"REQUESTER"}'
```

### Create Request
```bash
curl -X POST http://localhost:5000/api/v1/requests \
  -H "Content-Type: application/json" \
  -d '{"requester_id":1,"title":"Materials","budget":5000}'
```

### Add Item
```bash
curl -X POST http://localhost:5000/api/v1/requests/1/items \
  -H "Content-Type: application/json" \
  -d '{"title":"Book Title","item_type":"book","quantity":2}'
```

### Submit Request
```bash
curl -X POST http://localhost:5000/api/v1/requests/1/submit \
  -H "Content-Type: application/json" \
  -d '{"submitted_by_id":1}'
```

### Approve Request
```bash
curl -X POST http://localhost:5000/api/v1/requests/1/approve \
  -H "Content-Type: application/json" \
  -d '{"approver_id":2,"comments":"Approved"}'
```

### Get Analytics
```bash
curl http://localhost:5000/api/v1/analytics/summary
```

## Directory Structure

```
smart_library_request_workflow/
├── models/              Database models
├── services/            Business logic
├── workflows/           State machine & workflow
├── api/                 REST API routes
├── tests/               Tests
├── app.py               Flask app entry point
├── config.py            Configuration
└── requirements.txt     Dependencies
```

## Database Models

### User
```python
User(
    username='john_doe',
    email='john@library.com',
    full_name='John Doe',
    role=UserRole.REQUESTER,  # ADMIN, LIBRARIAN, REQUESTER, APPROVER
    department='Research'
)
```

### Request
```python
Request(
    request_number='REQ-20240406-ABC123',
    requester_id=1,
    title='Request Title',
    status=WorkflowStatus.DRAFT,  # or SUBMITTED, PENDING_APPROVAL, etc.
    priority=2,  # 1-5, 1=highest
    budget=5000,
    department='Research'
)
```

### RequestItem
```python
RequestItem(
    request_id=1,
    title='Book Title',
    item_type='book',  # book, journal, database, etc.
    author='Author Name',
    isbn='978-0-123456-78-9',
    quantity=2,
    unit_cost=45,
    justification='Needed for research'
)
```

## Workflow States

- `DRAFT` → `SUBMITTED` → `PENDING_APPROVAL` → `APPROVED` → `IN_PROGRESS` → `COMPLETED`
- `REJECTED` → (back to `DRAFT`)
- `CANCELLED` (from any state)

## User Roles

| Role | Permissions |
|------|-------------|
| ADMIN | Full access |
| LIBRARIAN | Manage items, fulfillment |
| REQUESTER | Create own requests |
| APPROVER | Approve/reject requests |

## Approval Rules

Request requires approval if:
- Items count ≥ 5
- Priority 1 or 2 (high)
- Budget > $10,000

## Python Code Examples

### Create Everything & Complete
```python
from app import create_app
from services import RequestService, UserService
from models import UserRole

app = create_app()
db = app.SessionLocal()

# Create users
user_svc = UserService(db)
requester = user_svc.create_user('alice','alice@lib.com','Alice',UserRole.REQUESTER)
approver = user_svc.create_user('bob','bob@lib.com','Bob',UserRole.APPROVER)

# Create and complete request
req_svc = RequestService(db)
req = req_svc.create_request(requester.id, 'Books', 'Need books', 2, 'Research', 5000)
req_svc.add_item_to_request(req.id, 'Book Title', 'book', 'Author', quantity=2, unit_cost=45)
req_svc.submit_request(req.id, requester.id)
req_svc.approve_request(req.id, approver.id, 'Good value')
req_svc.complete_request(req.id)

db.close()
```

### Get All Pending Approvals
```python
from models import WorkflowStatus
pending = req_svc.get_requests_by_status(WorkflowStatus.PENDING_APPROVAL)
for r in pending:
    print(f"{r.request_number}: {r.title}")
```

### Generate Report
```python
from services import AnalyticsService
analytics = AnalyticsService(db)
summary = analytics.get_requests_summary()
print(f"Total: {summary['total_requests']}")
print(f"Approval Rate: {summary['approval_rate']:.1f}%")
```

## Configuration Defaults

| Setting | Value |
|---------|-------|
| Database | SQLite (library_requests.db) |
| Port | 5000 |
| Approval Threshold | 5 items |
| High Priority | 1-2 |
| High Budget | > $10,000 |

## Environment Variables

```bash
FLASK_ENV=development              # dev/prod/testing
DATABASE_URL=sqlite:///requests.db # Database connection
ADMIN_EMAIL=admin@library.com      # Admin email
SERVICENOW_URL=https://...         # ServiceNow URL
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 404 | Not found |
| 500 | Server error |

## Notifications

```python
from services import NotificationService

notif = NotificationService()
notif.send_request_submitted_notification(email, req_num, title, req_id)
notif.flush_notifications()  # Send all pending
```

## Testing

```bash
# All tests
python -m pytest tests/ -v

# Specific test
python -m pytest tests/test_services.py::TestRequestService -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Documentation Files

- **README.md** - Full feature documentation
- **API_DOCUMENTATION.md** - Complete API reference
- **SETUP_GUIDE.md** - Installation & deployment
- **GETTING_STARTED.md** - Getting started guide
- **PROJECT_SUMMARY.md** - Project overview
- **QUICK_REFERENCE.md** - This file

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port in use | `python app.py` on port 5001 |
| Import error | `pip install -r requirements.txt` |
| DB error | Delete `library_requests.db`, restart |
| Test fail | `python -m pytest tests/ -v --tb=short` |

## File Locations

| What | Where |
|------|-------|
| Models | `models/__init__.py` |
| Services | `services/*.py` |
| Workflow | `workflows/__init__.py` |
| API Routes | `api/routes.py` |
| Tests | `tests/test_*.py` |
| Config | `config.py` |
| App | `app.py` |

## Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| RequestService | services/request_service.py | Request operations |
| UserService | services/user_service.py | User management |
| NotificationService | services/notification_service.py | Notifications |
| AnalyticsService | services/analytics_service.py | Analytics |
| RequestWorkflow | workflows/__init__.py | Workflow logic |

---

**For full documentation, see README.md and API_DOCUMENTATION.md**

**Questions? Check GETTING_STARTED.md**
