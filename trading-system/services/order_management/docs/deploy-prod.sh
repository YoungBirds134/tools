#!/bin/bash

# Production deployment script for FC Trading API with Telegram Bot
# This script handles the complete deployment process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="fc-trading-api"
BACKUP_DIR="/opt/backups/fc-trading"
LOG_FILE="/var/log/fc-trading-deploy.log"

# Functions
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root for security reasons"
    fi
}

# Check system requirements
check_requirements() {
    log "Checking system requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Please install Docker first."
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose first."
    fi
    
    # Check if user is in docker group
    if ! groups | grep -q docker; then
        error "Current user is not in docker group. Run: sudo usermod -aG docker $USER"
    fi
    
    # Check available disk space (minimum 2GB)
    available_space=$(df / | tail -1 | awk '{print $4}')
    if [[ $available_space -lt 2097152 ]]; then
        warn "Less than 2GB disk space available. Consider freeing up space."
    fi
    
    log "System requirements check passed"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    
    sudo mkdir -p "$BACKUP_DIR"
    sudo mkdir -p /var/log/fc-trading
    sudo mkdir -p /opt/fc-trading/ssl
    sudo mkdir -p /opt/fc-trading/nginx
    
    # Set permissions
    sudo chown -R $USER:$USER /opt/fc-trading
    sudo chmod -R 755 /opt/fc-trading
    
    log "Directories created successfully"
}

# Backup existing deployment
backup_existing() {
    if [ -d "/opt/fc-trading/current" ]; then
        log "Creating backup of existing deployment..."
        
        backup_name="fc-trading-$(date +%Y%m%d-%H%M%S)"
        sudo mkdir -p "$BACKUP_DIR/$backup_name"
        
        sudo cp -r /opt/fc-trading/current/* "$BACKUP_DIR/$backup_name/" 2>/dev/null || true
        sudo docker-compose -f /opt/fc-trading/current/docker-compose.prod.yml down || true
        
        log "Backup created: $BACKUP_DIR/$backup_name"
    fi
}

# Validate environment file
validate_env() {
    log "Validating environment configuration..."
    
    if [ ! -f ".env" ]; then
        error "Environment file .env not found. Please create it first."
    fi
    
    # Check required variables
    required_vars=(
        "TELEGRAM_BOT_TOKEN"
        "FC_USERNAME"
        "FC_PASSWORD"
        "FC_ENVIRONMENT"
        "SECRET_KEY"
        "REDIS_URL"
    )
    
    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=" .env; then
            error "Required environment variable $var not found in .env"
        fi
    done
    
    # Validate Telegram bot token format
    if ! grep -E "^TELEGRAM_BOT_TOKEN=[0-9]+:[A-Za-z0-9_-]+$" .env > /dev/null; then
        error "Invalid Telegram bot token format in .env"
    fi
    
    log "Environment validation passed"
}

# Generate SSL certificates (self-signed for development)
generate_ssl() {
    log "Generating SSL certificates..."
    
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        mkdir -p ssl
        
        openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
            -subj "/C=VN/ST=HCM/L=HoChiMinh/O=FC Trading/CN=localhost"
        
        log "SSL certificates generated"
    else
        info "SSL certificates already exist"
    fi
}

# Build and deploy application
deploy_application() {
    log "Building and deploying application..."
    
    # Create deployment directory
    sudo mkdir -p /opt/fc-trading/current
    
    # Copy application files
    sudo cp -r . /opt/fc-trading/current/
    sudo chown -R $USER:$USER /opt/fc-trading/current
    
    # Build Docker images
    cd /opt/fc-trading/current
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    # Start services
    docker-compose -f docker-compose.prod.yml up -d
    
    log "Application deployed successfully"
}

# Health checks
perform_health_checks() {
    log "Performing health checks..."
    
    # Wait for services to start
    sleep 30
    
    # Check Redis
    if ! docker-compose -f /opt/fc-trading/current/docker-compose.prod.yml exec -T redis redis-cli ping | grep -q PONG; then
        error "Redis health check failed"
    fi
    
    # Check API health endpoint
    for i in {1..10}; do
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            log "API health check passed"
            break
        fi
        if [ $i -eq 10 ]; then
            error "API health check failed after 10 attempts"
        fi
        sleep 10
    done
    
    # Check Celery worker
    if ! docker-compose -f /opt/fc-trading/current/docker-compose.prod.yml exec -T celery-worker celery -A app.telegram.tasks.celery_app inspect ping | grep -q pong; then
        warn "Celery worker health check failed - this might be normal during startup"
    fi
    
    log "Health checks completed"
}

# Setup monitoring and alerting
setup_monitoring() {
    log "Setting up monitoring..."
    
    # Create monitoring script
    cat > /opt/fc-trading/monitor.sh << 'EOF'
#!/bin/bash
# Basic monitoring script
cd /opt/fc-trading/current

# Check services
services=("redis" "fc-trading-api" "celery-worker" "celery-beat" "nginx")
for service in "${services[@]}"; do
    if ! docker-compose -f docker-compose.prod.yml ps | grep -q "$service.*Up"; then
        echo "Service $service is down!" | logger -t fc-trading-monitor
        # Add notification logic here (email, Slack, etc.)
    fi
done

# Check disk space
available=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$available" -gt 90 ]; then
    echo "Disk space usage is $available%" | logger -t fc-trading-monitor
fi
EOF

    chmod +x /opt/fc-trading/monitor.sh
    
    # Add to crontab if not exists
    if ! crontab -l 2>/dev/null | grep -q "fc-trading/monitor.sh"; then
        (crontab -l 2>/dev/null; echo "*/5 * * * * /opt/fc-trading/monitor.sh") | crontab -
        log "Monitoring cron job added"
    fi
    
    log "Monitoring setup completed"
}

# Setup log rotation
setup_log_rotation() {
    log "Setting up log rotation..."
    
    sudo tee /etc/logrotate.d/fc-trading > /dev/null << EOF
/var/log/fc-trading/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    sharedscripts
    postrotate
        docker-compose -f /opt/fc-trading/current/docker-compose.prod.yml restart fc-trading-api celery-worker celery-beat
    endscript
}
EOF
    
    log "Log rotation configured"
}

# Cleanup old backups
cleanup_backups() {
    log "Cleaning up old backups..."
    
    # Keep only last 7 backups
    sudo find "$BACKUP_DIR" -maxdepth 1 -type d -name "fc-trading-*" | sort | head -n -7 | sudo xargs rm -rf
    
    log "Backup cleanup completed"
}

# Main deployment process
main() {
    log "Starting FC Trading API deployment..."
    
    check_root
    check_requirements
    create_directories
    validate_env
    backup_existing
    generate_ssl
    deploy_application
    perform_health_checks
    setup_monitoring
    setup_log_rotation
    cleanup_backups
    
    log "Deployment completed successfully!"
    info "Application is available at:"
    info "  - API: https://localhost/docs"
    info "  - Health: https://localhost/health"
    info "  - Monitoring: http://localhost:5555 (Flower)"
    info ""
    info "Important next steps:"
    info "  1. Configure your domain in nginx.conf"
    info "  2. Set up proper SSL certificates for production"
    info "  3. Configure firewall rules"
    info "  4. Set up external monitoring"
    info "  5. Test Telegram bot functionality"
    info ""
    info "Logs are available in /var/log/fc-trading/"
    info "Monitoring: tail -f /var/log/fc-trading-deploy.log"
}

# Error handling
trap 'error "Deployment failed at line $LINENO"' ERR

# Run main function
main "$@"
