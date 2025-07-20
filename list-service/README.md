# List Clients Service

Microservice for listing and retrieving client information with search and pagination capabilities.

## Local Installation

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### Setup Steps

1. **Clone and navigate to the service directory:**
```bash
cd list-service
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
- Create PostgreSQL database: `list_service_db`
- Update `.env` file with your database credentials

5. **Configure environment variables:**
Edit `.env` file:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/list_service_db
JWT_SECRET=distributed-programming-edison
JWT_EXPIRES_IN=24h
BCRYPT_ROUNDS=12
PORT=8002
HOST=0.0.0.0
```

6. **Run the service:**
```powershell
python main.py
```

The service will be available at `http://localhost:8002`

## API Testing

### Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### List All Clients

**GET** `/clients`

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 10, max: 100)
- `search`: Search term for name or email

**Response:**
```json
{
    "clients": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1234567890",
            "address": "123 Main St, City, Country",
            "created_at": "2025-07-20T10:30:00.000Z"
        }
    ],
    "total": 1
}
```

### Get Specific Client

**GET** `/clients/{client_id}`

**Response:**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1234567890",
    "address": "123 Main St, City, Country",
    "created_at": "2025-07-20T10:30:00.000Z"
}
```

### Test with cURL

**List clients with pagination:**
```bash
curl -X GET "http://localhost:8002/clients?skip=0&limit=5" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Search clients:**
```bash
curl -X GET "http://localhost:8002/clients?search=john" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Get specific client:**
```bash
curl -X GET "http://localhost:8002/clients/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8002/health
```

## Docker Usage

1. **Build image:**
```bash
docker build -t list-clients-service .
```

2. **Run container:**
```bash
docker run -p 8002:8002 --env-file .env list-clients-service
```

## Error Handling

- **401**: Invalid or missing JWT token
- **404**: Client not found
- **422**: Invalid query parameters
curl -X GET "http://localhost:3005/clients?skip=0&limit=5" -H "Authorization: Bearer YOUR_JWT_TOKEN"