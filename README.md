# Smart Library Request Workflow

A comprehensive Python-based request management system for library resource requests with intelligent workflow automation, approval routing, and analytics.

## Features

- **Request Management**: Create, submit, track, and manage library resource requests
- **Smart Workflow Engine**: Intelligent state machine with automatic approval routing based on request criteria
- **User Roles & Permissions**: Multi-tier user system (Admin, Librarian, Requester, Approver)
- **Approval Workflow**: Automatic approval routing based on budget, priority, and item count
- **Notifications**: Email notifications for status updates and approvals
- **Analytics & Reporting**: Request statistics, approval rates, and departmental spending
- **REST API**: Full-featured REST API for integration
- **Database Models**: Comprehensive SQLAlchemy models with relationships

## Project Structure

```
smart_library_request_workflow/
├── models/              # Database models and schemas
├── services/            # Business logic and services
├── workflows/           # Workflow engine and state machine
├── api/                 # REST API routes and endpoints
├── database/            # Database initialization
├── utils/               # Utility functions and helpers
├── tests/               # Unit and integration tests
├── config.py            # Application configuration
├── app.py               # Flask application factory
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone/Navigate to the project directory:
```bash
cd smart_library_request_workflow
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables (optional):
```bash
export FLASK_ENV=development
export DATABASE_URL=sqlite:///library_requests.db
export SERVICENOW_URL=https://dev.service-now.com
```

## Running the Application

### Start the Flask server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Health Check:
```bash
curl http://localhost:5000/health
```

## API Endpoints

### Requests
- `POST /api/v1/requests` - Create new request
- `GET /api/v1/requests/<id>` - Get request details
- `POST /api/v1/requests/<id>/items` - Add item to request
- `POST /api/v1/requests/<id>/submit` - Submit request
- `POST /api/v1/requests/<id>/approve` - Approve request
- `POST /api/v1/requests/<id>/reject` - Reject request
- `POST /api/v1/requests/<id>/complete` - Mark as completed
- `GET /api/v1/requests/status/<status>` - Get requests by status

### Users
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/<id>` - Get user details

### Analytics
- `GET /api/v1/analytics/summary` - Get dashboard summary
- `GET /api/v1/analytics/status-breakdown` - Get status breakdown

## Request Workflow States

- **DRAFT**: Initial state, request being prepared
- **SUBMITTED**: Request submitted for review
- **PENDING_APPROVAL**: Waiting for approval (auto-determined by system)
- **APPROVED**: Request approved
- **REJECTED**: Request rejected, can be resubmitted
- **IN_PROGRESS**: Being fulfilled
- **COMPLETED**: Completed
- **CANCELLED**: Request cancelled

## Approval Logic

A request is automatically flagged for approval if:
- Number of items >= 5
- Priority level is 1 or 2 (high priority)
- Total budget > $10,000

## Database Models

### User
- username, email, full_name
- role: admin, librarian, requester, approver
- department, is_active

### Request
- request_number (auto-generated)
- title, description
- status, priority, budget
- requester_id (FK to User)
- timestamps: created_at, submitted_at, completed_at

### RequestItem
- title, author, isbn
- item_type: book, journal, database, etc.
- quantity, unit_cost
- justification
- request_id (FK to Request)

### Approval
- request_id (FK to Request)
- approver_id (FK to User)
- status: pending, approved, rejected
- comments, approval_date

### RequestNote
- request_id (FK to Request)
- author_id (FK to User)
- content, created_at

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_services.py

# Run with coverage
python -m pytest --cov=. tests/
```

## Configuration

Edit `config.py` to customize:
- Database URL
- Request timeout duration
- Approval thresholds
- Notification settings
- ServiceNow integration parameters

## Environment Variables

```
FLASK_ENV=development|production|testing
DATABASE_URL=connection_string
ADMIN_EMAIL=admin@library.com
SERVICENOW_URL=https://...
SERVICENOW_USER=user
SERVICENOW_PASS=password
```

## ServiceNow Integration

The system is designed to integrate with ServiceNow:
- Configuration settings for ServiceNow API connection
- Future: Two-way sync of requests and records
- Future: Approval notifications to ServiceNow

## Example Usage

```python
from app import create_app
from sqlalchemy.orm import Session
from services import RequestService, UserService
from models import UserRole

# Initialize app and database
app = create_app()
db = app.SessionLocal()

# Create users
user_service = UserService(db)
requester = user_service.create_user(
    username='john_doe',
    email='john@library.com',
    full_name='John Doe',
    role=UserRole.REQUESTER,
    department='Research'
)

approver = user_service.create_user(
    username='jane_smith',
    email='jane@library.com',
    full_name='Jane Smith',
    role=UserRole.APPROVER
)

# Create a request
req_service = RequestService(db)
request = req_service.create_request(
    requester_id=requester.id,
    title='Research Materials Bundle',
    description='Need research materials for spring semester',
    priority=2,
    budget=5000,
    department='Research'
)

# Add items
req_service.add_item_to_request(
    request_id=request.id,
    title='Database Access',
    item_type='database',
    quantity=1,
    unit_cost=2500
)

# Submit request
req_service.submit_request(request.id, requester.id)

# Approve request
req_service.approve_request(request.id, approver.id, comments='Approved')

# Mark as completed
req_service.complete_request(request.id)
```

## Error Handling

The system includes comprehensive error handling:
- Input validation
- Workflow state validation
- Business rule enforcement
- Descriptive error messages

## Performance Considerations

- Database indexes on frequently queried fields (status, requester_id, created_at)
- Batch operations for bulk imports
- Async notification queue for scalability

## Security

- Role-based access control (RBAC)
- Input validation and sanitization
- User authentication/authorization (can be extended)
- Audit trail via workflow history

## Future Enhancements

- [ ] User authentication with JWT
- [ ] Email notifications integration
- [ ] File attachments support
- [ ] Advanced filtering and search
- [ ] Workflow customization UI
- [ ] Budget forecasting
- [ ] Vendor integration
- [ ] Mobile app support
- [ ] Real-time WebSocket updates
- [ ] Audit logging and compliance reporting

## Contributing

1. Create a feature branch
2. Make changes and test thoroughly
3. Submit pull request with description

## License

Proprietary - Library Services

## Support

For issues or questions, contact the Library Services team.

## Changelog

### Version 1.0.0 (Initial Release)
- Core request management functionality
- Workflow engine with state machine
- Basic approval routing
- REST API
- Analytics and reporting
- Unit and integration tests
