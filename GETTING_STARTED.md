# Getting Started - Smart Library Request Workflow

Welcome to the Smart Library Request Workflow project! This guide will help you get up and running in minutes.

## 1. First Time Setup (5 minutes)

### Step 1: Install Python Dependencies
```bash
cd "d:\NM Project\smart_library_request_workflow"
pip install -r requirements.txt
```

### Step 2: Start the Application
```bash
python app.py
```

You should see output similar to:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3: Verify it's Working
Open a new terminal and run:
```bash
curl http://localhost:5000/health
```

You should get:
```json
{
  "status": "healthy",
  "service": "Smart Library Request Workflow"
}
```

✓ Congratulations! The application is running.

## 2. Try the Example (5 minutes)

While the app is running, open a new terminal and execute:
```bash
python example_usage.py
```

This will demonstrate:
- Creating users with different roles
- Creating library requests
- Adding items to requests
- Submitting requests for approval
- Approving requests
- Generating analytics
- Sending notifications

## 3. Make Your First API Call (2 minutes)

### Create a User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@library.com",
    "full_name": "John Doe",
    "role": "REQUESTER",
    "department": "Research"
  }'
```

Expected response:
```json
{
  "status": "success",
  "message": "User created",
  "user_id": 1
}
```

### Create a Request
```bash
curl -X POST http://localhost:5000/api/v1/requests \
  -H "Content-Type: application/json" \
  -d '{
    "requester_id": 1,
    "title": "Research Materials",
    "description": "Need materials for spring semester",
    "priority": 2,
    "budget": 5000,
    "department": "Research"
  }'
```

### Get Request Details
Replace `{request_id}` with the ID from the previous response:
```bash
curl http://localhost:5000/api/v1/requests/1
```

### Get Analytics
```bash
curl http://localhost:5000/api/v1/analytics/summary
```

## 4. Run Tests (2 minutes)

```bash
python -m pytest tests/ -v
```

Expected output:
```
tests/test_services.py::TestRequestService::test_create_request PASSED
tests/test_services.py::TestWorkflow::test_valid_transitions PASSED
tests/test_integration.py::TestWorkflowIntegration::test_complete_workflow PASSED
...
```

## 5. Explore the Codebase

### Key Files to Review

**Start here:**
1. [README.md](README.md) - Project overview
2. [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Full API reference

**Then explore:**
3. [models/__init__.py](models/__init__.py) - Database models
4. [services/request_service.py](services/request_service.py) - Request logic
5. [workflows/__init__.py](workflows/__init__.py) - Workflow engine
6. [api/routes.py](api/routes.py) - API endpoints

**Configuration:**
7. [config.py](config.py) - Application settings
8. [SETUP_GUIDE.md](SETUP_GUIDE.md) - Deployment guide

## 6. Common Tasks

### Create a Complete Workflow

```python
from app import create_app
from services import RequestService, UserService
from models import UserRole

app = create_app()
db = app.SessionLocal()

# 1. Create users
user_service = UserService(db)
requester = user_service.create_user(
    username='alice',
    email='alice@library.com',
    full_name='Alice Johnson',
    role=UserRole.REQUESTER
)
approver = user_service.create_user(
    username='bob',
    email='bob@library.com',
    full_name='Bob Smith',
    role=UserRole.APPROVER
)

# 2. Create and manage request
req_service = RequestService(db)
request = req_service.create_request(
    requester_id=requester.id,
    title='Research Database',
    budget=15000,
    priority=1
)

# 3. Add items
req_service.add_item_to_request(
    request_id=request.id,
    title='JSTOR',
    item_type='database',
    quantity=1,
    unit_cost=5000
)

# 4. Submit and approve
req_service.submit_request(request.id, requester.id)
req_service.approve_request(request.id, approver.id)
req_service.complete_request(request.id)

db.close()
```

### Query Requests by Status

```python
from models import WorkflowStatus

# Get pending approvals
pending = req_service.get_requests_by_status(WorkflowStatus.PENDING_APPROVAL)
print(f"Items waiting for approval: {len(pending)}")

# Get completed requests
completed = req_service.get_requests_by_status(WorkflowStatus.COMPLETED)
print(f"Completed requests: {len(completed)}")
```

### Get Analytics

```python
from services import AnalyticsService

analytics = AnalyticsService(db)
summary = analytics.get_requests_summary()

print(f"Total requests: {summary['total_requests']}")
print(f"Approval rate: {summary['approval_rate']:.1f}%")
print(f"Average value: ${summary['average_request_value']:.2f}")
```

## 7. Using Postman

1. Create a new Postman collection
2. Add these requests:
   - POST `http://localhost:5000/api/v1/users`
   - POST `http://localhost:5000/api/v1/requests`
   - GET `http://localhost:5000/api/v1/requests/1`
   - POST `http://localhost:5000/api/v1/requests/1/submit`
   - GET `http://localhost:5000/api/v1/analytics/summary`

3. Use the sample payloads in [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 8. Stop the Application

Press `Ctrl+C` in the terminal running the app.

## 9. Next Steps

### To Deploy
See [SETUP_GUIDE.md](SETUP_GUIDE.md#production-deployment)

### To Modify
1. Edit files in the respective directories
2. Run tests: `python -m pytest tests/`
3. Restart the app: `python app.py`

### To Extend
- Add new request fields: Edit [models/__init__.py](models/__init__.py)
- Add new business logic: Create new services in [services/](services/)
- Add new endpoints: Edit [api/routes.py](api/routes.py)
- Add new approval rules: Edit [workflows/__init__.py](workflows/__init__.py)

## 10. Troubleshooting

**Port 5000 already in use?**
```bash
python -c "from app import create_app; app = create_app(); app.run(port=5001)"
```

**Import errors?**
```bash
pip install -r requirements.txt --upgrade
```

**Database errors?**
```bash
# Remove old database
rm library_requests.db
# Run app again to create fresh database
python app.py
```

**Tests failing?**
```bash
python -m pytest tests/ -v --tb=short
```

## 11. Project Structure Quick Reference

```
smart_library_request_workflow/
├── models/              ← Database models (User, Request, etc.)
├── services/            ← Business logic (RequestService, UserService, etc.)
├── workflows/           ← Workflow engine and state machine
├── api/                 ← REST API endpoints
├── tests/               ← Unit and integration tests
├── config.py            ← Configuration settings
├── app.py               ← Flask application
└── example_usage.py     ← Example code
```

## 12. Key Concepts

### Request Workflow
```
1. Create (DRAFT)
   ↓
2. Add Items
   ↓
3. Submit (SUBMITTED or PENDING_APPROVAL)
   ↓
4. Approve (APPROVED)
   ↓
5. Complete (COMPLETED)
```

### Approval Trigger
Auto-approval required if:
- 5+ items
- High priority (1-2)
- Budget > $10,000

### User Roles
- **REQUESTER**: Can create and manage own requests
- **APPROVER**: Can approve/reject requests
- **LIBRARIAN**: Can manage items and fulfillment
- **ADMIN**: Can manage everything

## 13. Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Project overview & features |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Installation & deployment |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project structure & details |
| [GETTING_STARTED.md](GETTING_STARTED.md) | This file |

## Done! 🎉

You now have a working Smart Library Request Workflow system. 

**Next: Explore the code, run the example, and try the API!**

For detailed documentation, see the README.md and API_DOCUMENTATION.md files.

---
**Quick Links:**
- Start app: `python app.py`
- Run example: `python example_usage.py`
- Run tests: `python -m pytest tests/`
- View API docs: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Setup guide: [SETUP_GUIDE.md](SETUP_GUIDE.md)
