# Add User Service

Microservice for adding new users to the system.

## Local Installation

### Prerequisites
- Python 3.11+
- PostgreSQL with UUID extension
- Git

### Setup Steps

1. **Clone and navigate to the service directory:**
```bash
cd add-service
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
PORT=8001
HOST=0.0.0.0
```

6. **Run the service:**
```powershell
python main.py
```

The service will be available at `http://localhost:8001`

## API Testing

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Create User

**POST** `/users`

**Request Body:**
```json
{
    "email": "john.doe@email.com",
    "password": "optional_password",
    "first_name": "John",
    "last_name": "Doe",
    "github_id": "johndoe123",
    "role": "client"
}
```

**Response:**
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@email.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2025-07-20T10:30:00.000Z",
    "updated_at": "2025-07-20T10:30:00.000Z",
    "github_id": "johndoe123",
    "role": "client"
}
```

### Test with cURL

```bash
curl -X POST "http://localhost:8001/users" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.smith@email.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "client"
  }'
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8001/health
```

## Database Schema

The service uses a `users` table with the following structure:
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
docker build -t add-user-service .
```

2. **Run container:**
```bash
docker run -p 8001:8001 --env-file .env add-user-service
```

## Error Handling

- **400**: Email already registered
- **401**: Invalid or missing JWT token
- **422**: Invalid request data
