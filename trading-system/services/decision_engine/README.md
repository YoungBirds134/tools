# Decision Engine Service

Vietnamese Stock Trading Decision Engine - Core trading decision logic and rule management.

## Overview

The Decision Engine Service is the central component that aggregates signals from Technical Analysis and Prediction services to make informed trading decisions. It implements sophisticated rule-based logic with Vietnamese market specialization.

## Features

### Core Decision Making
- **Multi-Signal Aggregation**: Combines signals from technical analysis, ML predictions, and market sentiment
- **Rule-Based Engine**: Configurable trading rules with priority-based execution
- **Risk Assessment**: Comprehensive risk analysis for each trading decision
- **Vietnamese Market Rules**: Built-in support for HOSE, HNX, and UPCOM trading regulations

### Decision Types
- **BUY**: Long position recommendations
- **SELL**: Short/exit position recommendations  
- **HOLD**: Maintain current position
- **CLOSE_POSITION**: Close existing positions
- **REDUCE_POSITION**: Partial position reduction
- **INCREASE_POSITION**: Position size increase

### Risk Management
- **Position Sizing**: Automatic calculation based on risk tolerance
- **Exposure Limits**: Portfolio and sector exposure controls
- **Stop Loss/Take Profit**: Automated risk management levels
- **Market Condition Adaptation**: Decision adjustment based on market volatility

### Vietnamese Market Specialization
- **Trading Sessions**: Morning (9:00-11:30), Afternoon (13:00-15:00)
- **Lot Size Validation**: 100-share lot requirements
- **Price Limits**: Ceiling/floor price validations
- **Market Hours**: Automatic trading hour enforcement

## API Endpoints

### Decision Making
```
POST /decisions                 - Make single symbol decision
POST /decisions/batch          - Make batch decisions for multiple symbols
GET  /decisions/history        - Get decision history with filtering
```

### Signal Management
```
GET  /signals/{symbol}         - Get active signals for symbol
GET  /market-context          - Get current market context
```

### Rule Management
```
GET  /rules                   - Get all trading rules
POST /rules                   - Create new trading rule
PUT  /rules/{rule_id}         - Enable/disable trading rule
```

### Monitoring
```
GET  /health                  - Service health check
GET  /metrics                 - Prometheus metrics
```

## Configuration

### Environment Variables

See `.env.example` for complete configuration options:

- **Service**: Port, debug settings, logging configuration
- **Database**: PostgreSQL connection for decision storage
- **Redis**: Caching and session management
- **External Services**: Integration with other microservices
- **Trading**: Vietnamese market rules and risk parameters
- **Security**: JWT tokens and CORS settings

### Signal Weights

Configure signal source weights in environment:
```bash
TECHNICAL_ANALYSIS_WEIGHT=0.4
PREDICTION_MODEL_WEIGHT=0.3
MARKET_SENTIMENT_WEIGHT=0.2
RISK_MANAGEMENT_WEIGHT=0.1
```

### Risk Thresholds

Set risk management parameters:
```bash
MAX_PORTFOLIO_VAR=0.05
MAX_SINGLE_POSITION_RISK=0.02
STOP_LOSS_PERCENT=5.0
TAKE_PROFIT_PERCENT=10.0
```

## Usage Examples

### Single Decision Request

```python
import httpx

# Make single decision
decision_request = {
    "symbol": "VCB",
    "current_price": 85500,
    "current_position": 0,
    "available_capital": 100000000,
    "market": "HOSE",
    "strategy": "balanced"
}

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8004/decisions",
        json=decision_request
    )
    decision = response.json()
    print(f"Decision: {decision['decision_type']}")
    print(f"Confidence: {decision['confidence_score']:.2f}")
```

### Batch Decision Request

```python
batch_request = {
    "symbols": ["VCB", "VIC", "VHM", "MSN", "HPG"],
    "portfolio_context": {
        "portfolio_id": "PORTFOLIO_001",
        "total_value": 1000000000,
        "available_cash": 200000000,
        "invested_value": 800000000,
        "number_of_positions": 5,
        "max_position_size": 100000000,
        "max_sector_exposure": 200000000,
        "max_daily_trades": 10,
        "trades_today": 2
    },
    "strategy": "aggressive"
}

response = await client.post(
    "http://localhost:8004/decisions/batch",
    json=batch_request
)
```

### Create Trading Rule

```python
rule_request = {
    "rule_id": "vn30_only",
    "rule_name": "VN30 Stocks Only",
    "rule_type": "filter",
    "conditions": {
        "allowed_symbols": ["VCB", "VIC", "VHM", "MSN", "HPG"]
    },
    "actions": {
        "block_trading": True
    },
    "priority": 8,
    "enabled": True,
    "symbols": None,
    "markets": ["HOSE"],
    "created_by": "strategy_team"
}

response = await client.post(
    "http://localhost:8004/rules",
    json=rule_request
)
```

## Decision Logic

### Signal Aggregation

1. **Weight-based Scoring**: Each signal source has configurable weight
2. **Confidence Adjustment**: Signal confidence modifies final score
3. **Consensus Building**: Multiple signals create stronger decisions
4. **Conflict Resolution**: Opposing signals reduce overall confidence

### Rule Execution

1. **Priority Order**: Rules execute by priority (1-10)
2. **Condition Evaluation**: Check rule applicability
3. **Action Application**: Apply rule actions to decision
4. **Impact Assessment**: Track rule influence on final decision

### Risk Assessment

1. **Position Risk**: Calculate individual position exposure
2. **Portfolio Risk**: Assess overall portfolio impact
3. **Market Risk**: Factor in current market conditions
4. **Liquidity Risk**: Consider stock liquidity and volume

## Vietnamese Market Rules

### Default Rules

1. **Trading Hours Check**: Block trading outside market hours
2. **Risk Limit Check**: Enforce maximum position exposure
3. **Minimum Volume Check**: Ensure adequate liquidity
4. **Lot Size Validation**: Ensure 100-share multiples
5. **Price Limit Check**: Validate against ceiling/floor prices

### Market Sessions

- **Morning**: 09:00-11:30 (GMT+7)
- **Afternoon**: 13:00-15:00 (GMT+7)
- **ATO/ATC**: Special session handling
- **Closed**: No trading allowed

## Performance and Monitoring

### Metrics

- **Decision Latency**: Average decision processing time
- **Confidence Distribution**: Decision confidence levels
- **Signal Activity**: Active signals by source and type
- **Rule Execution**: Rule performance and usage
- **Error Rates**: Decision processing errors

### Health Checks

The service provides comprehensive health monitoring:
- Redis connectivity status
- Decision engine status
- Active rules count
- Decision history size

### Logging

Structured JSON logging with:
- Decision details and reasoning
- Signal processing information
- Rule execution results
- Performance metrics
- Error tracking

## Integration

### Input Services

- **Technical Analysis Service** (Port 8002): Technical indicators and signals
- **Prediction Service** (Port 8003): ML-based price predictions
- **Market Data Service** (Port 8001): Real-time market data
- **Risk Management Service** (Port 8005): Risk assessments

### Output Services

- **Order Management Service** (Port 8000): Execute trading decisions
- **Portfolio Service**: Update portfolio positions
- **Notification Service**: Alert on important decisions

### Data Flow

1. **Signal Collection**: Gather signals from multiple sources
2. **Context Assembly**: Build market and portfolio context
3. **Rule Application**: Apply trading rules and filters
4. **Decision Generation**: Create final trading decision
5. **Risk Validation**: Validate decision against risk limits
6. **Execution Preparation**: Format for order management

## Development

### Running the Service

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run the service
python app/main.py
```

### Docker

```bash
# Build image
docker build -t decision-engine .

# Run container
docker run -p 8004:8004 decision-engine
```

### Testing

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Architecture

### Core Components

1. **DecisionEngine**: Main decision processing logic
2. **RuleEngine**: Trading rule management and execution
3. **SignalAggregator**: Multi-source signal combination
4. **RiskAssessor**: Risk analysis and validation
5. **ContextManager**: Market and portfolio context

### Design Patterns

- **Strategy Pattern**: Different decision strategies
- **Rule Pattern**: Configurable business rules
- **Observer Pattern**: Signal and event handling
- **Factory Pattern**: Decision and signal creation

### Vietnamese Market Adaptations

- **Trading Calendar**: Vietnamese holiday handling
- **Price Formatting**: VND currency and tick sizes
- **Regulatory Compliance**: HOSE/HNX/UPCOM rules
- **Local Indicators**: Vietnam-specific technical analysis

## Security

- JWT-based authentication
- Rate limiting and throttling
- Input validation and sanitization
- Secure configuration management
- Audit logging for all decisions

## Troubleshooting

### Common Issues

1. **High Decision Latency**: Check signal service connectivity
2. **Low Confidence Scores**: Review signal weights and quality
3. **Rule Conflicts**: Examine rule priorities and conditions
4. **Memory Usage**: Monitor decision history retention

### Debug Mode

Enable debug logging for detailed information:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

## Support

For technical support and questions:
- Check service health endpoint: `/health`
- Review service logs for errors
- Monitor Prometheus metrics: `/metrics`
- Validate configuration settings
