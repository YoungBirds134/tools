"""
Decision Engine Main Application
Vietnamese Stock Trading Decision Engine Service
Enhanced with production patterns and Vietnamese market specialization
"""

import asyncio
import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Any

import aioredis
import httpx
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from pydantic import ValidationError

from app.config import get_settings
from app.models import (
    DecisionRequest, TradingDecision, DecisionResponse,
    MultiSymbolDecisionRequest, Signal, MarketContext,
    RiskAssessment, TradingRule, DecisionMetrics,
    PortfolioContext, BacktestRequest, BacktestResult,
    RuleExecutionResult, DecisionType, SignalSource,
    ConfidenceLevel, RiskLevel, MarketCondition
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
decision_requests_total = Counter(
    'decision_requests_total',
    'Total number of decision requests',
    ['symbol', 'decision_type', 'status']
)

decision_processing_time = Histogram(
    'decision_processing_seconds',
    'Time spent processing decisions',
    ['symbol', 'strategy']
)

active_signals = Gauge(
    'active_signals_total',
    'Number of active signals',
    ['source', 'signal_type']
)

decision_confidence = Histogram(
    'decision_confidence_score',
    'Distribution of decision confidence scores',
    ['symbol', 'decision_type']
)

# Global variables
redis_client: Optional[aioredis.Redis] = None
settings = get_settings()


class DecisionEngine:
    """Core decision engine for trading decisions"""
    
    def __init__(self):
        self.signals_cache: Dict[str, List[Signal]] = {}
        self.market_context_cache: Optional[MarketContext] = None
        self.active_rules: List[TradingRule] = []
        self.decision_history: List[TradingDecision] = []
        
    async def initialize(self):
        """Initialize decision engine"""
        logger.info("Initializing Decision Engine")
        await self._load_trading_rules()
        await self._initialize_market_context()
        logger.info("Decision Engine initialized successfully")
    
    async def _load_trading_rules(self):
        """Load trading rules from configuration"""
        try:
            # Load default rules
            default_rules = [
                TradingRule(
                    rule_id="risk_limit_check",
                    rule_name="Risk Limit Check",
                    rule_type="risk",
                    conditions={"max_position_exposure": 0.05},
                    actions={"reduce_position": True},
                    priority=10,
                    created_by="system"
                ),
                TradingRule(
                    rule_id="market_hours_check",
                    rule_name="Trading Hours Check",
                    rule_type="timing",
                    conditions={"allowed_sessions": ["MORNING", "AFTERNOON"]},
                    actions={"block_trading": True},
                    priority=9,
                    created_by="system"
                ),
                TradingRule(
                    rule_id="minimum_volume_check",
                    rule_name="Minimum Volume Check",
                    rule_type="liquidity",
                    conditions={"min_avg_volume": 10000},
                    actions={"reduce_confidence": 0.2},
                    priority=7,
                    created_by="system"
                )
            ]
            
            self.active_rules = default_rules
            logger.info(f"Loaded {len(self.active_rules)} trading rules")
            
        except Exception as e:
            logger.error(f"Error loading trading rules: {e}")
            self.active_rules = []
    
    async def _initialize_market_context(self):
        """Initialize market context"""
        try:
            # Initialize with default context
            self.market_context_cache = MarketContext(
                market_condition=MarketCondition.UNKNOWN,
                market_trend="neutral",
                volatility_level=RiskLevel.MEDIUM,
                current_session="UNKNOWN"
            )
            logger.info("Market context initialized")
            
        except Exception as e:
            logger.error(f"Error initializing market context: {e}")
    
    async def process_decision(
        self,
        request: DecisionRequest,
        signals: List[Signal],
        market_context: MarketContext,
        portfolio_context: Optional[PortfolioContext] = None
    ) -> TradingDecision:
        """Process trading decision based on signals and context"""
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Apply trading rules
            rule_results = await self._apply_trading_rules(request, signals, market_context)
            
            # Aggregate signals
            aggregated_signal = await self._aggregate_signals(signals, request.symbol)
            
            # Assess risk
            risk_assessment = await self._assess_risk(request, market_context, portfolio_context)
            
            # Generate decision
            decision = await self._generate_decision(
                request, aggregated_signal, risk_assessment, market_context, rule_results
            )
            
            # Record metrics
            processing_time = asyncio.get_event_loop().time() - start_time
            decision_processing_time.labels(
                symbol=request.symbol,
                strategy=request.strategy or "default"
            ).observe(processing_time)
            
            decision_confidence.labels(
                symbol=request.symbol,
                decision_type=decision.decision_type.value
            ).observe(decision.confidence_score)
            
            decision_requests_total.labels(
                symbol=request.symbol,
                decision_type=decision.decision_type.value,
                status="success"
            ).inc()
            
            # Store decision in history
            self.decision_history.append(decision)
            
            # Cache decision in Redis
            if redis_client:
                await self._cache_decision(decision)
            
            logger.info(
                f"Generated decision for {request.symbol}: "
                f"{decision.decision_type.value} (confidence: {decision.confidence_score:.2f})"
            )
            
            return decision
            
        except Exception as e:
            logger.error(f"Error processing decision for {request.symbol}: {e}")
            decision_requests_total.labels(
                symbol=request.symbol,
                decision_type="ERROR",
                status="error"
            ).inc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Decision processing failed: {str(e)}"
            )
    
    async def _apply_trading_rules(
        self,
        request: DecisionRequest,
        signals: List[Signal],
        market_context: MarketContext
    ) -> List[RuleExecutionResult]:
        """Apply trading rules and return results"""
        
        results = []
        
        for rule in self.active_rules:
            if not rule.enabled:
                continue
            
            try:
                start_time = asyncio.get_event_loop().time()
                
                # Check rule applicability
                if not self._is_rule_applicable(rule, request.symbol, market_context):
                    continue
                
                # Execute rule
                result = await self._execute_rule(rule, request, signals, market_context)
                
                execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)
                result.execution_time_ms = execution_time
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error executing rule {rule.rule_id}: {e}")
                error_result = RuleExecutionResult(
                    rule_id=rule.rule_id,
                    symbol=request.symbol,
                    executed=False,
                    conditions_met=False,
                    errors=[str(e)]
                )
                results.append(error_result)
        
        return results
    
    def _is_rule_applicable(
        self,
        rule: TradingRule,
        symbol: str,
        market_context: MarketContext
    ) -> bool:
        """Check if rule is applicable to current context"""
        
        # Check symbol filter
        if rule.symbols and symbol not in rule.symbols:
            return False
        
        # Check session filter
        if rule.sessions and market_context.current_session not in rule.sessions:
            return False
        
        return True
    
    async def _execute_rule(
        self,
        rule: TradingRule,
        request: DecisionRequest,
        signals: List[Signal],
        market_context: MarketContext
    ) -> RuleExecutionResult:
        """Execute a trading rule"""
        
        result = RuleExecutionResult(
            rule_id=rule.rule_id,
            symbol=request.symbol,
            executed=True,
            conditions_met=False
        )
        
        try:
            # Rule-specific execution logic
            if rule.rule_type == "risk":
                await self._execute_risk_rule(rule, request, result)
            elif rule.rule_type == "timing":
                await self._execute_timing_rule(rule, market_context, result)
            elif rule.rule_type == "liquidity":
                await self._execute_liquidity_rule(rule, request, result)
            
        except Exception as e:
            result.errors.append(str(e))
            result.executed = False
        
        return result
    
    async def _execute_risk_rule(
        self,
        rule: TradingRule,
        request: DecisionRequest,
        result: RuleExecutionResult
    ):
        """Execute risk management rule"""
        
        max_exposure = rule.conditions.get("max_position_exposure", 0.05)
        current_exposure = 0.0
        
        if request.current_position and request.available_capital > 0:
            position_value = float(request.current_position * request.current_price)
            current_exposure = position_value / float(request.available_capital)
        
        if current_exposure > max_exposure:
            result.conditions_met = True
            result.actions_taken.append(f"Risk limit exceeded: {current_exposure:.2%} > {max_exposure:.2%}")
            result.decision_impact = "REDUCE_RISK"
    
    async def _execute_timing_rule(
        self,
        rule: TradingRule,
        market_context: MarketContext,
        result: RuleExecutionResult
    ):
        """Execute timing rule"""
        
        allowed_sessions = rule.conditions.get("allowed_sessions", [])
        current_session = market_context.current_session
        
        if current_session not in allowed_sessions:
            result.conditions_met = True
            result.actions_taken.append(f"Trading not allowed in {current_session}")
            result.decision_impact = "BLOCK_TRADING"
    
    async def _execute_liquidity_rule(
        self,
        rule: TradingRule,
        request: DecisionRequest,
        result: RuleExecutionResult
    ):
        """Execute liquidity rule"""
        
        min_volume = rule.conditions.get("min_avg_volume", 10000)
        
        # In a real implementation, we would fetch volume data
        # For now, we'll simulate
        avg_volume = 50000  # Simulated average volume
        
        if avg_volume < min_volume:
            result.conditions_met = True
            result.actions_taken.append(f"Low liquidity: {avg_volume} < {min_volume}")
            result.decision_impact = "REDUCE_CONFIDENCE"
    
    async def _aggregate_signals(self, signals: List[Signal], symbol: str) -> Signal:
        """Aggregate multiple signals into a single signal"""
        
        if not signals:
            # Return neutral signal
            return Signal(
                signal_id=f"neutral_{symbol}_{datetime.utcnow().isoformat()}",
                symbol=symbol,
                source=SignalSource.MANUAL,
                signal_type=DecisionType.HOLD,
                strength=0.0,
                confidence=0.0
            )
        
        # Weight signals by source and confidence
        source_weights = settings.SIGNAL_WEIGHTS
        
        total_weight = 0.0
        weighted_strength = 0.0
        weighted_confidence = 0.0
        
        buy_signals = 0
        sell_signals = 0
        hold_signals = 0
        
        for signal in signals:
            weight = source_weights.get(signal.source.value, 0.5) * signal.confidence
            total_weight += weight
            
            # Convert signal type to numeric value for aggregation
            signal_value = 0.0
            if signal.signal_type == DecisionType.BUY:
                signal_value = signal.strength
                buy_signals += 1
            elif signal.signal_type == DecisionType.SELL:
                signal_value = -signal.strength
                sell_signals += 1
            else:
                hold_signals += 1
            
            weighted_strength += signal_value * weight
            weighted_confidence += signal.confidence * weight
        
        if total_weight > 0:
            final_strength = weighted_strength / total_weight
            final_confidence = weighted_confidence / total_weight
        else:
            final_strength = 0.0
            final_confidence = 0.0
        
        # Determine aggregated signal type
        if final_strength > 0.1:
            signal_type = DecisionType.BUY
        elif final_strength < -0.1:
            signal_type = DecisionType.SELL
        else:
            signal_type = DecisionType.HOLD
        
        return Signal(
            signal_id=f"aggregated_{symbol}_{datetime.utcnow().isoformat()}",
            symbol=symbol,
            source=SignalSource.TECHNICAL_ANALYSIS,  # Most common source
            signal_type=signal_type,
            strength=abs(final_strength),
            confidence=final_confidence,
            supporting_data={
                "buy_signals": buy_signals,
                "sell_signals": sell_signals,
                "hold_signals": hold_signals,
                "total_signals": len(signals)
            }
        )
    
    async def _assess_risk(
        self,
        request: DecisionRequest,
        market_context: MarketContext,
        portfolio_context: Optional[PortfolioContext]
    ) -> RiskAssessment:
        """Assess risk for the trading decision"""
        
        # Calculate exposure
        position_value = 0.0
        if request.current_position:
            position_value = float(request.current_position * request.current_price)
        
        exposure_ratio = 0.0
        if request.available_capital > 0:
            exposure_ratio = position_value / float(request.available_capital)
        
        # Assess market risk based on volatility
        market_risk_multiplier = {
            RiskLevel.VERY_LOW: 0.5,
            RiskLevel.LOW: 0.7,
            RiskLevel.MEDIUM: 1.0,
            RiskLevel.HIGH: 1.5,
            RiskLevel.VERY_HIGH: 2.0
        }
        
        base_risk = exposure_ratio
        market_multiplier = market_risk_multiplier.get(market_context.volatility_level, 1.0)
        adjusted_risk = min(base_risk * market_multiplier, 1.0)
        
        # Determine overall risk level
        if adjusted_risk < 0.2:
            overall_risk = RiskLevel.LOW
        elif adjusted_risk < 0.4:
            overall_risk = RiskLevel.MEDIUM
        elif adjusted_risk < 0.7:
            overall_risk = RiskLevel.HIGH
        else:
            overall_risk = RiskLevel.VERY_HIGH
        
        return RiskAssessment(
            symbol=request.symbol,
            current_exposure=request.available_capital,
            max_exposure=request.available_capital,
            exposure_ratio=exposure_ratio,
            position_size_vnd=position_value,
            position_risk=adjusted_risk,
            overall_risk_level=overall_risk,
            risk_score=adjusted_risk
        )
    
    async def _generate_decision(
        self,
        request: DecisionRequest,
        signal: Signal,
        risk_assessment: RiskAssessment,
        market_context: MarketContext,
        rule_results: List[RuleExecutionResult]
    ) -> TradingDecision:
        """Generate final trading decision"""
        
        decision_id = str(uuid.uuid4())
        
        # Check for blocking rules
        blocking_rules = [r for r in rule_results if r.decision_impact == "BLOCK_TRADING"]
        if blocking_rules:
            return TradingDecision(
                decision_id=decision_id,
                symbol=request.symbol,
                decision_type=DecisionType.HOLD,
                recommended_action="HOLD - Trading blocked by rules",
                confidence_level=ConfidenceLevel.VERY_HIGH,
                confidence_score=1.0,
                risk_level=risk_assessment.overall_risk_level,
                risk_score=risk_assessment.risk_score,
                reasoning=f"Trading blocked by rules: {[r.rule_id for r in blocking_rules]}",
                market_condition=market_context.market_condition
            )
        
        # Apply risk adjustments
        risk_reducing_rules = [r for r in rule_results if r.decision_impact == "REDUCE_RISK"]
        confidence_reducing_rules = [r for r in rule_results if r.decision_impact == "REDUCE_CONFIDENCE"]
        
        adjusted_confidence = signal.confidence
        for _ in confidence_reducing_rules:
            adjusted_confidence *= 0.8  # Reduce confidence by 20%
        
        # Determine final decision type
        decision_type = signal.signal_type
        
        # Risk-based position sizing
        max_position_vnd = float(request.available_capital) * 0.05  # 5% max position
        if request.max_position_size:
            max_position_vnd = min(max_position_vnd, float(request.max_position_size))
        
        # Calculate recommended quantity
        quantity = None
        if decision_type in [DecisionType.BUY, DecisionType.SELL]:
            if decision_type == DecisionType.BUY:
                quantity = int(max_position_vnd / float(request.current_price))
                # Ensure quantity is in valid lot size
                quantity = (quantity // 100) * 100  # Round to nearest 100 shares
        
        # Set confidence level
        if adjusted_confidence >= 0.8:
            confidence_level = ConfidenceLevel.VERY_HIGH
        elif adjusted_confidence >= 0.6:
            confidence_level = ConfidenceLevel.HIGH
        elif adjusted_confidence >= 0.4:
            confidence_level = ConfidenceLevel.MEDIUM
        elif adjusted_confidence >= 0.2:
            confidence_level = ConfidenceLevel.LOW
        else:
            confidence_level = ConfidenceLevel.VERY_LOW
        
        # Generate reasoning
        reasoning_parts = [
            f"Signal: {signal.signal_type.value} (strength: {signal.strength:.2f})",
            f"Market condition: {market_context.market_condition.value}",
            f"Risk level: {risk_assessment.overall_risk_level.value}"
        ]
        
        if rule_results:
            active_rules = [r.rule_id for r in rule_results if r.conditions_met]
            if active_rules:
                reasoning_parts.append(f"Active rules: {', '.join(active_rules)}")
        
        reasoning = "; ".join(reasoning_parts)
        
        return TradingDecision(
            decision_id=decision_id,
            symbol=request.symbol,
            decision_type=decision_type,
            recommended_action=f"{decision_type.value}",
            quantity=quantity,
            price=request.current_price,
            confidence_level=confidence_level,
            confidence_score=adjusted_confidence,
            risk_level=risk_assessment.overall_risk_level,
            risk_score=risk_assessment.risk_score,
            reasoning=reasoning,
            supporting_signals=[signal.signal_id],
            market_condition=market_context.market_condition,
            market_context={
                "volatility": market_context.volatility_level.value,
                "session": market_context.current_session
            }
        )
    
    async def _cache_decision(self, decision: TradingDecision):
        """Cache decision in Redis"""
        try:
            if redis_client:
                cache_key = f"decision:{decision.symbol}:{decision.decision_id}"
                await redis_client.setex(
                    cache_key,
                    3600,  # 1 hour TTL
                    decision.json()
                )
        except Exception as e:
            logger.error(f"Error caching decision: {e}")


# Initialize decision engine
decision_engine = DecisionEngine()


# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Decision Engine service")
    
    # Initialize Redis
    global redis_client
    try:
        redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        logger.info("Connected to Redis")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis_client = None
    
    # Initialize decision engine
    await decision_engine.initialize()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Decision Engine service")
    if redis_client:
        await redis_client.close()


# Create FastAPI app
app = FastAPI(
    title="Decision Engine Service",
    description="Vietnamese Stock Trading Decision Engine",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Dependency functions
async def get_redis_client() -> Optional[aioredis.Redis]:
    """Get Redis client"""
    return redis_client


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "decision_engine",
        "version": "1.0.0"
    }
    
    # Check Redis connection
    if redis_client:
        try:
            await redis_client.ping()
            health_status["redis"] = "connected"
        except Exception:
            health_status["redis"] = "disconnected"
            health_status["status"] = "degraded"
    else:
        health_status["redis"] = "not_configured"
    
    # Check decision engine status
    health_status["decision_engine"] = {
        "active_rules": len(decision_engine.active_rules),
        "decision_history_size": len(decision_engine.decision_history)
    }
    
    return health_status


# Metrics endpoint
@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()


# Main decision endpoints
@app.post("/decisions", response_model=TradingDecision)
async def make_decision(
    request: DecisionRequest,
    background_tasks: BackgroundTasks,
    redis_client: Optional[aioredis.Redis] = Depends(get_redis_client)
):
    """Make a trading decision for a single symbol"""
    
    try:
        # Validate request
        if request.current_price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current price must be positive"
            )
        
        # Get signals (in production, this would fetch from other services)
        signals = await get_signals_for_symbol(request.symbol)
        
        # Get market context
        market_context = await get_current_market_context()
        
        # Get portfolio context if available
        portfolio_context = None
        # In production, fetch from portfolio service
        
        # Process decision
        decision = await decision_engine.process_decision(
            request, signals, market_context, portfolio_context
        )
        
        # Log decision for monitoring
        background_tasks.add_task(log_decision_metrics, decision)
        
        return decision
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {e}"
        )
    except Exception as e:
        logger.error(f"Error making decision: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Decision processing failed: {str(e)}"
        )


@app.post("/decisions/batch", response_model=DecisionResponse)
async def make_batch_decisions(
    request: MultiSymbolDecisionRequest,
    background_tasks: BackgroundTasks
):
    """Make trading decisions for multiple symbols"""
    
    try:
        start_time = asyncio.get_event_loop().time()
        
        decisions = []
        buy_count = 0
        sell_count = 0
        hold_count = 0
        total_risk = 0.0
        max_risk_decision = None
        max_risk_score = 0.0
        
        # Process each symbol
        for symbol in request.symbols:
            try:
                # Create individual decision request
                individual_request = DecisionRequest(
                    symbol=symbol,
                    current_price=1000.0,  # In production, fetch real price
                    available_capital=request.portfolio_context.available_cash,
                    market=settings.DEFAULT_MARKET,
                    strategy=request.strategy
                )
                
                # Get signals and context
                signals = await get_signals_for_symbol(symbol)
                market_context = await get_current_market_context()
                
                # Process decision
                decision = await decision_engine.process_decision(
                    individual_request, signals, market_context, request.portfolio_context
                )
                
                decisions.append(decision)
                
                # Update counters
                if decision.decision_type == DecisionType.BUY:
                    buy_count += 1
                elif decision.decision_type == DecisionType.SELL:
                    sell_count += 1
                else:
                    hold_count += 1
                
                # Track risk
                total_risk += decision.risk_score
                if decision.risk_score > max_risk_score:
                    max_risk_score = decision.risk_score
                    max_risk_decision = decision.decision_id
                    
            except Exception as e:
                logger.error(f"Error processing decision for {symbol}: {e}")
                continue
        
        processing_time = int((asyncio.get_event_loop().time() - start_time) * 1000)
        
        response = DecisionResponse(
            request_id=str(uuid.uuid4()),
            decisions=decisions,
            total_decisions=len(decisions),
            buy_decisions=buy_count,
            sell_decisions=sell_count,
            hold_decisions=hold_count,
            total_risk_exposure=total_risk,
            max_risk_decision=max_risk_decision,
            processing_time_ms=processing_time
        )
        
        # Log batch metrics
        background_tasks.add_task(log_batch_decision_metrics, response)
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing batch decisions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch decision processing failed: {str(e)}"
        )


# Signal and context endpoints
@app.get("/signals/{symbol}")
async def get_symbol_signals(symbol: str):
    """Get active signals for a symbol"""
    try:
        signals = await get_signals_for_symbol(symbol.upper())
        return {
            "symbol": symbol.upper(),
            "signals": signals,
            "count": len(signals),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting signals for {symbol}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get signals: {str(e)}"
        )


@app.get("/market-context")
async def get_market_context():
    """Get current market context"""
    try:
        context = await get_current_market_context()
        return context
    except Exception as e:
        logger.error(f"Error getting market context: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get market context: {str(e)}"
        )


# Rules management endpoints
@app.get("/rules")
async def get_trading_rules():
    """Get all trading rules"""
    return {
        "rules": decision_engine.active_rules,
        "count": len(decision_engine.active_rules)
    }


@app.post("/rules", response_model=TradingRule)
async def create_trading_rule(rule: TradingRule):
    """Create a new trading rule"""
    try:
        # Add to active rules
        decision_engine.active_rules.append(rule)
        
        logger.info(f"Created new trading rule: {rule.rule_id}")
        return rule
        
    except Exception as e:
        logger.error(f"Error creating trading rule: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create rule: {str(e)}"
        )


@app.put("/rules/{rule_id}")
async def update_trading_rule(rule_id: str, enabled: bool):
    """Enable or disable a trading rule"""
    try:
        for rule in decision_engine.active_rules:
            if rule.rule_id == rule_id:
                rule.enabled = enabled
                rule.updated_at = datetime.utcnow()
                logger.info(f"Updated rule {rule_id}: enabled={enabled}")
                return {"status": "updated", "rule_id": rule_id, "enabled": enabled}
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rule {rule_id} not found"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating trading rule {rule_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update rule: {str(e)}"
        )


# Decision history and metrics
@app.get("/decisions/history")
async def get_decision_history(
    symbol: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """Get decision history"""
    try:
        history = decision_engine.decision_history
        
        # Filter by symbol if provided
        if symbol:
            history = [d for d in history if d.symbol == symbol.upper()]
        
        # Apply pagination
        total = len(history)
        paginated_history = history[offset:offset + limit]
        
        return {
            "decisions": paginated_history,
            "total": total,
            "limit": limit,
            "offset": offset,
            "symbol_filter": symbol
        }
        
    except Exception as e:
        logger.error(f"Error getting decision history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get decision history: {str(e)}"
        )


# Helper functions
async def get_signals_for_symbol(symbol: str) -> List[Signal]:
    """Get signals for a symbol (mock implementation)"""
    # In production, this would fetch from Technical Analysis and Prediction services
    signals = [
        Signal(
            signal_id=f"ta_{symbol}_{datetime.utcnow().isoformat()}",
            symbol=symbol,
            source=SignalSource.TECHNICAL_ANALYSIS,
            signal_type=DecisionType.BUY,
            strength=0.7,
            confidence=0.8,
            reasoning="RSI oversold, MACD bullish crossover"
        ),
        Signal(
            signal_id=f"pred_{symbol}_{datetime.utcnow().isoformat()}",
            symbol=symbol,
            source=SignalSource.PREDICTION_MODEL,
            signal_type=DecisionType.BUY,
            strength=0.6,
            confidence=0.75,
            reasoning="ML model predicts 5% price increase"
        )
    ]
    
    # Update metrics
    for signal in signals:
        active_signals.labels(
            source=signal.source.value,
            signal_type=signal.signal_type.value
        ).set(1)
    
    return signals


async def get_current_market_context() -> MarketContext:
    """Get current market context (mock implementation)"""
    # In production, this would fetch from Market Data service
    current_time = datetime.now().time()
    
    # Determine trading session
    morning_start = time(9, 0)
    morning_end = time(11, 30)
    afternoon_start = time(13, 0)
    afternoon_end = time(15, 0)
    
    if morning_start <= current_time <= morning_end:
        session = "MORNING"
    elif afternoon_start <= current_time <= afternoon_end:
        session = "AFTERNOON"
    else:
        session = "CLOSED"
    
    return MarketContext(
        market_condition=MarketCondition.BULL_MARKET,
        market_trend="upward",
        volatility_level=RiskLevel.MEDIUM,
        vn_index_change=1.5,
        current_session=session,
        market_volume=1000000
    )


async def log_decision_metrics(decision: TradingDecision):
    """Log decision metrics for monitoring"""
    try:
        logger.info(
            f"Decision logged: {decision.symbol} - {decision.decision_type.value} "
            f"(confidence: {decision.confidence_score:.2f}, risk: {decision.risk_score:.2f})"
        )
    except Exception as e:
        logger.error(f"Error logging decision metrics: {e}")


async def log_batch_decision_metrics(response: DecisionResponse):
    """Log batch decision metrics"""
    try:
        logger.info(
            f"Batch decision processed: {response.total_decisions} decisions "
            f"(Buy: {response.buy_decisions}, Sell: {response.sell_decisions}, "
            f"Hold: {response.hold_decisions}) in {response.processing_time_ms}ms"
        )
    except Exception as e:
        logger.error(f"Error logging batch metrics: {e}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
