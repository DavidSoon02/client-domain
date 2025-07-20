# User Domain Microservices

Distributed microservices architecture for user management with JWT authentication and UUID-based identification.

## Architecture Overview

This project consists of three independent microservices:

- **Add Service** (Port 8001) - Creates new users
- **List Service** (Port 8002) - Retrieves and searches users  
- **Delete Service** (Port 8003) - Removes users

Each service uses the same PostgreSQL database with a `users` table that includes UUID primary keys, timestamps, and role-based access.

## Database Schema

All services use a shared `users` table with the following structure:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    github_id VARCHAR(255),
    role VARCHAR(50) DEFAULT 'client'
);
```

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL with UUID extension
- Valid JWT token with secret: `distributed-programming-edison`

### Database Setup

First, run the initialization script on your PostgreSQL database:
```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

Then run the `init.sql` file from any service directory to create the table structure.

### Setup All Services

1. **Setup Add Service:**
```powershell
cd add-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. **Setup List Service:**
```powershell
cd list-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. **Setup Delete Service:**
```powershell
cd delete-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Running Services

Open three terminal windows and run each service:

**Terminal 1 - Add Service:**
```powershell
cd add-service
.\venv\Scripts\Activate.ps1
python main.py
```

**Terminal 2 - List Service:**
```powershell
cd list-service
.\venv\Scripts\Activate.ps1
python main.py
```

**Terminal 3 - Delete Service:**
```powershell
cd delete-service
.\venv\Scripts\Activate.ps1
python main.py
```

## API Endpoints

| Service | Method | Endpoint | Description |
|---------|--------|----------|-------------|
| Add | POST | `/users` | Create new user |
| List | GET | `/users` | List all users (with pagination/search) |
| List | GET | `/users/{uuid}` | Get specific user |
| Delete | DELETE | `/users/{uuid}` | Delete user |
| All | GET | `/health` | Health check |

## Authentication

All endpoints (except health checks) require JWT authentication:

```
Authorization: Bearer <your-jwt-token>
```

## User Data Structure

### Request (Create User):
```json
{
    "email": "user@example.com",
    "password": "optional_password",
    "first_name": "John",
    "last_name": "Doe",
    "github_id": "optional_github_id",
    "role": "client"
}
```

### Response (User Object):
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2025-07-20T10:30:00.000Z",
    "updated_at": "2025-07-20T10:30:00.000Z",
    "github_id": "optional_github_id",
    "role": "client"
}
```

## Testing Workflow

1. **Create User** → Add Service (POST /users)
2. **List Users** → List Service (GET /users)
3. **Get User** → List Service (GET /users/{uuid})
4. **Delete User** → Delete Service (DELETE /users/{uuid})

## Docker Deployment

Each service includes a Dockerfile for containerization:

```bash
# Build images
docker build -t add-user-service ./add-service
docker build -t list-users-service ./list-service  
docker build -t delete-user-service ./delete-service

# Run containers
docker run -p 8001:8001 --env-file ./add-service/.env add-user-service
docker run -p 8002:8002 --env-file ./list-service/.env list-users-service
docker run -p 8003:8003 --env-file ./delete-service/.env delete-user-service
```

## Environment Variables

Each service uses the following environment variables:

```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=distributed-programming-edison
JWT_EXPIRES_IN=24h
BCRYPT_ROUNDS=12
PORT=800X
HOST=0.0.0.0
```

## Service Details

For detailed installation and testing instructions, see individual README files:

- [Add Service README](./add-service/README.md)
- [List Service README](./list-service/README.md)
- [Delete Service README](./delete-service/README.md)
