#!/bin/bash

# Django Celery Project Setup Script

echo "🚀 Setting up Django Celery Project..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed. Please install PostgreSQL first."
    echo "   Run: sudo apt install postgresql postgresql-contrib"
fi

# Check if Redis is installed
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis is not installed. Please install Redis first."
    echo "   Run: sudo apt install redis-server"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created. Please edit it with your configuration."
    else
        echo "⚠️  .env.example not found. Creating default .env file..."
        cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=celery_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
EOF
        echo "✅ Default .env file created"
    fi
else
    echo "✅ .env file already exists"
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if sudo systemctl is-active --quiet postgresql; then
    echo "✅ PostgreSQL is running"
else
    echo "⚠️  PostgreSQL is not running. Please start it with: sudo systemctl start postgresql"
fi

# Check if Redis is running
echo "🔍 Checking Redis..."
if sudo systemctl is-active --quiet redis-server; then
    echo "✅ Redis is running"
else
    echo "⚠️  Redis is not running. Please start it with: sudo systemctl start redis-server"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database and Redis credentials"
echo "2. Create PostgreSQL database (see README.md for instructions)"
echo "3. Run migrations: python manage.py migrate"
echo "4. Start Django server: python manage.py runserver"
echo "5. Start Celery worker (in another terminal): celery -A celery_project worker --loglevel=info"
echo ""
echo "For detailed instructions, see README.md"

