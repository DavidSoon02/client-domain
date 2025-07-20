# Delete User Service

Microservice for deleting users from the system.

## Local Installation

### Prerequisites
- Python 3.11+
- PostgreSQL with UUID extension
- Git

### Setup Steps

1. **Clone and navigate to the service directory:**
```bash
cd delete-service
```

2. **Create virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

4. **Database setup:**
- Run the init.sql script to create the users table
- Update `.env` file with your database credentials

5. **Configure environment variables:**
Edit `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
JWT_SECRET=distributed-programming-edison
JWT_EXPIRES_IN=24h
BCRYPT_ROUNDS=12
PORT=8003
HOST=0.0.0.0
```

6. **Run the service:**
```powershell
python main.py
```

The service will be available at `http://localhost:8003`

## API Testing

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Delete User

**DELETE** `/users/{user_id}`

**Response:**
```json
{
    "message": "User deleted successfully",
    "deleted_user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Test with cURL

**Delete a user:**
```bash
curl -X DELETE "http://localhost:8003/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8003/health
```

## Database Schema

The service uses a `users` table with UUID primary keys:
- `id`: UUID (Primary Key, auto-generated)
- `email`: VARCHAR(255) (Unique, Required)
- `password`: VARCHAR(255) (Optional)
- `first_name`: VARCHAR(100) (Required)
- `last_name`: VARCHAR(100) (Required)
- `is_active`: BOOLEAN (Default: true)
- `created_at`: TIMESTAMPTZ (Auto-generated)
- `updated_at`: TIMESTAMPTZ (Auto-generated)
- `github_id`: VARCHAR(255) (Optional)
- `role`: VARCHAR(50) (Default: 'client')

## Docker Usage

1. **Build image:**
```bash
docker build -t delete-user-service .
```

2. **Run container:**
```bash
docker run -p 8003:8003 --env-file .env delete-user-service
```

## Error Handling

- **401**: Invalid or missing JWT token
- **404**: User not found

## Testing Workflow

To test the complete microservice ecosystem:

1. **Start all services** on different ports (8001, 8002, 8003)
2. **Create a user** using Add Service (POST /users)
3. **List users** using List Service (GET /users)
4. **Get specific user** using List Service (GET /users/{id})
5. **Delete user** using Delete Service (DELETE /users/{id})
6. **Verify deletion** using List Service

### Complete Test Example

```bash
# 1. Add a user
curl -X POST "http://localhost:8001/users" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }'

# 2. List all users
curl -X GET "http://localhost:8002/users" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 3. Get specific user (using UUID from response)
curl -X GET "http://localhost:8002/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 4. Delete the user
curl -X DELETE "http://localhost:8003/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 5. Verify deletion
curl -X GET "http://localhost:8002/users/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
