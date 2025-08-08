"""
Decision Engine Models for Vietnamese Stock Trading
Enhanced models for trading decisions, signals, and rule management
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, time
from decimal import Decimal
from enum import Enum


class DecisionType(str, Enum):
    """Types of trading decisions"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    CLOSE_POSITION = "CLOSE_POSITION"
    REDUCE_POSITION = "REDUCE_POSITION"
    INCREASE_POSITION = "INCREASE_POSITION"


class SignalSource(str, Enum):
    """Sources of trading signals"""
    TECHNICAL_ANALYSIS = "TECHNICAL_ANALYSIS"
    PREDICTION_MODEL = "PREDICTION_MODEL"
    MARKET_SENTIMENT = "MARKET_SENTIMENT"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    NEWS_ANALYSIS = "NEWS_ANALYSIS"
    MANUAL = "MANUAL"


class ConfidenceLevel(str, Enum):
    """Confidence levels for decisions"""
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class RiskLevel(str, Enum):
    """Risk levels"""
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class MarketCondition(str, Enum):
    """Market condition types"""
    BULL_MARKET = "BULL_MARKET"
    BEAR_MARKET = "BEAR_MARKET"
    SIDEWAYS = "SIDEWAYS"
    VOLATILE = "VOLATILE"
    UNKNOWN = "UNKNOWN"


class MarketEnum(str, Enum):
    """Vietnamese stock exchanges"""
    HOSE = "HOSE"
    HNX = "HNX"
    UPCOM = "UPCOM"


# Base Models
class Signal(BaseModel):
    """Trading signal from various sources"""
    signal_id: str = Field(..., description="Unique signal identifier")
    symbol: str = Field(..., description="Stock symbol")
    source: SignalSource = Field(..., description="Signal source")
    signal_type: DecisionType = Field(..., description="Signal type")
    strength: float = Field(..., ge=0, le=1, description="Signal strength (0-1)")
    confidence: float = Field(..., ge=0, le=1, description="Signal confidence (0-1)")
    
    # Signal details
    entry_price: Optional[Decimal] = Field(None, description="Suggested entry price")
    target_price: Optional[Decimal] = Field(None, description="Target price")
    stop_loss: Optional[Decimal] = Field(None, description="Stop loss price")
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Signal generation time")
    expires_at: Optional[datetime] = Field(None, description="Signal expiration time")
    
    # Additional context
    reasoning: Optional[str] = Field(None, description="Signal reasoning")
    supporting_data: Dict[str, Any] = Field(default_factory=dict, description="Supporting data")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class MarketContext(BaseModel):
    """Current market context for decision making"""
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Context timestamp")
    
    # Market state
    market_condition: MarketCondition = Field(..., description="Overall market condition")
    market_trend: str = Field(..., description="Current market trend")
    volatility_level: RiskLevel = Field(..., description="Market volatility level")
    
    # Indices data
    vn_index_change: Optional[Decimal] = Field(None, description="VN-Index change %")
    hnx_index_change: Optional[Decimal] = Field(None, description="HNX-Index change %")
    
    # Market breadth
    advancing_stocks: Optional[int] = Field(None, description="Number of advancing stocks")
    declining_stocks: Optional[int] = Field(None, description="Number of declining stocks")
    
    # Volume and activity
    market_volume: Optional[int] = Field(None, description="Total market volume")
    volume_ratio: Optional[Decimal] = Field(None, description="Volume vs average ratio")
    
    # Foreign activity
    foreign_net_buy: Optional[Decimal] = Field(None, description="Foreign net buy in VND")
    foreign_net_sell: Optional[Decimal] = Field(None, description="Foreign net sell in VND")
    
    # Sector performance
    sector_performance: Dict[str, Decimal] = Field(default_factory=dict, description="Sector performance data")
    
    # Trading session info
    current_session: str = Field(..., description="Current trading session")
    session_remaining_time: Optional[int] = Field(None, description="Remaining session time in minutes")


class RiskAssessment(BaseModel):
    """Risk assessment for trading decisions"""
    symbol: str = Field(..., description="Stock symbol")
    assessment_time: datetime = Field(default_factory=datetime.utcnow, description="Assessment time")
    
    # Portfolio risk
    current_exposure: Decimal = Field(..., description="Current exposure amount")
    max_exposure: Decimal = Field(..., description="Maximum allowed exposure")
    exposure_ratio: float = Field(..., ge=0, le=1, description="Exposure ratio")
    
    # Position risk
    position_size_vnd: Decimal = Field(..., description="Position size in VND")
    position_risk: float = Field(..., ge=0, le=1, description="Position risk level")
    
    # Market risk
    beta: Optional[Decimal] = Field(None, description="Stock beta")
    correlation_with_market: Optional[Decimal] = Field(None, description="Correlation with VN-Index")
    
    # Liquidity risk
    average_volume: Optional[int] = Field(None, description="Average daily volume")
    liquidity_score: Optional[float] = Field(None, ge=0, le=1, description="Liquidity score")
    
    # Sector risk
    sector: Optional[str] = Field(None, description="Stock sector")
    sector_exposure: Optional[Decimal] = Field(None, description="Current sector exposure")
    sector_risk_level: Optional[RiskLevel] = Field(None, description="Sector risk level")
    
    # Risk metrics
    var_1d: Optional[Decimal] = Field(None, description="1-day Value at Risk")
    expected_shortfall: Optional[Decimal] = Field(None, description="Expected shortfall")
    
    # Overall assessment
    overall_risk_level: RiskLevel = Field(..., description="Overall risk level")
    risk_score: float = Field(..., ge=0, le=1, description="Risk score (0=low, 1=high)")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class TradingRule(BaseModel):
    """Trading rule definition"""
    rule_id: str = Field(..., description="Unique rule identifier")
    rule_name: str = Field(..., description="Rule name")
    rule_type: str = Field(..., description="Rule type (entry, exit, risk)")
    
    # Rule conditions
    conditions: Dict[str, Any] = Field(..., description="Rule conditions")
    actions: Dict[str, Any] = Field(..., description="Rule actions")
    
    # Rule parameters
    priority: int = Field(default=1, ge=1, le=10, description="Rule priority")
    enabled: bool = Field(default=True, description="Rule enabled status")
    
    # Applicability
    symbols: Optional[List[str]] = Field(None, description="Applicable symbols (None = all)")
    markets: Optional[List[MarketEnum]] = Field(None, description="Applicable markets")
    sessions: Optional[List[str]] = Field(None, description="Applicable sessions")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Rule creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Rule update time")
    created_by: str = Field(..., description="Rule creator")
    
    # Performance tracking
    usage_count: int = Field(default=0, description="Rule usage count")
    success_rate: Optional[float] = Field(None, ge=0, le=1, description="Rule success rate")


class DecisionRequest(BaseModel):
    """Request for trading decision"""
    symbol: str = Field(..., description="Stock symbol")
    current_price: Decimal = Field(..., ge=0, description="Current stock price")
    
    # Portfolio context
    current_position: Optional[int] = Field(None, description="Current position size")
    available_capital: Decimal = Field(..., ge=0, description="Available capital")
    
    # Market context
    market: MarketEnum = Field(..., description="Stock exchange")
    
    # Decision parameters
    strategy: Optional[str] = Field(None, description="Trading strategy to use")
    max_position_size: Optional[Decimal] = Field(None, description="Maximum position size")
    risk_tolerance: Optional[RiskLevel] = Field(None, description="Risk tolerance level")
    
    # Time constraints
    decision_deadline: Optional[datetime] = Field(None, description="Decision deadline")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class TradingDecision(BaseModel):
    """Trading decision output"""
    decision_id: str = Field(..., description="Unique decision identifier")
    symbol: str = Field(..., description="Stock symbol")
    decision_type: DecisionType = Field(..., description="Decision type")
    
    # Decision details
    recommended_action: str = Field(..., description="Recommended action")
    quantity: Optional[int] = Field(None, description="Recommended quantity")
    price: Optional[Decimal] = Field(None, description="Recommended price")
    
    # Risk management
    stop_loss: Optional[Decimal] = Field(None, description="Stop loss price")
    take_profit: Optional[Decimal] = Field(None, description="Take profit price")
    position_size_vnd: Optional[Decimal] = Field(None, description="Position size in VND")
    
    # Confidence and risk
    confidence_level: ConfidenceLevel = Field(..., description="Decision confidence")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score")
    risk_level: RiskLevel = Field(..., description="Decision risk level")
    risk_score: float = Field(..., ge=0, le=1, description="Risk score")
    
    # Supporting information
    reasoning: str = Field(..., description="Decision reasoning")
    supporting_signals: List[str] = Field(default_factory=list, description="Supporting signal IDs")
    conflicting_signals: List[str] = Field(default_factory=list, description="Conflicting signal IDs")
    
    # Market context
    market_condition: MarketCondition = Field(..., description="Market condition at decision time")
    market_context: Dict[str, Any] = Field(default_factory=dict, description="Market context data")
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Decision creation time")
    valid_until: Optional[datetime] = Field(None, description="Decision validity end time")
    
    # Execution tracking
    executed: bool = Field(default=False, description="Decision executed status")
    execution_time: Optional[datetime] = Field(None, description="Execution time")
    execution_price: Optional[Decimal] = Field(None, description="Actual execution price")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class DecisionMetrics(BaseModel):
    """Metrics for decision performance tracking"""
    decision_id: str = Field(..., description="Decision identifier")
    symbol: str = Field(..., description="Stock symbol")
    
    # Performance metrics
    success: Optional[bool] = Field(None, description="Decision success status")
    profit_loss: Optional[Decimal] = Field(None, description="Profit/loss in VND")
    profit_loss_percent: Optional[Decimal] = Field(None, description="Profit/loss percentage")
    
    # Timing metrics
    decision_time: datetime = Field(..., description="Decision creation time")
    execution_time: Optional[datetime] = Field(None, description="Execution time")
    close_time: Optional[datetime] = Field(None, description="Position close time")
    holding_period: Optional[int] = Field(None, description="Holding period in minutes")
    
    # Risk metrics
    max_drawdown: Optional[Decimal] = Field(None, description="Maximum drawdown")
    risk_adjusted_return: Optional[Decimal] = Field(None, description="Risk-adjusted return")
    
    # Market context
    market_condition_at_entry: MarketCondition = Field(..., description="Market condition at entry")
    market_condition_at_exit: Optional[MarketCondition] = Field(None, description="Market condition at exit")


class PortfolioContext(BaseModel):
    """Current portfolio context for decision making"""
    portfolio_id: str = Field(..., description="Portfolio identifier")
    
    # Portfolio metrics
    total_value: Decimal = Field(..., description="Total portfolio value")
    available_cash: Decimal = Field(..., description="Available cash")
    invested_value: Decimal = Field(..., description="Invested value")
    
    # Risk metrics
    portfolio_beta: Optional[Decimal] = Field(None, description="Portfolio beta")
    portfolio_var: Optional[Decimal] = Field(None, description="Portfolio VaR")
    
    # Diversification
    number_of_positions: int = Field(..., description="Number of open positions")
    sector_exposure: Dict[str, Decimal] = Field(default_factory=dict, description="Sector exposure")
    market_exposure: Dict[str, Decimal] = Field(default_factory=dict, description="Market exposure")
    
    # Performance
    daily_pnl: Optional[Decimal] = Field(None, description="Daily P&L")
    total_return: Optional[Decimal] = Field(None, description="Total return")
    
    # Constraints
    max_position_size: Decimal = Field(..., description="Maximum position size")
    max_sector_exposure: Decimal = Field(..., description="Maximum sector exposure")
    max_daily_trades: int = Field(..., description="Maximum daily trades")
    
    # Activity
    trades_today: int = Field(default=0, description="Trades executed today")
    last_trade_time: Optional[datetime] = Field(None, description="Last trade timestamp")


# Request/Response Models
class MultiSymbolDecisionRequest(BaseModel):
    """Request for decisions on multiple symbols"""
    symbols: List[str] = Field(..., min_items=1, max_items=50, description="List of symbols")
    portfolio_context: PortfolioContext = Field(..., description="Portfolio context")
    strategy: Optional[str] = Field(None, description="Trading strategy")
    
    @validator("symbols")
    def validate_symbols(cls, v):
        return [symbol.upper() for symbol in v]


class DecisionResponse(BaseModel):
    """Response containing trading decisions"""
    request_id: str = Field(..., description="Request identifier")
    decisions: List[TradingDecision] = Field(..., description="Trading decisions")
    
    # Summary
    total_decisions: int = Field(..., description="Total number of decisions")
    buy_decisions: int = Field(..., description="Number of buy decisions")
    sell_decisions: int = Field(..., description="Number of sell decisions")
    hold_decisions: int = Field(..., description="Number of hold decisions")
    
    # Risk summary
    total_risk_exposure: Decimal = Field(..., description="Total risk exposure")
    max_risk_decision: Optional[str] = Field(None, description="Highest risk decision ID")
    
    # Timing
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Response creation time")


class RuleExecutionResult(BaseModel):
    """Result of rule execution"""
    rule_id: str = Field(..., description="Rule identifier")
    symbol: str = Field(..., description="Symbol processed")
    
    # Execution details
    executed: bool = Field(..., description="Rule executed successfully")
    conditions_met: bool = Field(..., description="Rule conditions satisfied")
    actions_taken: List[str] = Field(default_factory=list, description="Actions taken")
    
    # Performance
    execution_time_ms: int = Field(..., description="Execution time in milliseconds")
    
    # Output
    decision_impact: Optional[str] = Field(None, description="Impact on decision")
    generated_signals: List[str] = Field(default_factory=list, description="Generated signal IDs")
    
    # Errors
    errors: List[str] = Field(default_factory=list, description="Execution errors")
    warnings: List[str] = Field(default_factory=list, description="Execution warnings")


class BacktestRequest(BaseModel):
    """Request for strategy backtesting"""
    strategy_name: str = Field(..., description="Strategy name")
    symbols: List[str] = Field(..., description="Symbols to test")
    start_date: datetime = Field(..., description="Backtest start date")
    end_date: datetime = Field(..., description="Backtest end date")
    initial_capital: Decimal = Field(..., description="Initial capital")
    
    # Strategy parameters
    strategy_params: Dict[str, Any] = Field(default_factory=dict, description="Strategy parameters")
    
    @validator("symbols")
    def validate_symbols(cls, v):
        return [symbol.upper() for symbol in v]


class BacktestResult(BaseModel):
    """Backtesting results"""
    strategy_name: str = Field(..., description="Strategy name")
    
    # Performance metrics
    total_return: Decimal = Field(..., description="Total return")
    annualized_return: Decimal = Field(..., description="Annualized return")
    sharpe_ratio: Optional[Decimal] = Field(None, description="Sharpe ratio")
    max_drawdown: Decimal = Field(..., description="Maximum drawdown")
    
    # Trade statistics
    total_trades: int = Field(..., description="Total number of trades")
    winning_trades: int = Field(..., description="Number of winning trades")
    losing_trades: int = Field(..., description="Number of losing trades")
    win_rate: Decimal = Field(..., description="Win rate percentage")
    
    # Risk metrics
    volatility: Decimal = Field(..., description="Strategy volatility")
    var_95: Optional[Decimal] = Field(None, description="95% Value at Risk")
    
    # Detailed results
    trades: List[Dict[str, Any]] = Field(default_factory=list, description="Individual trades")
    equity_curve: List[Dict[str, Any]] = Field(default_factory=list, description="Equity curve data")
    
    # Summary
    backtest_period: str = Field(..., description="Backtest period")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Result generation time")
