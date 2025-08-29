# Real Estate Platform API

A comprehensive FastAPI backend for a real estate platform with apartment management, rental tracking, and notification system.

## 🏗️ Project Structure

```
AO/
├── main.py                    # FastAPI application entry point
├── database.py                # Database configuration and session management
├── dependencies.py            # Authentication and authorization dependencies
├── background_jobs.py         # Background job scheduler for notifications
├── setup.py                   # Database and initial setup script
├── requirements.txt           # Python dependencies
├── alembic.ini               # Alembic configuration for migrations
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore file
├── alembic/                  # Database migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── crud/                     # CRUD operations
│   ├── __init__.py
│   └── user.py              # All CRUD operations
├── models/                   # SQLAlchemy models
│   ├── __init__.py
│   └── user.py              # Database models
├── routers/                  # API route handlers
│   ├── __init__.py
│   ├── auth.py              # Authentication endpoints
│   ├── apartments.py        # Apartment management endpoints
│   ├── notifications.py     # Notification endpoints
│   ├── purchase_requests.py # Purchase/rental inquiries
│   └── admins.py            # Admin management endpoints
└── schemas/                  # Pydantic schemas
    ├── __init__.py
    └── user.py              # Request/response models
```

## 🚀 Features

### 🏠 Apartment Management
- **Apartment Types**: Support for both rental and purchase properties
- **Apartment Parts**: Rental properties can have multiple parts (studios)
- **Flexible Pricing**: Separate pricing for rent and purchase
- **Location & Descriptions**: Detailed property information

### 👥 User Management
- **Role-Based Access**: Super admins and regular admins
- **JWT Authentication**: Secure token-based authentication
- **Permission Control**: Different access levels for different operations

### 📊 Rental Management
- **Contract Tracking**: Start and end dates for rental contracts
- **Tenant Information**: Name, phone, and document storage
- **Status Management**: Available, rented, upcoming end statuses
- **Financial Tracking**: Rent value, deposit, and commission tracking

### 🔔 Notification System
- **Automated Alerts**: Daily background jobs check for:
  - Contract expirations (configurable days ahead)
  - Unpaid rent notifications
- **Admin Notifications**: Targeted notifications to appropriate admins
- **Status Management**: Mark notifications as read/resolved

### 📝 Purchase Requests
- **Guest Inquiries**: Allow potential buyers/renters to submit inquiries
- **Contact Information**: Capture tenant details and requirements
- **Admin Management**: Admins can view and manage all requests

### 📱 WhatsApp Integration
- **Direct Contact**: Generate WhatsApp links for direct communication
- **Auto-messaging**: Pre-filled messages with property details

## 🛠️ Technical Features

- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy ORM**: Robust database operations with MySQL support
- **Alembic Migrations**: Version control for database schema
- **Background Jobs**: APScheduler for automated tasks
- **Pydantic Validation**: Request/response validation and serialization
- **JWT Security**: Token-based authentication with role permissions
- **CORS Support**: Cross-origin resource sharing configuration

## 📋 Database Models

### Admin
- User management with role-based permissions
- Super admin and regular admin roles

### Apartment
- Property information with type (rent/purchase)
- Pricing and location details

### ApartmentPart
- Individual rental units within properties
- Contract and tenant management
- Status tracking and financial details

### Notification
- Automated system notifications
- Contract expiration and payment alerts

### PurchaseRequest
- Guest inquiries and contact requests
- Lead management for sales/rentals

## 🔧 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your MySQL database credentials and other settings
```

### 3. Setup Database
```bash
# Create your MySQL database first
# Then run the setup script
python setup.py
```

### 4. Run the Application
```bash
python main.py
```

### 5. Access the API
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### Login
```bash
POST /api/v1/auth/login
{
    "email": "admin@example.com",
    "password": "your_password"
}
```

### Using JWT Token
Include the token in the Authorization header:
```
Authorization: Bearer your_jwt_token_here
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Admin login
- `POST /api/v1/auth/register` - Register new admin (super admin only)

### Apartments
- `GET /api/v1/apartments` - List apartments (public)
- `GET /api/v1/apartments/{id}` - Get apartment details (public)
- `POST /api/v1/apartments` - Create apartment (admin)
- `PUT /api/v1/apartments/{id}` - Update apartment (admin)
- `DELETE /api/v1/apartments/{id}` - Delete apartment (super admin)
- `GET /api/v1/apartments/{id}/whatsapp` - Get WhatsApp contact (public)

### Apartment Parts
- `GET /api/v1/apartments/{id}/parts` - List apartment parts (public)
- `POST /api/v1/apartments/{id}/parts` - Create apartment part (admin)
- `PUT /api/v1/apartments/{id}/parts/{part_id}` - Update part (admin)
- `DELETE /api/v1/apartments/{id}/parts/{part_id}` - Delete part (super admin)

### Notifications
- `GET /api/v1/notifications` - Get admin's notifications
- `GET /api/v1/notifications/all` - Get all notifications (super admin)
- `PUT /api/v1/notifications/{id}` - Update notification status
- `GET /api/v1/notifications/unread/count` - Get unread count

### Purchase Requests
- `POST /api/v1/purchase-requests` - Create inquiry (public)
- `GET /api/v1/purchase-requests` - List requests (admin)

### Admin Management
- `GET /api/v1/admins` - List all admins (super admin)
- `GET /api/v1/admins/me` - Get current admin info
- `POST /api/v1/admins` - Create admin (super admin)
- `PUT /api/v1/admins/{id}` - Update admin (super admin)
- `DELETE /api/v1/admins/{id}` - Delete admin (super admin)

## 🔄 Background Jobs

The system runs daily background jobs to:

1. **Contract Expiration Check** (9:00 AM daily)
   - Identifies contracts expiring within configured days
   - Creates notifications for admins
   - Configurable via `NOTIFICATION_DAYS_AHEAD` environment variable

2. **Unpaid Rent Check** (10:00 AM daily)
   - Placeholder for payment tracking system
   - Can be extended to integrate with payment processors

## 🔧 Configuration

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/real_estate_db

# Security
SECRET_KEY=your-very-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Background Jobs
NOTIFICATION_DAYS_AHEAD=30
UNPAID_RENT_CHECK_DAYS=5
```

## 🚀 Production Deployment

1. **Environment Setup**:
   - Use a production MySQL database
   - Set strong SECRET_KEY
   - Configure CORS origins properly

2. **Database Migrations**:
   ```bash
   alembic upgrade head
   ```

3. **WSGI Server**:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

4. **Reverse Proxy**: Use Nginx for SSL termination and load balancing

## 🧪 Development

### Running Tests
```bash
# Add your test commands here
pytest
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Manual Background Job Testing
```bash
python background_jobs.py
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support and questions, please contact the development team or create an issue in the repository.

## Getting Started

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

   Or with uvicorn directly:

   ```bash
   uvicorn main:app --reload
   ```

4. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Development

The project follows a modular structure:

- **models/**: SQLAlchemy database models
- **schemas/**: Pydantic models for request/response validation
- **crud/**: Database operations (Create, Read, Update, Delete)
- **routers/**: FastAPI route handlers

To add a new entity:

1. Create a model in `models/`
2. Create schemas in `schemas/`
3. Create CRUD operations in `crud/`
4. Create API routes in `routers/`
5. Include the router in `main.py`

## Example Usage

The template includes example files for a User entity. Uncomment the code in the example files to see a working implementation.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

Add your custom endpoints by creating routers and including them in `main.py`.
