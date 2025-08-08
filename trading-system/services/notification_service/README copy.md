# 🔔 Trading Notification Service

Enterprise-grade notification service for trading platform with Telegram bot integration.

## 🚀 Features

### 📊 Notification Management
- **Multi-channel delivery**: Telegram, Email, SMS, Push notifications
- **Priority-based routing**: Critical, High, Medium, Low priority levels
- **Scheduled notifications**: Send notifications at specific times
- **Delivery tracking**: Track notification status and delivery results
- **User preferences**: Custom notification settings per user

### 🤖 Telegram Bot Integration
- **Interactive menus**: Rich keyboard navigation
- **Real-time notifications**: Instant trading alerts and updates
- **User management**: Subscribe/unsubscribe functionality
- **Settings control**: Configure notification preferences via chat
- **Status monitoring**: Check service health and statistics

### 🏗️ Enterprise Architecture
- **FastAPI framework**: High-performance async API
- **Redis caching**: Session management and notification storage
- **Celery integration**: Background task processing
- **Docker containerization**: Production-ready deployment
- **Nginx reverse proxy**: Load balancing and rate limiting

### 🔐 Security & Monitoring
- **Rate limiting**: API endpoint protection
- **User authorization**: Secure access control
- **Health checks**: Kubernetes-ready probes
- **Logging & metrics**: Comprehensive monitoring
- **Error handling**: Graceful failure management

## 📁 Project Structure

```
notification-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── api/
│   │   └── routers.py            # API endpoints
│   ├── core/
│   │   └── config.py             # Configuration management
│   ├── models/
│   │   ├── telegram_models.py    # Telegram data models
│   │   └── notification_models.py # Notification data models
│   ├── services/
│   │   └── notification_service.py # Core notification logic
│   ├── telegram/
│   │   ├── handlers.py           # Telegram bot handlers
│   │   ├── keyboards.py          # Interactive keyboards
│   │   ├── utils.py              # Utility functions
│   │   └── session.py            # Session management
│   └── utils/
├── tests/                        # Test suite
├── docs/                         # Documentation
├── docker-compose.yml            # Multi-service setup
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
├── nginx.conf                    # Reverse proxy config
├── redis.conf                    # Redis configuration
└── .env.example                  # Environment template
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- Redis
- Docker & Docker Compose (optional)
- Telegram Bot Token

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd notification-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your settings:

```bash
# Required settings
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather
AUTHORIZED_USERS=["123456789"]  # Your Telegram chat ID
REDIS_URL=redis://localhost:6379/0

# Optional settings
DEBUG=true
LOG_LEVEL=INFO
```

### 3. Run with Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f notification-service

# Stop services
docker-compose down
```

### 4. Run Locally (Development)

```bash
# Start Redis
redis-server

# Start notification service
python -m app.main

# Or with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 📚 API Documentation

### Base URL
- Development: `http://localhost:8001`
- Production: `https://your-domain.com`

### Key Endpoints

#### Send Notification
```http
POST /api/v1/notifications/send
Content-Type: application/json

{
  "user_id": "123456789",
  "notification_type": "trading_alert",
  "title": "Order Executed",
  "message": "Your buy order for AAPL has been executed",
  "priority": "high"
}
```

#### Get User Notifications
```http
GET /api/v1/notifications/{user_id}?limit=20
```

#### Subscribe User
```http
POST /api/v1/users/{user_id}/subscribe
```

#### Health Check
```http
GET /api/v1/health/
```

### Interactive Documentation
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## 🤖 Telegram Bot Usage

### Commands
- `/start` - Initialize bot and show welcome
- `/help` - Show help and available commands
- `/menu` - Display main menu
- `/status` - Check service status
- `/settings` - Configure notification preferences

### Features
- **Interactive Menus**: Navigate using button keyboards
- **Real-time Notifications**: Receive trading alerts instantly
- **Settings Management**: Control notification preferences
- **Status Monitoring**: Check service health and statistics

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather | Required |
| `AUTHORIZED_USERS` | Allowed user chat IDs | `[]` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `WEBHOOK_MODE` | Use webhook instead of polling | `false` |

### Notification Types

- `trading_alert` - Trading-related notifications
- `account_update` - Account balance and status changes
- `system_maintenance` - System maintenance notifications
- `security_alert` - Security-related alerts
- `price_alert` - Price movement notifications

### Priority Levels

- `critical` - Immediate attention required
- `high` - Important but not urgent
- `medium` - Standard notifications
- `low` - Informational messages

## 🚀 Deployment

### Docker Production Setup

```bash
# Production environment
export TELEGRAM_BOT_TOKEN=your-production-token
export AUTHORIZED_USERS='["user1", "user2"]'

# Start production stack
docker-compose -f docker-compose.yml up -d

# Scale workers
docker-compose up --scale celery-worker=3 -d
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notification-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: notification-service
  template:
    spec:
      containers:
      - name: notification-service
        image: notification-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379/0"
        readinessProbe:
          httpGet:
            path: /api/v1/health/ready
            port: 8001
        livenessProbe:
          httpGet:
            path: /api/v1/health/live
            port: 8001
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_notification_service.py

# Send test notification
curl -X POST "http://localhost:8001/api/v1/notifications/test/123456789"
```

## 📊 Monitoring

### Health Checks
- Liveness: `/api/v1/health/live`
- Readiness: `/api/v1/health/ready`
- Status: `/api/v1/health/`

### Metrics
- Service uptime and performance
- Notification delivery rates
- User engagement statistics
- Error rates and response times

### Logging
Structured logging with multiple levels:
- `ERROR`: Critical issues requiring attention
- `WARNING`: Potential issues to monitor
- `INFO`: General operational information
- `DEBUG`: Detailed debugging information

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and API docs
- **Issues**: Create GitHub issue for bugs
- **Discussions**: Use GitHub discussions for questions
- **Email**: contact@your-domain.com

## 🔄 Changelog

### v1.0.0 (2025-01-16)
- ✨ Initial release
- 🔔 Multi-channel notification support
- 🤖 Telegram bot integration
- 🚀 FastAPI production setup
- 🐳 Docker containerization
- 📊 Health monitoring
- 🔐 Security features

---

**Built with ❤️ for enterprise trading platforms**
