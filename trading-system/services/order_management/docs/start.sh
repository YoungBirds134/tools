#!/bin/bash

# Quick Start Script for FC Trading API
# This script helps you start the application in different modes

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Function to check if .env exists
check_env() {
    if [ ! -f ".env" ]; then
        warn ".env file not found. Creating from template..."
        if [ -f ".env.production" ]; then
            cp .env.production .env
            warn "Please update .env with your actual credentials!"
            info "Required variables: TELEGRAM_BOT_TOKEN, FC_USERNAME, FC_PASSWORD"
        else
            error ".env.production template not found!"
        fi
    fi
}

# Function to check dependencies
check_dependencies() {
    log "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is required but not installed"
    fi
    
    if [ ! -f "requirements.txt" ]; then
        error "requirements.txt not found"
    fi
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        warn "Virtual environment not found. Creating..."
        python3 -m venv venv
    fi
    
    log "Dependencies check passed"
}

# Function to install requirements
install_requirements() {
    log "Installing/updating requirements..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    log "Requirements installed successfully"
}

# Function to start development mode
start_development() {
    log "Starting FC Trading API in DEVELOPMENT mode..."
    check_env
    check_dependencies
    install_requirements
    
    source venv/bin/activate
    
    # Set development environment
    export ENVIRONMENT=development
    export DEBUG=true
    export TELEGRAM_WEBHOOK_MODE=false
    
    log "Starting FastAPI server..."
    info "Access points:"
    info "  - API Docs: http://localhost:8000/docs"
    info "  - Health: http://localhost:8000/health"
    info "  - API: http://localhost:8000"
    echo ""
    
    # Start with reload for development
    python run.py
}

# Function to start production mode
start_production() {
    log "Starting FC Trading API in PRODUCTION mode with Docker..."
    
    if ! command -v docker &> /dev/null; then
        error "Docker is required for production mode"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is required for production mode"
    fi
    
    check_env
    
    log "Deploying with Docker Compose..."
    ./deploy.sh
}

# Function to start bot only
start_bot() {
    log "Starting Telegram Bot only (polling mode)..."
    check_env
    check_dependencies
    install_requirements
    
    source venv/bin/activate
    
    # Set bot environment
    export ENVIRONMENT=development
    export TELEGRAM_WEBHOOK_MODE=false
    
    log "Starting Telegram bot in polling mode..."
    info "Bot will start polling for messages..."
    
    python -m app.telegram.bot
}

# Function to run tests
run_tests() {
    log "Running tests..."
    check_dependencies
    
    source venv/bin/activate
    
    # Install test dependencies if not present
    pip install pytest pytest-asyncio httpx
    
    # Run tests
    python -m pytest tests/ -v
}

# Function to show help
show_help() {
    echo "FC Trading API - Quick Start Script"
    echo ""
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes:"
    echo "  dev, development    - Start in development mode (recommended for testing)"
    echo "  prod, production    - Start in production mode with Docker"
    echo "  bot                 - Start only Telegram bot (polling mode)"
    echo "  test                - Run tests"
    echo "  help                - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 dev              # Start development server"
    echo "  $0 prod             # Deploy with Docker"
    echo "  $0 bot              # Start bot only"
    echo "  $0 test             # Run tests"
    echo ""
    echo "Environment setup:"
    echo "  1. Copy .env.production to .env"
    echo "  2. Update .env with your credentials"
    echo "  3. Run: $0 dev"
}

# Main script logic
case "${1:-dev}" in
    "dev"|"development")
        start_development
        ;;
    "prod"|"production")
        start_production
        ;;
    "bot"|"telegram")
        start_bot
        ;;
    "test"|"tests")
        run_tests
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        warn "Unknown mode: $1"
        show_help
        exit 1
        ;;
esac
