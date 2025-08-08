# Quick Start Guide - Lightweight Docker Testing

## Overview
This guide helps you quickly test the FC Trading API using a lightweight Docker Compose setup.

## Prerequisites
- Docker and Docker Compose installed
- Port 8000 and 6379 available on your machine

## Quick Start

### 1. Copy Environment File
```bash
cp .env.test .env
```

### 2. Start Services
```bash
# Using Make (recommended)
make test-up

# Or using Docker Compose directly
docker-compose -f docker-compose.test.yml up -d --build
```

### 3. Run Tests
```bash
# Full test suite
make test-full

# Or run the test script directly
./test-service.sh
```

### 4. Access Services
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Test API Endpoints
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000/

# Test Telegram bot info
curl http://localhost:8000/api/v1/telegram/bot/info
```

## Available Make Commands

```bash
make help           # Show all available commands
make test-up        # Start test services
make test-down      # Stop test services
make test-restart   # Restart test services
make test-logs      # Show logs
make test-clean     # Clean up everything
make test-full      # Run full test suite
make test-api       # Test API endpoints
make test-status    # Show service status
make test-shell     # Get shell access to API container
```

## Services Included

### Lightweight Setup (docker-compose.test.yml)
- **Redis**: Session management and caching
- **FC Trading API**: Main FastAPI application
- **Development mode**: With hot reload and volume mounting

### Removed from Lightweight Setup
- PostgreSQL (uses in-memory storage)
- Celery worker/beat (background tasks disabled)
- Nginx (direct API access)
- Monitoring tools (Prometheus, Grafana, Flower)

## Configuration

### Environment Variables (.env.test)
```env
APP_NAME="FC Trading API - Test"
ENVIRONMENT="development"
DEBUG="true"
REDIS_URL="redis://localhost:6379"
ENABLE_TELEGRAM_BOT="false"  # Enable if you have bot token
```

### Enable Telegram Bot (Optional)
1. Get bot token from @BotFather
2. Update `.env` file:
```env
TELEGRAM_BOT_TOKEN="your_bot_token_here"
ENABLE_TELEGRAM_BOT="true"
```

## Troubleshooting

### Port Conflicts
If ports 8000 or 6379 are in use:
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :6379

# Stop conflicting services
kill -9 <PID>
```

### Service Not Starting
```bash
# Check logs
make test-logs

# Check service status
make test-status

# Rebuild containers
make test-clean
make test-up
```

### API Not Responding
```bash
# Check if container is running
docker ps

# Check API logs
docker-compose -f docker-compose.test.yml logs fc-trading-api

# Get shell access
make test-shell
```

## Development Workflow

1. **Start services**: `make test-up`
2. **Make changes**: Edit code (auto-reload enabled)
3. **Test changes**: `make test-api`
4. **Check logs**: `make test-logs`
5. **Stop services**: `make test-down`

## Performance Notes

This lightweight setup uses:
- **Single worker**: For development testing
- **Development mode**: With debug enabled
- **Volume mounting**: For hot reload
- **Minimal logging**: Reduced log retention
- **No persistence**: Uses in-memory storage where possible

## Next Steps

Once testing is complete, you can:
1. Move to full production setup with `docker-compose.yml`
2. Add monitoring and persistence
3. Configure SSL/TLS
4. Set up proper secrets management

## Cleanup

```bash
# Stop and remove all test containers
make test-clean

# Remove unused Docker resources
docker system prune -a
```
