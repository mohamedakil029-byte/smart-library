# API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
Currently, the API operates without authentication. Future versions will include JWT token-based authentication.

## Response Format

All responses are in JSON format with the following structure:

### Success Response
```json
{
  "status": "success",
  "data": {},
  "message": "Operation completed"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Request Endpoints

### Create Request
```
POST /requests
Content-Type: application/json

{
  "requester_id": 1,
  "title": "Request Title",
  "description": "Detailed description",
  "priority": 2,
  "department": "Research",
  "budget": 5000
}

Response: 201 Created
{
  "status": "success",
  "message": "Request created",
  "request_id": 1,
  "request_number": "REQ-20240406-A1B2C3D4"
}
```

### Get Request
```
GET /requests/{request_id}

Response: 200 OK
{
  "status": "success",
  "request": {
    "id": 1,
    "request_number": "REQ-20240406-A1B2C3D4",
    "title": "Request Title",
    "status": "draft",
    "priority": 2,
    "budget": 5000,
    "items_count": 2,
    "created_at": "2024-04-06T10:30:00",
    "submitted_at": null
  }
}
```

### Add Item to Request
```
POST /requests/{request_id}/items
Content-Type: application/json

{
  "title": "Book Title",
  "item_type": "book",
  "author": "Author Name",
  "isbn": "978-0-123456-78-9",
  "quantity": 2,
  "unit_cost": 45,
  "justification": "Required for research project"
}

Response: 201 Created
{
  "status": "success",
  "message": "Item added",
  "item_id": 5
}
```

### Submit Request
```
POST /requests/{request_id}/submit
Content-Type: application/json

{
  "submitted_by_id": 1
}

Response: 200 OK
{
  "status": "success",
  "message": "Request submitted"
}
```

### Approve Request
```
POST /requests/{request_id}/approve
Content-Type: application/json

{
  "approver_id": 2,
  "comments": "Approved - good value"
}

Response: 200 OK
{
  "status": "success",
  "message": "Request approved"
}
```

### Reject Request
```
POST /requests/{request_id}/reject
Content-Type: application/json

{
  "approver_id": 2,
  "comments": "Needs more justification"
}

Response: 200 OK
{
  "status": "success",
  "message": "Request rejected"
}
```

### Complete Request
```
POST /requests/{request_id}/complete

Response: 200 OK
{
  "status": "success",
  "message": "Request completed"
}
```

### Get Requests by Status
```
GET /requests/status/{status}

Valid statuses: draft, submitted, pending_approval, approved, rejected, in_progress, completed, cancelled

Response: 200 OK
{
  "status": "success",
  "requests": [
    {
      "id": 1,
      "request_number": "REQ-20240406-A1B2C3D4",
      "title": "Request Title",
      "status": "submitted"
    }
  ]
}
```

## User Endpoints

### Create User
```
POST /users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@library.com",
  "full_name": "John Doe",
  "role": "REQUESTER",
  "department": "Research"
}

Valid roles: ADMIN, LIBRARIAN, REQUESTER, APPROVER

Response: 201 Created
{
  "status": "success",
  "message": "User created",
  "user_id": 1
}
```

### Get User
```
GET /users/{user_id}

Response: 200 OK
{
  "status": "success",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@library.com",
    "full_name": "John Doe",
    "role": "requester",
    "department": "Research",
    "is_active": true
  }
}
```

## Analytics Endpoints

### Get Analytics Summary
```
GET /analytics/summary

Response: 200 OK
{
  "status": "success",
  "summary": {
    "total_requests": 25,
    "pending_approval": 5,
    "approved": 15,
    "completed": 3,
    "rejected": 2,
    "approval_rate": 88.0,
    "total_items": 67,
    "average_request_value": 2500.0
  }
}
```

### Get Status Breakdown
```
GET /analytics/status-breakdown

Response: 200 OK
{
  "status": "success",
  "breakdown": {
    "draft": 2,
    "submitted": 3,
    "pending_approval": 5,
    "approved": 10,
    "rejected": 1,
    "in_progress": 3,
    "completed": 1,
    "cancelled": 0
  }
}
```

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input or bad request |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

## Rate Limiting

Not currently implemented. Future versions will include rate limiting.

## Pagination

Not currently implemented. Future versions will include pagination for large result sets.

## Filtering & Search

Not currently implemented. Future versions will include advanced filtering capabilities.

## cURL Examples

### Create a Request
```bash
curl -X POST http://localhost:5000/api/v1/requests \
  -H "Content-Type: application/json" \
  -d '{
    "requester_id": 1,
    "title": "Research Materials",
    "description": "Need materials for spring semester",
    "priority": 2,
    "budget": 5000
  }'
```

### Get Request Details
```bash
curl http://localhost:5000/api/v1/requests/1
```

### Submit a Request
```bash
curl -X POST http://localhost:5000/api/v1/requests/1/submit \
  -H "Content-Type: application/json" \
  -d '{"submitted_by_id": 1}'
```

### Approve a Request
```bash
curl -X POST http://localhost:5000/api/v1/requests/1/approve \
  -H "Content-Type: application/json" \
  -d '{
    "approver_id": 2,
    "comments": "Approved"
  }'
```

### Get Analytics
```bash
curl http://localhost:5000/api/v1/analytics/summary
```
