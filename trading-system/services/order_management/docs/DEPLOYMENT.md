# FC Trading API - Production Deployment Guide

## Overview
This document provides comprehensive instructions for deploying the FC Trading API with Telegram Bot integration in a production environment.

## Architecture

### Services
- **FastAPI Application**: Main trading API with Telegram bot integration
- **Redis**: Session storage and Celery message broker
- **Celery Worker**: Background task processing
- **Celery Beat**: Scheduled task execution
- **Nginx**: Reverse proxy with SSL termination
- **Flower**: Celery monitoring dashboard

### Technology Stack
- FastAPI 0.104.1
- Python Telegram Bot 20.7
- Redis 7.0
- Celery 5.3.4
- Nginx (Alpine)
- Docker & Docker Compose

## Prerequisites

### System Requirements
- Linux server (Ubuntu 20.04+ recommended)
- Docker 20.10+
- Docker Compose 2.0+
- Minimum 2GB RAM
- Minimum 10GB disk space
- SSL certificate (Let's Encrypt recommended)

### Domain Setup
- Domain name pointing to server IP
- SSL certificate for HTTPS
- Firewall configuration (ports 80, 443)

## Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo>
cd fc-trading.py
cp .env.production .env
```

### 2. Configure Environment
Edit `.env` with your credentials:
```bash
# Required configurations
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook
FC_USERNAME=your-fc-username
FC_PASSWORD=your-fc-password
SECRET_KEY=your-secret-key
```

### 3. Deploy
```bash
./deploy-prod.sh
```

## Detailed Configuration

### Environment Variables

#### Telegram Bot Configuration
```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram/webhook
TELEGRAM_WEBHOOK_SECRET=your-webhook-secret
TELEGRAM_ADMIN_CHAT_IDS=123456789,987654321
```

#### FastConnect Trading API
```bash
FC_ENVIRONMENT=LIVE  # or DEMO
FC_USERNAME=your-username
FC_PASSWORD=your-password
FC_PIN=your-pin
FC_BASE_URL=https://fc-data.ssi.com.vn
FC_STREAMING_URL=https://fc-md.ssi.com.vn
```

#### Security Configuration
```bash
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=your-domain.com,localhost
CORS_ORIGINS=https://your-domain.com
```

### SSL Configuration

#### Using Let's Encrypt
```bash
# Install certbot
sudo apt install certbot

# Generate certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
```

#### Using Self-Signed (Development)
```bash
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

### Nginx Configuration

Update `nginx.conf` with your domain:
```nginx
server_name your-domain.com;
```

For multiple domains:
```nginx
server_name your-domain.com www.your-domain.com;
```

## Deployment Process

### Automated Deployment
The `deploy-prod.sh` script handles:

1. **System Requirements Check**
   - Docker installation
   - Disk space
   - User permissions

2. **Environment Validation**
   - Required variables
   - Token format validation
   - Configuration syntax

3. **Backup Creation**
   - Previous deployment backup
   - Database snapshots
   - Configuration files

4. **Application Deployment**
   - Docker image building
   - Service orchestration
   - Health checks

5. **Monitoring Setup**
   - Log rotation
   - Health monitoring
   - Alerting configuration

### Manual Deployment Steps

If you prefer manual deployment:

```bash
# 1. Build images
docker-compose -f docker-compose.prod.yml build

# 2. Start services
docker-compose -f docker-compose.prod.yml up -d

# 3. Check health
curl -f http://localhost:8000/health

# 4. Verify services
docker-compose -f docker-compose.prod.yml ps
```

## Monitoring and Maintenance

### Health Checks

#### API Health
```bash
curl -f https://your-domain.com/health
```

#### Service Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

#### Logs
```bash
# Application logs
docker-compose logs fc-trading-api

# Celery worker logs
docker-compose logs celery-worker

# All services
docker-compose logs -f
```

### Flower Monitoring
Access Celery monitoring at: `http://monitoring.your-domain.com`

Default credentials (change in production):
- Username: admin
- Password: set in nginx config

### Log Files
- Application: `/var/log/fc-trading/app.log`
- Deployment: `/var/log/fc-trading-deploy.log`
- Nginx: `/var/log/nginx/`

## Scaling and Performance

### Horizontal Scaling

#### Multiple Workers
```yaml
# In docker-compose.prod.yml
celery-worker:
  deploy:
    replicas: 4
```

#### Load Balancing
```nginx
upstream fc_trading_api {
    server fc-trading-api-1:8000;
    server fc-trading-api-2:8000;
    server fc-trading-api-3:8000;
}
```

### Performance Tuning

#### FastAPI Workers
```bash
WORKERS=4  # In .env
```

#### Redis Optimization
```bash
# In docker-compose.prod.yml
redis:
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

#### Nginx Optimization
```nginx
worker_processes auto;
worker_connections 1024;
```

## Security Best Practices

### Secrets Management
- Use environment variables for sensitive data
- Never commit secrets to version control
- Rotate secrets regularly
- Use strong, unique passwords

### Network Security
```bash
# Firewall configuration
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### SSL/TLS Configuration
- Use TLS 1.2+ only
- Strong cipher suites
- HSTS headers
- Certificate pinning

### Access Control
- Limit admin access
- Use strong authentication
- Monitor access logs
- Regular security audits

## Backup and Recovery

### Automated Backups
```bash
# Create backup script
cat > /opt/scripts/backup-fc-trading.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/fc-trading"

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup application data
docker-compose -f /opt/fc-trading/current/docker-compose.prod.yml exec -T redis redis-cli BGSAVE
cp /var/lib/docker/volumes/fc-trading_redis_data/_data/dump.rdb "$BACKUP_DIR/$DATE/"

# Backup configuration
cp -r /opt/fc-trading/current "$BACKUP_DIR/$DATE/app"

# Compress backup
tar -czf "$BACKUP_DIR/fc-trading-$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"
rm -rf "$BACKUP_DIR/$DATE"

# Clean old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x /opt/scripts/backup-fc-trading.sh

# Schedule backup
echo "0 2 * * * /opt/scripts/backup-fc-trading.sh" | crontab -
```

### Recovery Process
```bash
# 1. Stop services
docker-compose -f docker-compose.prod.yml down

# 2. Restore Redis data
tar -xzf /opt/backups/fc-trading/fc-trading-YYYYMMDD_HHMMSS.tar.gz
cp dump.rdb /var/lib/docker/volumes/fc-trading_redis_data/_data/

# 3. Restore application
cp -r app/* /opt/fc-trading/current/

# 4. Start services
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check logs
docker-compose logs

# Check system resources
free -h
df -h

# Check ports
netstat -tlnp
```

#### Telegram Bot Not Responding
```bash
# Check webhook
curl -X GET "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo"

# Check logs
docker-compose logs fc-trading-api | grep telegram

# Test bot connection
docker-compose exec fc-trading-api python -c "
from app.telegram.bot import telegram_bot
import asyncio
asyncio.run(telegram_bot.get_me())
"
```

#### High Memory Usage
```bash
# Check container stats
docker stats

# Check Redis memory
docker-compose exec redis redis-cli info memory

# Optimize Redis
docker-compose exec redis redis-cli config set maxmemory 512mb
```

### Performance Issues

#### Slow API Response
```bash
# Check worker count
grep WORKERS .env

# Check database connections
docker-compose exec fc-trading-api python -c "
from app.services.fc_service import FCService
print('FC API Status')
"

# Monitor requests
tail -f /var/log/nginx/access.log
```

#### Celery Tasks Failing
```bash
# Check Celery status
docker-compose exec celery-worker celery -A app.telegram.tasks.celery_app inspect active

# Check Redis connection
docker-compose exec celery-worker python -c "
import redis
r = redis.from_url('redis://redis:6379')
print(r.ping())
"
```

## Maintenance

### Regular Tasks

#### Daily
- Check service health
- Monitor resource usage
- Review error logs
- Verify backups

#### Weekly
- Update dependencies
- Security patches
- Performance review
- Log rotation

#### Monthly
- Full system backup
- Security audit
- Performance optimization
- Documentation update

### Update Process

#### Application Updates
```bash
# 1. Backup current deployment
./deploy-prod.sh  # Handles backup automatically

# 2. Update code
git pull origin main

# 3. Update dependencies
pip install -r requirements.txt

# 4. Rebuild and deploy
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

#### System Updates
```bash
# 1. Update system packages
sudo apt update && sudo apt upgrade

# 2. Update Docker
curl -fsSL https://get.docker.com | sh

# 3. Restart services
docker-compose -f docker-compose.prod.yml restart
```

## Support and Contact

### Documentation
- API Documentation: `https://your-domain.com/docs`
- Telegram Bot Guide: `TELEGRAM_BOT.md`
- Development Setup: `README.md`

### Monitoring Endpoints
- Health Check: `https://your-domain.com/health`
- Metrics: `https://your-domain.com/metrics`
- Flower: `http://monitoring.your-domain.com`

### Emergency Contacts
- System Administrator: admin@your-company.com
- Development Team: dev@your-company.com
- On-call Support: +84-xxx-xxx-xxxx

Remember to customize this guide with your specific domain, credentials, and contact information before deployment.
