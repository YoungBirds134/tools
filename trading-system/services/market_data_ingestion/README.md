# Market Data Ingestion Service

Enhanced market data ingestion service for Vietnamese stock exchanges (HOSE, HNX, UPCOM) using SSI FastConnect API.

## Features

### Market Data Capabilities
- **Real-time Quotes**: Live price data with bid/ask, volume, and market statistics
- **Trade Data**: Individual trade executions with price, volume, and timing
- **Order Book**: Depth of market with buy/sell levels up to 10 levels
- **Historical Data**: Historical price data with multiple timeframes
- **Market Indices**: VN-Index, HNX-Index, UPCOM-Index tracking
- **WebSocket Streaming**: Real-time data streaming for subscribed symbols

### Vietnamese Market Support
- **Trading Sessions**: Support for PRE_OPEN, CONTINUOUS, INTERMISSION, CLOSE sessions
- **Price Types**: Ceiling (trần trên), Floor (trần dưới), Reference (giá tham chiếu) prices
- **Market Exchanges**: HOSE, HNX, UPCOM exchanges
- **Foreign Trading**: Foreign buy/sell volume tracking
- **Vietnamese Symbols**: VN30, VIC, VCB, FPT, HPG, TCB, MSN, BID default tracking

### Production Features
- **Circuit Breaker**: Fault tolerance with automatic recovery
- **Rate Limiting**: Token bucket rate limiting for API calls
- **Retry Logic**: Exponential backoff with configurable retry attempts
- **Structured Logging**: JSON logging with correlation IDs
- **Health Checks**: Readiness and liveness probes
- **Metrics**: Prometheus-compatible metrics endpoint
- **CORS Support**: Configurable cross-origin resource sharing

### Data Processing
- **Background Collection**: Periodic data collection for configured symbols
- **Data Validation**: Pydantic models with Vietnamese market validation
- **Error Handling**: Comprehensive error handling with circuit breaker
- **Caching**: Redis caching for improved performance
- **Message Streaming**: Kafka integration for event streaming

## API Endpoints

### Health & Monitoring
- `GET /health` - Health check
- `GET /health/ready` - Readiness check with SSI client status
- `GET /metrics` - Service and client metrics

### Market Data
- `POST /api/v1/market-data` - Get market data for multiple symbols
- `GET /api/v1/quote/{symbol}` - Get detailed quote for symbol
- `GET /api/v1/trades/{symbol}` - Get recent trades for symbol
- `GET /api/v1/orderbook/{symbol}` - Get order book depth
- `POST /api/v1/historical` - Get historical price data
- `GET /api/v1/indices` - Get market indices data

### Real-time Streaming
- `WebSocket /ws/stream` - Real-time data streaming

## Configuration

### Environment Variables
```bash
# SSI API Configuration
MARKET_DATA_CONSUMER_ID=your_consumer_id
MARKET_DATA_CONSUMER_SECRET=your_consumer_secret
MARKET_DATA_PRIVATE_KEY=your_base64_private_key
MARKET_DATA_PUBLIC_KEY=your_base64_public_key

# Market Configuration
MARKET_DATA_SYMBOLS=["VN30", "VIC", "VCB"]
MARKET_DATA_REFRESH_INTERVAL=5
MARKET_DATA_ENABLE_REAL_TIME=true

# Database & Cache
MARKET_DATA_DATABASE_URL=postgresql://user:pass@localhost:5432/market_data
MARKET_DATA_REDIS_URL=redis://localhost:6379

# Kafka
MARKET_DATA_KAFKA_BOOTSTRAP_SERVERS=["localhost:9092"]
MARKET_DATA_KAFKA_TOPIC_PREFIX=market_data
```

## Usage Examples

### Get Real-time Quote
```python
import httpx

response = httpx.get("http://localhost:8001/api/v1/quote/VIC")
quote = response.json()
print(f"VIC Price: {quote['last_price']} VND")
```

### Stream Real-time Data
```python
import websockets
import json

async def stream_data():
    uri = "ws://localhost:8001/ws/stream"
    async with websockets.connect(uri) as websocket:
        # Subscribe to symbols
        subscription = {
            "symbols": ["VIC", "VCB", "FPT"],
            "data_types": ["QUOTE"]
        }
        await websocket.send(json.dumps(subscription))
        
        # Receive data
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")
```

### Get Historical Data
```python
import httpx
from datetime import date

historical_request = {
    "symbol": "VIC",
    "from_date": "2024-01-01",
    "to_date": "2024-01-31",
    "resolution": "1D"
}

response = httpx.post(
    "http://localhost:8001/api/v1/historical",
    json=historical_request
)
historical_data = response.json()
```

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit configuration
nano .env

# Run service
python -m uvicorn main:app --reload --port 8001
```

### Docker
```bash
# Build image
docker build -t market-data-ingestion .

# Run container
docker run -p 8001:8001 --env-file .env market-data-ingestion
```

## Architecture

### Components
1. **SSI Client**: Enhanced HTTP client with circuit breaker and rate limiting
2. **FastAPI App**: RESTful API with WebSocket support
3. **Background Tasks**: Periodic data collection and processing
4. **Data Models**: Pydantic models with Vietnamese market validation
5. **Monitoring**: Health checks, metrics, and structured logging

### Data Flow
1. SSI FastConnect API → SSI Client → Data Processing → API Endpoints
2. Background Collection → Kafka → Database Storage
3. WebSocket Streaming → Real-time Data → Client Applications

### Resilience Patterns
- **Circuit Breaker**: Prevents cascade failures
- **Rate Limiting**: Respects API limits
- **Retry Logic**: Handles transient failures
- **Health Checks**: Kubernetes-ready probes
- **Graceful Shutdown**: Clean resource cleanup

## Monitoring

### Metrics Available
- Request count and error rates
- SSI client statistics
- Circuit breaker state
- Response times
- Background task status

### Logging
- Structured JSON logging
- Request/response tracing
- Error context with stack traces
- Performance metrics

## Security

### Authentication
- SSI API authentication with HMAC signatures
- Token management with automatic refresh

### Network Security
- CORS configuration
- Trusted host middleware
- Rate limiting protection

## Vietnamese Market Specifics

### Trading Sessions
- **8:00-8:45**: Pre-opening (HOSE)
- **9:00-11:30**: Morning session
- **13:00-15:00**: Afternoon session
- **15:00-15:15**: Closing auction
- **15:30-16:30**: After hours trading

### Price Limits
- **Ceiling Price**: Maximum allowed price (trần trên)
- **Floor Price**: Minimum allowed price (trần dưới)
- **Reference Price**: Previous closing price (giá tham chiếu)

### Supported Exchanges
- **HOSE**: Ho Chi Minh Stock Exchange
- **HNX**: Hanoi Stock Exchange
- **UPCOM**: Unlisted Public Company Market
