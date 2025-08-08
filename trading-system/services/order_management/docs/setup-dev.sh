#!/bin/bash

# Quick development setup script
# This script sets up the development environment quickly

set -e

echo "🚀 Setting up FC Trading API development environment..."

# Create .env from template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from production template..."
    cp .env.production .env
    echo "⚠️  Please update .env with your actual credentials!"
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p ssl
mkdir -p data

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Generate self-signed SSL certificates for development
if [ ! -f "ssl/cert.pem" ]; then
    echo "🔐 Generating SSL certificates for development..."
    openssl req -x509 -newkey rsa:2048 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=VN/ST=HCM/L=HoChiMinh/O=FC Trading Dev/CN=localhost"
fi

# Start Redis if Docker is available
if command -v docker &> /dev/null; then
    echo "🗄️  Starting Redis container..."
    docker run -d --name fc-trading-redis -p 6379:6379 redis:7-alpine || echo "Redis container already running"
else
    echo "⚠️  Docker not found. Please install Redis manually or use Docker."
fi

# Test the setup
echo "🧪 Testing the setup..."
python -c "
import sys
try:
    from app.main import app
    print('✅ FastAPI app imports successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env with your actual credentials"
echo "2. Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "3. Visit: http://localhost:8000/docs"
echo ""
echo "For Telegram bot development:"
echo "1. Set TELEGRAM_BOT_TOKEN in .env"
echo "2. Use polling mode for local development"
echo "3. Test with: python -m app.telegram.bot"
