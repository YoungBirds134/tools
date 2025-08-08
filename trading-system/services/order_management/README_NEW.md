# Order Management Service

Production-ready microservice for managing trading orders in Vietnamese stock market with SSI FastConnect integration.

## Overview

The Order Management Service is a critical component of the quantum trading system, responsible for handling all order lifecycle management including creation, modification, cancellation, and execution tracking. It provides comprehensive Vietnamese market compliance, real-time position tracking, and portfolio management capabilities.

## Features

### Core Features
- **Real-time Order Management**: Create, modify, cancel orders with real-time status updates
- **Vietnamese Market Compliance**: Full support for HOSE, HNX, and UPCOM markets
- **Order Types**: LO, ATO, ATC, MTL, MOK, MAK, PLO with market-specific validation
- **Trading Session Management**: Automatic session detection and trading rules enforcement
- **Portfolio Tracking**: Real-time position updates and portfolio performance analytics
- **Risk Management**: Position limits, buying power calculations, and exposure monitoring

### Advanced Features
- **SSI FastConnect Integration**: Direct connection to Vietnamese stock exchange
- **Async Processing**: High-performance async operations for real-time trading
- **Database Persistence**: PostgreSQL with SQLAlchemy ORM for data integrity
- **Redis Caching**: Fast session management and data caching
- **Comprehensive Logging**: Structured logging with request tracing
- **Health Monitoring**: Detailed health checks and metrics collection

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- SSI FastConnect API access (optional for simulation mode)

### Installation

1. **Clone and Setup**
```bash
# Navigate to service directory
cd services/order_management

# Install dependencies
./deploy.sh install

# Setup database
./deploy.sh setup
```

2. **Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Configure your environment variables
# DATABASE_URL=postgresql://user:password@localhost:5432/trading_db
# REDIS_URL=redis://localhost:6379/0
# SSI_API_KEY=your_ssi_api_key
# SECRET_KEY=your_secret_key
```

3. **Start Service**
```bash
# Development mode with hot reload
./deploy.sh dev

# Production mode
./deploy.sh start
```

4. **Verify Installation**
```bash
# Check service status
./deploy.sh status

# Access API documentation
curl http://localhost:8001/docs
```

## API Documentation

### Base URL
```
http://localhost:8001/api/v1
```

### Authentication
All endpoints require JWT token authentication:
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8001/api/v1/orders
```

### Core Endpoints

#### Orders Management
- `POST /orders` - Create new order
- `GET /orders` - List orders with filtering
- `GET /orders/{order_id}` - Get specific order
- `PUT /orders/{order_id}` - Modify existing order
- `DELETE /orders/{order_id}` - Cancel order
- `GET /orders/{order_id}/executions` - Get order executions

#### Portfolio Management
- `GET /positions` - Get current positions
- `GET /positions/{symbol}` - Get specific position
- `GET /positions/summary/portfolio` - Portfolio summary
- `GET /positions/history/changes` - Position history
- `GET /positions/buying-power/available` - Available buying power

#### Account Management
- `GET /accounts/profile` - Account profile information
- `GET /accounts/balance` - Account balance and cash
- `GET /accounts/trading-limits` - Trading limits and restrictions
- `GET /accounts/trading-session` - Current trading session
- `GET /accounts/permissions` - Account permissions

### Example Requests

#### Create Order
```bash
curl -X POST "http://localhost:8001/api/v1/orders" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "symbol": "VIC",
  "side": "BUY",
  "order_type": "LO",
  "quantity": 100,
  "price": 85.5,
  "market": "HOSE",
  "time_in_force": "DAY"
}'
```

#### Get Portfolio Summary
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "http://localhost:8001/api/v1/positions/summary/portfolio"
```

## Architecture

### Service Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Order Service │    │Portfolio Service│
│   (main_new.py) │────│  (Core Logic)   │────│  (Positions)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Database      │    │   Redis Cache   │    │  Trading Session│
│  (PostgreSQL)   │    │   (Sessions)    │    │    Service      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Models
- **Order**: Order information with status tracking
- **OrderExecution**: Execution details and fills
- **Position**: Stock positions with real-time values
- **PositionHistory**: Historical position changes

### Vietnamese Market Compliance
- **Trading Sessions**: Morning auction, continuous sessions, closing auction
- **Market Rules**: HOSE, HNX, UPCOM specific order types and restrictions
- **Order Validation**: Price bands, lot sizes, trading hours enforcement
- **Risk Controls**: Position limits, concentration limits, buying power checks

## Configuration

### Environment Variables
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/trading_db
DATABASE_ECHO=false

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=optional_password

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SSI FastConnect API
SSI_API_URL=https://fc-data.ssi.com.vn
SSI_API_KEY=your_ssi_api_key
SSI_API_SECRET=your_ssi_api_secret

# Service Configuration
DEBUG=false
ENVIRONMENT=production
HOST=0.0.0.0
PORT=8001
LOG_LEVEL=info

# Trading Configuration
DEFAULT_MARKET=HOSE
MAX_ORDER_SIZE=1000000
MAX_POSITIONS=50
```

### Database Configuration
The service uses PostgreSQL with SQLAlchemy ORM. Database tables are automatically created on first run.

### Redis Configuration
Redis is used for session management, caching market data, and storing temporary order states.

## Vietnamese Market Integration

### Supported Markets
- **HOSE (Ho Chi Minh Stock Exchange)**: Main board stocks
- **HNX (Hanoi Stock Exchange)**: Secondary board stocks  
- **UPCOM**: Unlisted public company market

### Order Types
- **LO (Limit Order)**: Standard limit orders
- **ATO (At The Open)**: Market orders for opening auction
- **ATC (At The Close)**: Market orders for closing auction
- **MTL (Match Till Limit)**: Fill or kill orders
- **MOK (Market Order Kill)**: Immediate or cancel orders
- **MAK (Market All Kill)**: All or nothing orders
- **PLO (Post Limit Order)**: Post-session limit orders

### Trading Sessions
```
09:00-09:15  Morning Auction (ATO/LO only)
09:15-11:30  Continuous Morning Session
11:30-13:00  Lunch Break (no trading)
13:00-14:30  Continuous Afternoon Session
14:30-14:45  Closing Auction (ATC/LO only)
14:45-15:00  Post-Market Session (PLO only)
```

## Development

### Project Structure
```
order_management/
├── app/
│   ├── __init__.py
│   ├── main_new.py          # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # Data models and schemas
│   ├── routes/              # API endpoints
│   │   ├── orders.py        # Order management endpoints
│   │   ├── positions.py     # Portfolio endpoints
│   │   └── accounts.py      # Account endpoints
│   └── services/            # Business logic
│       ├── order_service.py # Order management service
│       ├── portfolio_service.py # Portfolio service
│       └── trading_session_service.py # Session management
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── deploy.sh               # Deployment script
└── README.md               # This file
```

### Running Tests
```bash
# Run all tests
./deploy.sh test

# Run specific test file
pytest tests/test_orders.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

### Development Workflow
1. Start service in development mode: `./deploy.sh dev`
2. Make changes to code (auto-reload enabled)
3. Test changes: `./deploy.sh test`
4. Check service status: `./deploy.sh status`

## Deployment

### Local Deployment
```bash
# Install dependencies
./deploy.sh install

# Setup database
./deploy.sh setup

# Start service
./deploy.sh start

# Check status
./deploy.sh status
```

### Docker Deployment
```bash
# Build image
docker build -t order-management:latest .

# Run container
docker run -d \
  --name order-management \
  -p 8001:8001 \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  order-management:latest
```

### Production Considerations
- Use PostgreSQL with proper connection pooling
- Configure Redis for session persistence
- Set up proper logging and monitoring
- Configure SSL/TLS for API endpoints
- Implement rate limiting and API throttling
- Set up health checks and alerting

## Monitoring and Logging

### Health Checks
- `/health` - Basic health status
- `/health/detailed` - Comprehensive health check
- `/health/live` - Kubernetes liveness probe
- `/health/ready` - Kubernetes readiness probe

### Metrics
- `/metrics` - Service metrics (Prometheus compatible)
- Order processing rates
- Database connection status
- Cache hit rates
- Error rates

### Logging
Structured logging with request correlation:
```json
{
  "timestamp": "2024-01-16T10:30:00Z",
  "level": "INFO",
  "service": "order_management",
  "request_id": "req_123456",
  "message": "Order created successfully",
  "order_id": "ORD_789",
  "account_id": "ACC_123"
}
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database status
   pg_ctl status
   
   # Verify connection string
   psql postgresql://user:password@localhost:5432/trading_db
   ```

2. **Redis Connection Failed**
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Verify Redis configuration
   redis-cli info
   ```

3. **Service Won't Start**
   ```bash
   # Check if port is available
   lsof -i :8001
   
   # Check logs
   ./deploy.sh logs
   ```

4. **SSI API Issues**
   ```bash
   # Test SSI connection
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        https://fc-data.ssi.com.vn/api/v1/status
   ```

### Debug Mode
```bash
# Start with debug logging
LOG_LEVEL=debug ./deploy.sh dev

# Enable SQL query logging
DATABASE_ECHO=true ./deploy.sh dev
```

## Security

### Authentication
- JWT token-based authentication
- Token expiration and refresh
- Role-based access control

### Data Protection
- Encrypted database connections
- Secure Redis connections
- API rate limiting
- Input validation and sanitization

### Trading Security
- Order validation and limits
- Position monitoring
- Risk management controls
- Audit logging

## Support

### Contact Information
- **Development Team**: trading-dev@company.com
- **Operations Team**: trading-ops@company.com
- **Emergency**: +84-xxx-xxx-xxxx

### Documentation
- API Documentation: http://localhost:8001/docs
- Technical Specification: /docs/technical/
- Deployment Guide: /docs/deployment/

### License
Copyright (c) 2024 Trading System. All rights reserved.

---

**Note**: This service handles real financial transactions. Always test thoroughly in a sandbox environment before deploying to production.
