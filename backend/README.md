# eSalama Backend API

Python-based backend API for the eSalama Schools student tracking and attendance system.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **QR Codes**: qrcode library

## Features

- RESTful API with automatic OpenAPI documentation
- JWT-based authentication with role-based access control
- Student management
- Real-time GPS location tracking
- QR code generation and verification for attendance
- Attendance recording (arrival/departure)
- Notification system
- Audit logging

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- Redis (optional, for caching)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/eodenyire/eSalama.git
   cd eSalama/backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure:
   - Database connection URL
   - JWT secret key
   - Redis URL (if using)
   - External service credentials (Twilio, AWS, etc.)

5. **Set up the database**:
   ```bash
   # Create PostgreSQL database
   createdb esalama
   
   # Run migrations (tables will be created automatically on first run)
   ```

### Running the Application

**Development mode**:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode**:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── config/
│   ├── database.py      # Database configuration
│   └── settings.py      # Application settings
├── migrations/          # Database migrations
├── src/
│   ├── auth/           # Authentication & authorization
│   ├── students/       # Student management
│   ├── attendance/     # Attendance tracking
│   ├── location-tracking/  # GPS tracking
│   ├── qr-verification/    # QR code operations
│   ├── notifications/  # Notification system
│   ├── models.py       # Database models
│   ├── schemas.py      # Pydantic schemas
│   └── main.py         # Main application
├── tests/              # Unit and integration tests
├── .env.example        # Example environment variables
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/auth/me` - Get current user info

### Students
- `GET /api/v1/students` - List students
- `POST /api/v1/students` - Create student
- `GET /api/v1/students/{student_id}` - Get student details
- `PUT /api/v1/students/{student_id}` - Update student
- `PUT /api/v1/students/{student_id}/device` - Update device info

### Attendance
- `POST /api/v1/attendance` - Record attendance
- `GET /api/v1/attendance` - Get attendance records

### Location
- `POST /api/v1/location` - Post GPS coordinates
- `GET /api/v1/location/{student_id}/last` - Get last location
- `GET /api/v1/location/{student_id}/history` - Get location history

### QR Codes
- `POST /api/v1/qr/generate` - Generate QR code
- `POST /api/v1/qr/validate` - Validate QR code

### Notifications
- `POST /api/v1/notifications` - Send notification
- `GET /api/v1/notifications` - Get notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## Docker

Build and run with Docker:

```bash
# Build image
docker build -t esalama-backend .

# Run container
docker run -p 8000:8000 --env-file .env esalama-backend
```

## Security

- All API endpoints (except login/register) require JWT authentication
- Role-based access control enforces permissions
- Passwords are hashed using bcrypt
- QR codes are single-use and time-limited
- All sensitive data is encrypted in transit (HTTPS)

## Contributing

Please refer to the main repository's contributing guidelines.

## License

MIT License - see LICENSE file for details
