#!/bin/bash

# Real Estate Platform Setup Script

echo "🏠 Real Estate Platform Setup"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed. Please install MySQL server."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "📝 Please edit .env file with your database credentials and other settings"
else
    echo "⚙️ .env file already exists"
fi

# Initialize Alembic (if not already done)
if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions)" ]; then
    echo "🗄️ Initializing database migrations..."
    alembic revision --autogenerate -m "Initial migration"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Create MySQL database: CREATE DATABASE real_estate_db;"
echo "3. Run migrations: alembic upgrade head"
echo "4. Create super admin: python create_super_admin.py"
echo "5. Start the application: uvicorn main:app --reload"
echo ""
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
