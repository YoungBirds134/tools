#!/bin/bash

# Trading Notification Service Startup Script
# Production-ready startup with health checks and monitoring

set -e

echo "🚀 Starting Trading Notification Service..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found, copying from .env.example"
    cp .env.example .env
    print_error "Please configure your .env file with proper values before running again"
    exit 1
fi

# Load environment variables
source .env

# Check required environment variables
print_header "Checking environment configuration..."

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your-telegram-bot-token" ]; then
    print_error "TELEGRAM_BOT_TOKEN is not configured in .env file"
    echo "Please get a bot token from @BotFather and update your .env file"
    exit 1
fi

if [ -z "$AUTHORIZED_USERS" ] || [ "$AUTHORIZED_USERS" = '["123456789", "987654321"]' ]; then
    print_warning "AUTHORIZED_USERS not configured or using default values"
    echo "Consider updating AUTHORIZED_USERS in .env with your Telegram chat IDs"
fi

print_status "Environment configuration looks good!"

# Function to check if a service is running
check_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1

    print_header "Checking $service_name on port $port..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s "http://localhost:$port" > /dev/null 2>&1; then
            print_status "$service_name is running on port $port"
            return 0
        fi
        
        echo -n "."
        sleep 1
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start on port $port"
    return 1
}

# Function to check Redis
check_redis() {
    print_header "Checking Redis connection..."
    
    if command -v redis-cli > /dev/null 2>&1; then
        if redis-cli ping > /dev/null 2>&1; then
            print_status "Redis is running and accessible"
            return 0
        fi
    fi
    
    print_warning "Redis is not accessible, starting with Docker..."
    return 1
}

# Determine startup method
STARTUP_METHOD="docker"

if [ "$1" = "local" ]; then
    STARTUP_METHOD="local"
elif [ "$1" = "docker" ]; then
    STARTUP_METHOD="docker"
elif [ "$1" = "dev" ]; then
    STARTUP_METHOD="dev"
fi

case $STARTUP_METHOD in
    "local")
        print_header "Starting in LOCAL mode..."
        
        # Check Redis
        if ! check_redis; then
            print_error "Redis is required for local mode. Please start Redis first:"
            echo "  redis-server"
            echo "Or use Docker mode: ./start.sh docker"
            exit 1
        fi
        
        # Start the notification service
        print_header "Starting notification service..."
        python -m app.main
        ;;
        
    "dev")
        print_header "Starting in DEVELOPMENT mode..."
        
        # Check if we have docker-compose
        if ! command -v docker-compose > /dev/null 2>&1; then
            print_error "docker-compose is required but not installed"
            exit 1
        fi
        
        # Start development stack
        print_status "Starting development stack with docker-compose..."
        docker-compose up --build
        ;;
        
    "docker")
        print_header "Starting in DOCKER mode..."
        
        # Check if we have docker-compose
        if ! command -v docker-compose > /dev/null 2>&1; then
            print_error "docker-compose is required but not installed"
            exit 1
        fi
        
        # Start production stack
        print_status "Starting production stack with docker-compose..."
        docker-compose up -d --build
        
        # Wait for services to start
        sleep 5
        
        # Check service health
        if check_service "Notification Service" 8001; then
            print_status "🎉 Notification Service started successfully!"
            echo ""
            echo "📊 Service Information:"
            echo "  • API: http://localhost:8001"
            echo "  • Health Check: http://localhost:8001/api/v1/health/"
            echo "  • Documentation: http://localhost:8001/docs"
            echo "  • Redis: localhost:6379"
            echo ""
            echo "🤖 Telegram Bot:"
            echo "  • Bot is running and ready to receive messages"
            echo "  • Send /start to your bot to begin"
            echo ""
            echo "🔧 Management Commands:"
            echo "  • View logs: docker-compose logs -f notification-service"
            echo "  • Stop services: docker-compose down"
            echo "  • Restart: docker-compose restart notification-service"
            echo ""
            
            # Test notification endpoint
            print_header "Testing notification service..."
            curl -s "http://localhost:8001/api/v1/health/" | python -m json.tool || print_warning "Could not parse health check response"
            
        else
            print_error "Service failed to start properly"
            echo "Check logs with: docker-compose logs notification-service"
            exit 1
        fi
        ;;
        
    *)
        echo "Usage: $0 [local|docker|dev]"
        echo ""
        echo "  local  - Run locally (requires Redis to be running)"
        echo "  docker - Run with Docker Compose (recommended)"
        echo "  dev    - Run in development mode with live reload"
        echo ""
        echo "Default: docker"
        echo ""
        echo "Examples:"
        echo "  $0           # Start with Docker (production mode)"
        echo "  $0 docker    # Start with Docker (production mode)"
        echo "  $0 dev       # Start in development mode"
        echo "  $0 local     # Start locally (development)"
        exit 1
        ;;
esac
