"""
Technical Analysis Models for Vietnamese Stock Market
Enhanced models for indicators, patterns, signals and backtesting
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


class TimeFrame(str, Enum):
    """Chart timeframes"""
    M1 = "1m"      # 1 minute
    M5 = "5m"      # 5 minutes
    M15 = "15m"    # 15 minutes
    M30 = "30m"    # 30 minutes
    H1 = "1h"      # 1 hour
    H4 = "4h"      # 4 hours
    D1 = "1d"      # 1 day
    W1 = "1w"      # 1 week
    MN1 = "1M"     # 1 month


class IndicatorType(str, Enum):
    """Technical indicator types"""
    TREND = "TREND"
    MOMENTUM = "MOMENTUM"
    VOLATILITY = "VOLATILITY"
    VOLUME = "VOLUME"
    SUPPORT_RESISTANCE = "SUPPORT_RESISTANCE"


class PatternType(str, Enum):
    """Candlestick pattern types"""
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    REVERSAL = "REVERSAL"
    CONTINUATION = "CONTINUATION"


class SignalType(str, Enum):
    """Trading signal types"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


class SignalStrength(str, Enum):
    """Signal strength levels"""
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"


# Base Models
class OHLCV(BaseModel):
    """OHLCV candlestick data"""
    timestamp: datetime = Field(..., description="Candle timestamp")
    open: Decimal = Field(..., ge=0, description="Opening price")
    high: Decimal = Field(..., ge=0, description="Highest price")
    low: Decimal = Field(..., ge=0, description="Lowest price")
    close: Decimal = Field(..., ge=0, description="Closing price")
    volume: int = Field(..., ge=0, description="Trading volume")
    
    @validator("high")
    def validate_high_price(cls, v, values):
        if "low" in values and v < values["low"]:
            raise ValueError("High price cannot be lower than low price")
        return v
    
    @validator("low")
    def validate_low_price(cls, v, values):
        if "high" in values and v > values["high"]:
            raise ValueError("Low price cannot be higher than high price")
        return v


class PriceData(BaseModel):
    """Extended price data with additional metrics"""
    ohlcv: OHLCV = Field(..., description="Basic OHLCV data")
    
    # Calculated fields
    typical_price: Optional[Decimal] = Field(None, description="(H+L+C)/3")
    weighted_price: Optional[Decimal] = Field(None, description="(H+L+C+C)/4")
    median_price: Optional[Decimal] = Field(None, description="(H+L)/2")
    
    # Price changes
    price_change: Optional[Decimal] = Field(None, description="Close - Previous Close")
    price_change_percent: Optional[Decimal] = Field(None, description="Price change percentage")
    
    # Gap information
    gap_up: Optional[bool] = Field(None, description="Gap up from previous candle")
    gap_down: Optional[bool] = Field(None, description="Gap down from previous candle")
    gap_size: Optional[Decimal] = Field(None, description="Gap size in price units")


# Technical Indicator Models
class MovingAverageData(BaseModel):
    """Moving average indicator data"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    sma_5: Optional[Decimal] = Field(None, description="5-period SMA")
    sma_10: Optional[Decimal] = Field(None, description="10-period SMA")
    sma_20: Optional[Decimal] = Field(None, description="20-period SMA")
    sma_50: Optional[Decimal] = Field(None, description="50-period SMA")
    sma_200: Optional[Decimal] = Field(None, description="200-period SMA")
    
    ema_12: Optional[Decimal] = Field(None, description="12-period EMA")
    ema_26: Optional[Decimal] = Field(None, description="26-period EMA")
    ema_50: Optional[Decimal] = Field(None, description="50-period EMA")
    
    # Crossover signals
    golden_cross: Optional[bool] = Field(None, description="50 SMA crosses above 200 SMA")
    death_cross: Optional[bool] = Field(None, description="50 SMA crosses below 200 SMA")


class MACDData(BaseModel):
    """MACD indicator data"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    macd_line: Decimal = Field(..., description="MACD line (EMA12 - EMA26)")
    signal_line: Decimal = Field(..., description="Signal line (EMA of MACD)")
    histogram: Decimal = Field(..., description="MACD Histogram (MACD - Signal)")
    
    # Signals
    bullish_crossover: Optional[bool] = Field(None, description="MACD crosses above signal")
    bearish_crossover: Optional[bool] = Field(None, description="MACD crosses below signal")
    divergence: Optional[str] = Field(None, description="Bullish/Bearish divergence")


class RSIData(BaseModel):
    """RSI indicator data"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    rsi: Decimal = Field(..., ge=0, le=100, description="RSI value (0-100)")
    
    # Levels
    oversold: bool = Field(default=False, description="RSI < 30 (oversold)")
    overbought: bool = Field(default=False, description="RSI > 70 (overbought)")
    
    # Divergence
    bullish_divergence: Optional[bool] = Field(None, description="Price falls, RSI rises")
    bearish_divergence: Optional[bool] = Field(None, description="Price rises, RSI falls")


class BollingerBandsData(BaseModel):
    """Bollinger Bands indicator data"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    middle_band: Decimal = Field(..., description="Middle band (SMA)")
    upper_band: Decimal = Field(..., description="Upper band (SMA + 2*StdDev)")
    lower_band: Decimal = Field(..., description="Lower band (SMA - 2*StdDev)")
    bandwidth: Decimal = Field(..., description="Band width percentage")
    
    # Signals
    squeeze: bool = Field(default=False, description="Low volatility squeeze")
    breakout_up: Optional[bool] = Field(None, description="Price breaks above upper band")
    breakout_down: Optional[bool] = Field(None, description="Price breaks below lower band")


class StochasticData(BaseModel):
    """Stochastic oscillator data"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    k_percent: Decimal = Field(..., ge=0, le=100, description="%K value")
    d_percent: Decimal = Field(..., ge=0, le=100, description="%D value")
    
    # Signals
    oversold: bool = Field(default=False, description="%K < 20")
    overbought: bool = Field(default=False, description="%K > 80")
    bullish_crossover: Optional[bool] = Field(None, description="%K crosses above %D")
    bearish_crossover: Optional[bool] = Field(None, description="%K crosses below %D")


class ADXData(BaseModel):
    """ADX (Average Directional Index) data"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    adx: Decimal = Field(..., ge=0, le=100, description="ADX value")
    plus_di: Decimal = Field(..., ge=0, description="+DI value")
    minus_di: Decimal = Field(..., ge=0, description="-DI value")
    
    # Trend strength
    strong_trend: bool = Field(default=False, description="ADX > 25")
    very_strong_trend: bool = Field(default=False, description="ADX > 50")
    
    # Direction
    bullish_trend: Optional[bool] = Field(None, description="+DI > -DI")
    bearish_trend: Optional[bool] = Field(None, description="-DI > +DI")


class VolumeIndicatorData(BaseModel):
    """Volume-based indicators"""
    timestamp: datetime = Field(..., description="Calculation timestamp")
    
    # Volume moving averages
    volume_sma_20: Optional[Decimal] = Field(None, description="20-period volume SMA")
    volume_ratio: Optional[Decimal] = Field(None, description="Current volume / Average volume")
    
    # On-Balance Volume
    obv: Optional[Decimal] = Field(None, description="On-Balance Volume")
    obv_ma: Optional[Decimal] = Field(None, description="OBV moving average")
    
    # Volume Price Trend
    vpt: Optional[Decimal] = Field(None, description="Volume Price Trend")
    
    # Signals
    high_volume: bool = Field(default=False, description="Volume > 1.5x average")
    volume_breakout: Optional[bool] = Field(None, description="Volume confirms price breakout")


# Pattern Recognition Models
class CandlestickPattern(BaseModel):
    """Candlestick pattern recognition"""
    pattern_name: str = Field(..., description="Pattern name")
    pattern_type: PatternType = Field(..., description="Pattern type")
    timestamp: datetime = Field(..., description="Pattern timestamp")
    reliability: float = Field(..., ge=0, le=1, description="Pattern reliability (0-1)")
    
    # Pattern details
    candles_count: int = Field(..., ge=1, le=5, description="Number of candles in pattern")
    strength: SignalStrength = Field(..., description="Pattern strength")
    
    # Context
    trend_context: Optional[str] = Field(None, description="Trend context when pattern formed")
    volume_confirmation: Optional[bool] = Field(None, description="Volume confirms pattern")


class SupportResistanceLevel(BaseModel):
    """Support and resistance levels"""
    level: Decimal = Field(..., ge=0, description="Price level")
    level_type: str = Field(..., description="Support or Resistance")
    strength: SignalStrength = Field(..., description="Level strength")
    touch_count: int = Field(..., ge=1, description="Number of times level was tested")
    
    # Level details
    first_touch: datetime = Field(..., description="First time level was touched")
    last_touch: datetime = Field(..., description="Most recent touch")
    broken: bool = Field(default=False, description="Level has been broken")
    
    # Distance from current price
    distance_percent: Optional[Decimal] = Field(None, description="Distance from current price (%)")


# Signal and Analysis Models
class TradingSignal(BaseModel):
    """Trading signal with detailed analysis"""
    symbol: str = Field(..., description="Stock symbol")
    timeframe: TimeFrame = Field(..., description="Signal timeframe")
    signal_type: SignalType = Field(..., description="Signal type")
    strength: SignalStrength = Field(..., description="Signal strength")
    confidence: float = Field(..., ge=0, le=1, description="Signal confidence (0-1)")
    
    # Signal details
    entry_price: Optional[Decimal] = Field(None, description="Suggested entry price")
    stop_loss: Optional[Decimal] = Field(None, description="Stop loss price")
    take_profit: Optional[Decimal] = Field(None, description="Take profit price")
    risk_reward_ratio: Optional[Decimal] = Field(None, description="Risk/reward ratio")
    
    # Supporting indicators
    supporting_indicators: List[str] = Field(default_factory=list, description="Supporting indicators")
    conflicting_indicators: List[str] = Field(default_factory=list, description="Conflicting indicators")
    
    # Timestamps
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Signal generation time")
    expires_at: Optional[datetime] = Field(None, description="Signal expiration time")


class TechnicalAnalysisResult(BaseModel):
    """Comprehensive technical analysis result"""
    symbol: str = Field(..., description="Stock symbol")
    timeframe: TimeFrame = Field(..., description="Analysis timeframe")
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    
    # Current price info
    current_price: Decimal = Field(..., description="Current price")
    previous_close: Decimal = Field(..., description="Previous close")
    price_change: Decimal = Field(..., description="Price change")
    price_change_percent: Decimal = Field(..., description="Price change percentage")
    
    # Technical indicators
    moving_averages: Optional[MovingAverageData] = Field(None, description="Moving averages")
    macd: Optional[MACDData] = Field(None, description="MACD data")
    rsi: Optional[RSIData] = Field(None, description="RSI data")
    bollinger_bands: Optional[BollingerBandsData] = Field(None, description="Bollinger Bands")
    stochastic: Optional[StochasticData] = Field(None, description="Stochastic oscillator")
    adx: Optional[ADXData] = Field(None, description="ADX data")
    volume_indicators: Optional[VolumeIndicatorData] = Field(None, description="Volume indicators")
    
    # Pattern analysis
    candlestick_patterns: List[CandlestickPattern] = Field(default_factory=list, description="Detected patterns")
    support_resistance: List[SupportResistanceLevel] = Field(default_factory=list, description="S/R levels")
    
    # Overall analysis
    overall_signal: SignalType = Field(..., description="Overall trading signal")
    trend_direction: str = Field(..., description="Overall trend direction")
    trend_strength: SignalStrength = Field(..., description="Trend strength")
    
    # Summary scores
    bullish_score: float = Field(..., ge=0, le=100, description="Bullish sentiment score")
    bearish_score: float = Field(..., ge=0, le=100, description="Bearish sentiment score")
    volatility_score: float = Field(..., ge=0, le=100, description="Volatility score")


# Request Models
class TechnicalAnalysisRequest(BaseModel):
    """Request for technical analysis"""
    symbol: str = Field(..., description="Stock symbol")
    timeframe: TimeFrame = Field(default=TimeFrame.D1, description="Analysis timeframe")
    indicators: List[str] = Field(default_factory=list, description="Specific indicators to calculate")
    include_patterns: bool = Field(default=True, description="Include pattern recognition")
    include_signals: bool = Field(default=True, description="Include trading signals")
    lookback_periods: int = Field(default=100, ge=20, le=1000, description="Historical periods to analyze")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class IndicatorRequest(BaseModel):
    """Request for specific indicator calculation"""
    symbol: str = Field(..., description="Stock symbol")
    timeframe: TimeFrame = Field(default=TimeFrame.D1, description="Timeframe")
    indicator_type: str = Field(..., description="Indicator type (SMA, EMA, RSI, etc.)")
    period: int = Field(default=14, ge=1, le=200, description="Indicator period")
    additional_params: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class BacktestRequest(BaseModel):
    """Request for strategy backtesting"""
    symbol: str = Field(..., description="Stock symbol")
    timeframe: TimeFrame = Field(default=TimeFrame.D1, description="Backtest timeframe")
    start_date: date = Field(..., description="Backtest start date")
    end_date: date = Field(..., description="Backtest end date")
    initial_capital: Decimal = Field(default=1000000, ge=1000, description="Initial capital in VND")
    strategy_rules: Dict[str, Any] = Field(..., description="Strategy rules and parameters")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()
    
    @validator("end_date")
    def validate_date_range(cls, v, values):
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


class BacktestResult(BaseModel):
    """Backtesting result"""
    symbol: str = Field(..., description="Tested symbol")
    timeframe: TimeFrame = Field(..., description="Tested timeframe")
    start_date: date = Field(..., description="Backtest start date")
    end_date: date = Field(..., description="Backtest end date")
    
    # Performance metrics
    initial_capital: Decimal = Field(..., description="Initial capital")
    final_capital: Decimal = Field(..., description="Final capital")
    total_return: Decimal = Field(..., description="Total return in VND")
    total_return_percent: Decimal = Field(..., description="Total return percentage")
    
    # Trade statistics
    total_trades: int = Field(..., description="Total number of trades")
    winning_trades: int = Field(..., description="Number of winning trades")
    losing_trades: int = Field(..., description="Number of losing trades")
    win_rate: Decimal = Field(..., description="Win rate percentage")
    
    # Risk metrics
    max_drawdown: Decimal = Field(..., description="Maximum drawdown percentage")
    sharpe_ratio: Optional[Decimal] = Field(None, description="Sharpe ratio")
    sortino_ratio: Optional[Decimal] = Field(None, description="Sortino ratio")
    
    # Additional metrics
    avg_win: Decimal = Field(..., description="Average winning trade")
    avg_loss: Decimal = Field(..., description="Average losing trade")
    largest_win: Decimal = Field(..., description="Largest winning trade")
    largest_loss: Decimal = Field(..., description="Largest losing trade")
    
    # Trade details
    trades: List[Dict[str, Any]] = Field(default_factory=list, description="Individual trade details")


# Chart Models
class ChartRequest(BaseModel):
    """Request for chart generation"""
    symbol: str = Field(..., description="Stock symbol")
    timeframe: TimeFrame = Field(default=TimeFrame.D1, description="Chart timeframe")
    periods: int = Field(default=100, ge=20, le=500, description="Number of periods to chart")
    indicators: List[str] = Field(default_factory=list, description="Indicators to include")
    chart_type: str = Field(default="candlestick", description="Chart type")
    
    # Chart styling
    width: int = Field(default=800, ge=400, le=2000, description="Chart width")
    height: int = Field(default=600, ge=300, le=1500, description="Chart height")
    
    @validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()


class ChartData(BaseModel):
    """Chart data response"""
    symbol: str = Field(..., description="Chart symbol")
    timeframe: TimeFrame = Field(..., description="Chart timeframe")
    chart_url: Optional[str] = Field(None, description="Chart image URL")
    chart_data: Dict[str, Any] = Field(..., description="Chart data for client rendering")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Chart generation time")
