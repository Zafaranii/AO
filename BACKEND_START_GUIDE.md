# Backend Start Guide for Frontend Developers

This guide will help you quickly set up and run the AO Real Estate API backend for frontend development.

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **MySQL 8.0+** - [Download MySQL](https://dev.mysql.com/downloads/mysql/)
- **Git** - [Download Git](https://git-scm.com/downloads)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AO
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

The backend will automatically create the database and tables when you start the server! You just need to have MySQL running.

#### Option A: Using Docker (Recommended for quick setup)

```bash
# Start MySQL with Docker
docker run --name ao-mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mysql:8.0
```

#### Option B: Local MySQL Installation

1. Install MySQL on your system
2. Start MySQL service
3. The backend will automatically create the `real_estate_db` database and all tables on startup

### 5. Environment Configuration (Optional)

**Good news!** The backend will work with default settings even without a `.env` file. However, for production or custom setups, create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/real_estate_db

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Super Admin Configuration (for initial setup)
SUPER_ADMIN_NAME=Super Admin
SUPER_ADMIN_EMAIL=admin@example.com
SUPER_ADMIN_PHONE=+1234567890
SUPER_ADMIN_PASSWORD=admin123

# Storage Configuration
STORAGE_BACKEND=local
UPLOADS_DIR=uploads

# Database Debug (optional)
DB_ECHO=false
```

**Default Configuration (if no .env file):**
- Database: `mysql+pymysql://root:password@localhost:3306/real_estate_db`
- The server will show a warning message about using default settings

### 6. Initialize Super Admin (Optional)

The database and tables are created automatically, but you may want to create a super admin user:

```bash
python setup.py
```

This will:
- Create a super admin user
- Optionally create sample data

### 7. Start the Backend Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

**Note**: The backend will automatically:
- Create the `real_estate_db` database if it doesn't exist
- Create all necessary tables on startup
- Log the database creation process

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints Overview

### Authentication
- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/auth/refresh` - Refresh access token

### Apartments
- `GET /api/v1/apartments/rent` - Get rental apartments
- `POST /api/v1/apartments/rent` - Create rental apartment (Admin only)
- `GET /api/v1/apartments/sale` - Get sale apartments
- `POST /api/v1/apartments/sale` - Create sale apartment (Admin only)

### Admin Management
- `GET /api/v1/admins` - Get all admins (Super Admin only)
- `POST /api/v1/admins` - Create new admin (Super Admin only)

### File Uploads
- `POST /api/v1/uploads/part` - Upload apartment part images

## Frontend Integration

### CORS Configuration

The backend is configured to allow all origins for development. In production, update the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication Flow

1. **Login**: Send POST request to `/api/v1/auth/login` with email and password
2. **Store Token**: Save the returned access token in your frontend storage
3. **Include Token**: Add `Authorization: Bearer <token>` header to protected requests
4. **Refresh Token**: Use `/api/v1/auth/refresh` when the token expires

### Example Frontend Integration

```javascript
// Login
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  return data;
};

// Authenticated request
const fetchApartments = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/v1/apartments/rent', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  return response.json();
};
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in `.env`
   - The backend will automatically create the database, so this error usually means MySQL isn't running

2. **Port Already in Use**
   - Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

3. **Module Import Errors**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Permission Denied (File Uploads)**
   - Check `uploads/` directory permissions
   - Ensure directory exists and is writable

### Getting Help

- Check the API documentation at http://localhost:8000/docs
- Review the logs in the terminal where you started the server
- Check the `TESTING.md` file for API test examples

## Development Tips

1. **Hot Reload**: The server automatically reloads when you make changes to the code
2. **Database Changes**: Restart the server after making model changes
3. **Testing**: Use the provided test scripts in `test_api.py` and `test_curl.sh`
4. **File Uploads**: Test file uploads using the `/uploads/part` endpoint

## Production Deployment

For production deployment, see the `deploy.sh` script and `render.yaml` configuration file.

---

**Need Help?** Check the API documentation at http://localhost:8000/docs or contact the backend team.
