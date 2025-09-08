# API Documentation - ISP Technician Routing System

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication

All API endpoints (except login/register) require JWT authentication.

### Headers
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## Authentication Endpoints

### POST /auth/login
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_in": 86400,
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "user@example.com",
    "role": "technician"
  }
}
```

### POST /auth/register
Register a new user.

**Request:**
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "password": "password123",
  "role": "customer"
}
```

### POST /auth/refresh
Refresh access token using refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

## Technician Endpoints

### GET /technicians
Get all technicians (Admin only, customers see basic info only).

**Query Parameters:**
- `status`: Filter by status (available, busy, off-duty)
- `skill`: Filter by skill

### GET /technicians/{id}
Get technician by ID.

### GET /technicians/profile
Get current technician's profile (Technician only).

### PUT /technicians/profile
Update current technician's profile (Technician only).

### PUT /technicians/location
Update current technician's location (Technician only).

**Request:**
```json
{
  "location": {
    "lat": 37.7749,
    "lng": -122.4194
  }
}
```

### PUT /technicians/status
Update current technician's status (Technician only).

**Request:**
```json
{
  "status": "available"
}
```

## Job Endpoints

### GET /jobs
Get jobs with filtering based on user role.

**Query Parameters:**
- `status`: Filter by status
- `technician_id`: Filter by technician (Admin/Technician only)
- `customer_id`: Filter by customer (Admin only)
- `date`: Filter by date (YYYY-MM-DD)

### GET /jobs/{id}
Get job by ID.

### PUT /jobs/{id}
Update job. Permissions vary by role:
- **Customer**: Can only update notes
- **Technician**: Can update status, notes, actual times
- **Admin**: Can update all fields

### POST /jobs
Create new job (Admin only).

**Request:**
```json
{
  "customer_id": "customer_id",
  "service_type": "installation",
  "location": {
    "address": "123 Main St, City, State",
    "lat": 37.7749,
    "lng": -122.4194
  },
  "scheduled_date": "2023-12-01",
  "scheduled_time_window": {
    "start": "09:00",
    "end": "12:00"
  },
  "estimated_duration": 120
}
```

### PUT /jobs/{id}/assign
Assign job to technician (Admin only).

## Customer Endpoints

### GET /customers
Get all customers (Admin only).

### GET /customers/{id}
Get customer by ID.

### GET /customers/profile
Get current customer's profile (Customer only).

### PUT /customers/profile
Update current customer's profile (Customer only).

## Routing Endpoints

### POST /routing/optimize
Optimize routes for technicians.

**Request:**
```json
{
  "date": "2023-12-01",
  "technician_ids": ["tech1", "tech2"],
  "consider_traffic": true,
  "consider_weather": true
}
```

## Response Codes

- `200 OK`: Success
- `201 Created`: Resource created
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

## Error Response Format

```json
{
  "error": "Error Type",
  "message": "Detailed error message"
}
```

## Rate Limiting

API requests are limited to 60 requests per minute per IP address.

## Pagination

For endpoints returning lists, use query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response includes pagination info:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```
