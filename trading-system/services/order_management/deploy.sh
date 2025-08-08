#!/bin/bash

# Order Management Service - Deployment Script
# Production-ready deployment with health checks and monitoring

set -e

# Configuration
SERVICE_NAME="order-management"
SERVICE_PORT=8001
SERVICE_DIR="/Users/huynt/Downloads/16072025/trading-system/trading-system/services/order_management"
LOG_LEVEL="info"
WORKERS=1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] ${SERVICE_NAME}:${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ${SERVICE_NAME}:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ${SERVICE_NAME}:${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ${SERVICE_NAME}:${NC} $1"
}

# Function to check if port is available
check_port() {
    if lsof -Pi :$SERVICE_PORT -sTCP:LISTEN -t >/dev/null; then
        log_error "Port $SERVICE_PORT is already in use"
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    log "Installing Python dependencies..."
    
    cd "$SERVICE_DIR"
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    pip install -r requirements.txt
    
    log_success "Dependencies installed successfully"
}

# Function to setup database
setup_database() {
    log "Setting up database..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run database initialization
    python -c "
from app.database import init_database, check_database_connection
try:
    init_database()
    if check_database_connection():
        print('Database setup completed successfully')
    else:
        print('Database connection failed')
        exit(1)
except Exception as e:
    print(f'Database setup failed: {e}')
    exit(1)
"
    
    log_success "Database setup completed"
}

# Function to run health check
health_check() {
    local max_attempts=30
    local attempt=1
    
    log "Performing health check..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:$SERVICE_PORT/health >/dev/null 2>&1; then
            log_success "Health check passed"
            return 0
        fi
        
        log "Health check attempt $attempt/$max_attempts failed, retrying in 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log_error "Health check failed after $max_attempts attempts"
    return 1
}

# Function to start the service
start_service() {
    log "Starting $SERVICE_NAME..."
    
    cd "$SERVICE_DIR"
    
    # Check if port is available
    check_port
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Set environment variables
    export PYTHONPATH="$SERVICE_DIR:$PYTHONPATH"
    export PORT=$SERVICE_PORT
    
    # Start the service
    python -m uvicorn app.main_new:app \
        --host 0.0.0.0 \
        --port $SERVICE_PORT \
        --workers $WORKERS \
        --log-level $LOG_LEVEL \
        --access-log \
        --reload &
    
    # Save PID
    echo $! > "$SERVICE_DIR/service.pid"
    
    log_success "$SERVICE_NAME started on port $SERVICE_PORT (PID: $!)"
    
    # Wait for service to start
    sleep 5
    
    # Perform health check
    if health_check; then
        log_success "$SERVICE_NAME is running and healthy"
        log "Service URLs:"
        log "  - Health Check: http://localhost:$SERVICE_PORT/health"
        log "  - API Documentation: http://localhost:$SERVICE_PORT/docs"
        log "  - Service Info: http://localhost:$SERVICE_PORT/info"
        log "  - Metrics: http://localhost:$SERVICE_PORT/metrics"
    else
        log_error "$SERVICE_NAME failed to start properly"
        stop_service
        exit 1
    fi
}

# Function to stop the service
stop_service() {
    log "Stopping $SERVICE_NAME..."
    
    if [ -f "$SERVICE_DIR/service.pid" ]; then
        local pid=$(cat "$SERVICE_DIR/service.pid")
        if kill -0 $pid 2>/dev/null; then
            kill $pid
            log_success "$SERVICE_NAME stopped (PID: $pid)"
        else
            log_warning "Process $pid not found"
        fi
        rm -f "$SERVICE_DIR/service.pid"
    else
        log_warning "PID file not found"
    fi
}

# Function to restart the service
restart_service() {
    log "Restarting $SERVICE_NAME..."
    stop_service
    sleep 2
    start_service
}

# Function to check service status
check_status() {
    if [ -f "$SERVICE_DIR/service.pid" ]; then
        local pid=$(cat "$SERVICE_DIR/service.pid")
        if kill -0 $pid 2>/dev/null; then
            log_success "$SERVICE_NAME is running (PID: $pid)"
            
            # Check health endpoint
            if curl -s http://localhost:$SERVICE_PORT/health >/dev/null 2>&1; then
                log_success "Service is healthy"
            else
                log_warning "Service is running but health check failed"
            fi
        else
            log_error "$SERVICE_NAME is not running (stale PID file)"
            rm -f "$SERVICE_DIR/service.pid"
        fi
    else
        log_error "$SERVICE_NAME is not running"
    fi
}

# Function to view logs
view_logs() {
    log "Viewing $SERVICE_NAME logs..."
    # In production, this would tail actual log files
    log "Service is running with console output"
}

# Function to run in development mode
dev_mode() {
    log "Starting $SERVICE_NAME in development mode..."
    
    cd "$SERVICE_DIR"
    
    # Check if port is available
    check_port
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Set environment variables for development
    export PYTHONPATH="$SERVICE_DIR:$PYTHONPATH"
    export PORT=$SERVICE_PORT
    export DEBUG=true
    export ENVIRONMENT=development
    
    # Start in development mode with hot reload
    python -m uvicorn app.main_new:app \
        --host 0.0.0.0 \
        --port $SERVICE_PORT \
        --reload \
        --log-level debug \
        --access-log
}

# Function to run tests
run_tests() {
    log "Running tests for $SERVICE_NAME..."
    
    cd "$SERVICE_DIR"
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run tests
    python -m pytest tests/ -v --cov=app --cov-report=html
    
    log_success "Tests completed"
}

# Function to show help
show_help() {
    echo "Usage: $0 {start|stop|restart|status|logs|dev|test|install|setup|help}"
    echo ""
    echo "Commands:"
    echo "  start     - Start the Order Management Service"
    echo "  stop      - Stop the Order Management Service"
    echo "  restart   - Restart the Order Management Service"
    echo "  status    - Check service status"
    echo "  logs      - View service logs"
    echo "  dev       - Start in development mode with hot reload"
    echo "  test      - Run tests"
    echo "  install   - Install dependencies"
    echo "  setup     - Setup database"
    echo "  help      - Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  SERVICE_PORT - Port to run the service (default: 8001)"
    echo "  LOG_LEVEL    - Log level (default: info)"
    echo "  WORKERS      - Number of workers (default: 1)"
}

# Main script logic
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    dev)
        dev_mode
        ;;
    test)
        run_tests
        ;;
    install)
        install_dependencies
        ;;
    setup)
        setup_database
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
