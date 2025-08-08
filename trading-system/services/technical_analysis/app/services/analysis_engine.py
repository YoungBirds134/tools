"""
Technical Analysis Engine
Core engine for calculating technical indicators, pattern recognition, and signal generation
"""

import numpy as np
import pandas as pd
import talib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import asyncio
import structlog

from ..models import (
    OHLCV, PriceData, MovingAverageData, MACDData, RSIData, 
    BollingerBandsData, StochasticData, ADXData, VolumeIndicatorData,
    CandlestickPattern, SupportResistanceLevel, TradingSignal,
    TechnicalAnalysisResult, TimeFrame, SignalType, SignalStrength, PatternType
)
from ..config import settings

logger = structlog.get_logger(__name__)


class TechnicalAnalysisEngine:
    """Core technical analysis engine with Vietnamese market optimizations"""
    
    def __init__(self):
        self.indicators_cache = {}
        self.patterns_cache = {}
        self.last_calculation_time = {}
        
        logger.info("Technical Analysis Engine initialized",
                   default_periods=settings.default_periods)
    
    # Data Preparation Methods
    
    def prepare_dataframe(self, ohlcv_data: List[OHLCV]) -> pd.DataFrame:
        """Convert OHLCV data to pandas DataFrame for analysis"""
        if not ohlcv_data:
            raise ValueError("No OHLCV data provided")
        
        data = []
        for candle in ohlcv_data:
            data.append({
                'timestamp': candle.timestamp,
                'open': float(candle.open),
                'high': float(candle.high),
                'low': float(candle.low),
                'close': float(candle.close),
                'volume': float(candle.volume)
            })
        
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        # Add basic calculated columns
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['weighted_price'] = (df['high'] + df['low'] + df['close'] + df['close']) / 4
        df['median_price'] = (df['high'] + df['low']) / 2
        
        # Price changes
        df['price_change'] = df['close'].diff()
        df['price_change_pct'] = df['close'].pct_change() * 100
        
        return df
    
    def validate_data_sufficiency(self, df: pd.DataFrame, required_periods: int = None) -> bool:
        """Validate if we have enough data for calculations"""
        if df.empty:
            return False
        
        min_required = required_periods or settings.min_data_points
        return len(df) >= min_required
    
    # Moving Averages
    
    def calculate_moving_averages(self, df: pd.DataFrame) -> MovingAverageData:
        """Calculate various moving averages"""
        if not self.validate_data_sufficiency(df, 200):
            logger.warning("Insufficient data for moving averages calculation")
            return None
        
        try:
            close_prices = df['close'].values
            
            # Simple Moving Averages
            sma_5 = talib.SMA(close_prices, timeperiod=5)
            sma_10 = talib.SMA(close_prices, timeperiod=10)
            sma_20 = talib.SMA(close_prices, timeperiod=20)
            sma_50 = talib.SMA(close_prices, timeperiod=50)
            sma_200 = talib.SMA(close_prices, timeperiod=200)
            
            # Exponential Moving Averages
            ema_12 = talib.EMA(close_prices, timeperiod=12)
            ema_26 = talib.EMA(close_prices, timeperiod=26)
            ema_50 = talib.EMA(close_prices, timeperiod=50)
            
            # Get latest values
            latest_index = -1
            
            # Detect crossovers
            golden_cross = False
            death_cross = False
            
            if len(sma_50) > 1 and len(sma_200) > 1:
                # Golden Cross: SMA50 crosses above SMA200
                if (sma_50[-1] > sma_200[-1] and sma_50[-2] <= sma_200[-2]):
                    golden_cross = True
                # Death Cross: SMA50 crosses below SMA200
                elif (sma_50[-1] < sma_200[-1] and sma_50[-2] >= sma_200[-2]):
                    death_cross = True
            
            return MovingAverageData(
                timestamp=df.index[latest_index],
                sma_5=Decimal(str(round(sma_5[latest_index], 2))) if not np.isnan(sma_5[latest_index]) else None,
                sma_10=Decimal(str(round(sma_10[latest_index], 2))) if not np.isnan(sma_10[latest_index]) else None,
                sma_20=Decimal(str(round(sma_20[latest_index], 2))) if not np.isnan(sma_20[latest_index]) else None,
                sma_50=Decimal(str(round(sma_50[latest_index], 2))) if not np.isnan(sma_50[latest_index]) else None,
                sma_200=Decimal(str(round(sma_200[latest_index], 2))) if not np.isnan(sma_200[latest_index]) else None,
                ema_12=Decimal(str(round(ema_12[latest_index], 2))) if not np.isnan(ema_12[latest_index]) else None,
                ema_26=Decimal(str(round(ema_26[latest_index], 2))) if not np.isnan(ema_26[latest_index]) else None,
                ema_50=Decimal(str(round(ema_50[latest_index], 2))) if not np.isnan(ema_50[latest_index]) else None,
                golden_cross=golden_cross,
                death_cross=death_cross
            )
            
        except Exception as e:
            logger.error("Error calculating moving averages", error=str(e))
            return None
    
    # MACD
    
    def calculate_macd(self, df: pd.DataFrame) -> MACDData:
        """Calculate MACD indicator"""
        if not self.validate_data_sufficiency(df, 35):
            return None
        
        try:
            close_prices = df['close'].values
            
            # Calculate MACD
            macd_line, signal_line, histogram = talib.MACD(
                close_prices,
                fastperiod=settings.default_periods['macd_fast'],
                slowperiod=settings.default_periods['macd_slow'],
                signalperiod=settings.default_periods['macd_signal']
            )
            
            latest_index = -1
            
            # Detect crossovers
            bullish_crossover = False
            bearish_crossover = False
            
            if len(macd_line) > 1:
                if (macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]):
                    bullish_crossover = True
                elif (macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]):
                    bearish_crossover = True
            
            return MACDData(
                timestamp=df.index[latest_index],
                macd_line=Decimal(str(round(macd_line[latest_index], 4))),
                signal_line=Decimal(str(round(signal_line[latest_index], 4))),
                histogram=Decimal(str(round(histogram[latest_index], 4))),
                bullish_crossover=bullish_crossover,
                bearish_crossover=bearish_crossover
            )
            
        except Exception as e:
            logger.error("Error calculating MACD", error=str(e))
            return None
    
    # RSI
    
    def calculate_rsi(self, df: pd.DataFrame) -> RSIData:
        """Calculate RSI indicator"""
        if not self.validate_data_sufficiency(df, 20):
            return None
        
        try:
            close_prices = df['close'].values
            
            rsi_values = talib.RSI(close_prices, timeperiod=settings.default_periods['rsi'])
            
            latest_index = -1
            current_rsi = rsi_values[latest_index]
            
            # Detect divergences (simplified logic)
            bullish_divergence = self._detect_rsi_bullish_divergence(df, rsi_values)
            bearish_divergence = self._detect_rsi_bearish_divergence(df, rsi_values)
            
            return RSIData(
                timestamp=df.index[latest_index],
                rsi=Decimal(str(round(current_rsi, 2))),
                oversold=current_rsi < 30,
                overbought=current_rsi > 70,
                bullish_divergence=bullish_divergence,
                bearish_divergence=bearish_divergence
            )
            
        except Exception as e:
            logger.error("Error calculating RSI", error=str(e))
            return None
    
    # Bollinger Bands
    
    def calculate_bollinger_bands(self, df: pd.DataFrame) -> BollingerBandsData:
        """Calculate Bollinger Bands"""
        if not self.validate_data_sufficiency(df, 25):
            return None
        
        try:
            close_prices = df['close'].values
            
            upper_band, middle_band, lower_band = talib.BBANDS(
                close_prices,
                timeperiod=settings.default_periods['bb_period'],
                nbdevup=2,
                nbdevdn=2,
                matype=0
            )
            
            latest_index = -1
            current_price = close_prices[latest_index]
            
            # Calculate bandwidth
            bandwidth = ((upper_band[latest_index] - lower_band[latest_index]) / middle_band[latest_index]) * 100
            
            # Detect squeeze (low volatility)
            squeeze = bandwidth < 10  # Adjust threshold as needed
            
            # Detect breakouts
            breakout_up = current_price > upper_band[latest_index]
            breakout_down = current_price < lower_band[latest_index]
            
            return BollingerBandsData(
                timestamp=df.index[latest_index],
                middle_band=Decimal(str(round(middle_band[latest_index], 2))),
                upper_band=Decimal(str(round(upper_band[latest_index], 2))),
                lower_band=Decimal(str(round(lower_band[latest_index], 2))),
                bandwidth=Decimal(str(round(bandwidth, 2))),
                squeeze=squeeze,
                breakout_up=breakout_up,
                breakout_down=breakout_down
            )
            
        except Exception as e:
            logger.error("Error calculating Bollinger Bands", error=str(e))
            return None
    
    # Stochastic
    
    def calculate_stochastic(self, df: pd.DataFrame) -> StochasticData:
        """Calculate Stochastic oscillator"""
        if not self.validate_data_sufficiency(df, 20):
            return None
        
        try:
            high_prices = df['high'].values
            low_prices = df['low'].values
            close_prices = df['close'].values
            
            k_percent, d_percent = talib.STOCH(
                high_prices, low_prices, close_prices,
                fastk_period=settings.default_periods['stochastic'],
                slowk_period=3,
                slowd_period=3
            )
            
            latest_index = -1
            current_k = k_percent[latest_index]
            current_d = d_percent[latest_index]
            
            # Detect crossovers
            bullish_crossover = False
            bearish_crossover = False
            
            if len(k_percent) > 1:
                if (current_k > current_d and k_percent[-2] <= d_percent[-2]):
                    bullish_crossover = True
                elif (current_k < current_d and k_percent[-2] >= d_percent[-2]):
                    bearish_crossover = True
            
            return StochasticData(
                timestamp=df.index[latest_index],
                k_percent=Decimal(str(round(current_k, 2))),
                d_percent=Decimal(str(round(current_d, 2))),
                oversold=current_k < 20,
                overbought=current_k > 80,
                bullish_crossover=bullish_crossover,
                bearish_crossover=bearish_crossover
            )
            
        except Exception as e:
            logger.error("Error calculating Stochastic", error=str(e))
            return None
    
    # ADX
    
    def calculate_adx(self, df: pd.DataFrame) -> ADXData:
        """Calculate ADX (Average Directional Index)"""
        if not self.validate_data_sufficiency(df, 25):
            return None
        
        try:
            high_prices = df['high'].values
            low_prices = df['low'].values
            close_prices = df['close'].values
            
            adx_values = talib.ADX(high_prices, low_prices, close_prices, timeperiod=settings.default_periods['adx'])
            plus_di = talib.PLUS_DI(high_prices, low_prices, close_prices, timeperiod=settings.default_periods['adx'])
            minus_di = talib.MINUS_DI(high_prices, low_prices, close_prices, timeperiod=settings.default_periods['adx'])
            
            latest_index = -1
            current_adx = adx_values[latest_index]
            current_plus_di = plus_di[latest_index]
            current_minus_di = minus_di[latest_index]
            
            return ADXData(
                timestamp=df.index[latest_index],
                adx=Decimal(str(round(current_adx, 2))),
                plus_di=Decimal(str(round(current_plus_di, 2))),
                minus_di=Decimal(str(round(current_minus_di, 2))),
                strong_trend=current_adx > 25,
                very_strong_trend=current_adx > 50,
                bullish_trend=current_plus_di > current_minus_di,
                bearish_trend=current_minus_di > current_plus_di
            )
            
        except Exception as e:
            logger.error("Error calculating ADX", error=str(e))
            return None
    
    # Volume Indicators
    
    def calculate_volume_indicators(self, df: pd.DataFrame) -> VolumeIndicatorData:
        """Calculate volume-based indicators"""
        if not self.validate_data_sufficiency(df, 25):
            return None
        
        try:
            close_prices = df['close'].values
            volume = df['volume'].values
            
            # Volume SMA
            volume_sma_20 = talib.SMA(volume, timeperiod=20)
            current_volume_ratio = volume[-1] / volume_sma_20[-1] if volume_sma_20[-1] > 0 else 1
            
            # On-Balance Volume
            obv = talib.OBV(close_prices, volume)
            obv_ma = talib.SMA(obv, timeperiod=20)
            
            # Volume Price Trend (simplified)
            vpt = self._calculate_vpt(df)
            
            latest_index = -1
            
            return VolumeIndicatorData(
                timestamp=df.index[latest_index],
                volume_sma_20=Decimal(str(round(volume_sma_20[latest_index], 0))),
                volume_ratio=Decimal(str(round(current_volume_ratio, 2))),
                obv=Decimal(str(round(obv[latest_index], 0))),
                obv_ma=Decimal(str(round(obv_ma[latest_index], 0))),
                vpt=Decimal(str(round(vpt[latest_index], 0))),
                high_volume=current_volume_ratio > 1.5,
                volume_breakout=None  # Would need price breakout confirmation
            )
            
        except Exception as e:
            logger.error("Error calculating volume indicators", error=str(e))
            return None
    
    # Pattern Recognition
    
    def detect_candlestick_patterns(self, df: pd.DataFrame) -> List[CandlestickPattern]:
        """Detect candlestick patterns using TA-Lib"""
        if not self.validate_data_sufficiency(df, 10):
            return []
        
        patterns = []
        
        try:
            open_prices = df['open'].values
            high_prices = df['high'].values
            low_prices = df['low'].values
            close_prices = df['close'].values
            
            # Define pattern functions and their characteristics
            pattern_functions = {
                'DOJI': (talib.CDLDOJI, PatternType.NEUTRAL),
                'HAMMER': (talib.CDLHAMMER, PatternType.BULLISH),
                'HANGING_MAN': (talib.CDLHANGINGMAN, PatternType.BEARISH),
                'SHOOTING_STAR': (talib.CDLSHOOTINGSTAR, PatternType.BEARISH),
                'INVERTED_HAMMER': (talib.CDLINVERTEDHAMMER, PatternType.BULLISH),
                'ENGULFING_BULLISH': (talib.CDLENGULFING, PatternType.BULLISH),
                'MORNING_STAR': (talib.CDLMORNINGSTAR, PatternType.BULLISH),
                'EVENING_STAR': (talib.CDLEVENINGSTAR, PatternType.BEARISH),
                'THREE_WHITE_SOLDIERS': (talib.CDL3WHITESOLDIERS, PatternType.BULLISH),
                'THREE_BLACK_CROWS': (talib.CDL3BLACKCROWS, PatternType.BEARISH)
            }
            
            for pattern_name, (pattern_func, pattern_type) in pattern_functions.items():
                try:
                    pattern_signals = pattern_func(open_prices, high_prices, low_prices, close_prices)
                    
                    # Look for recent patterns
                    for i in range(max(0, len(pattern_signals) - settings.pattern_lookback_periods), len(pattern_signals)):
                        if pattern_signals[i] != 0:  # Pattern detected
                            reliability = abs(pattern_signals[i]) / 100.0  # TA-Lib returns -100 to 100
                            strength = self._determine_pattern_strength(reliability)
                            
                            patterns.append(CandlestickPattern(
                                pattern_name=pattern_name,
                                pattern_type=pattern_type,
                                timestamp=df.index[i],
                                reliability=reliability,
                                candles_count=1,  # Most patterns are single candle
                                strength=strength,
                                volume_confirmation=None  # Could add volume analysis
                            ))
                            
                except Exception as e:
                    logger.warning(f"Error detecting pattern {pattern_name}", error=str(e))
                    continue
            
            return patterns[-10:]  # Return last 10 patterns
            
        except Exception as e:
            logger.error("Error in pattern recognition", error=str(e))
            return []
    
    # Support and Resistance
    
    def calculate_support_resistance(self, df: pd.DataFrame) -> List[SupportResistanceLevel]:
        """Calculate support and resistance levels"""
        if not self.validate_data_sufficiency(df, 50):
            return []
        
        try:
            levels = []
            
            # Use pivot highs and lows
            high_prices = df['high'].values
            low_prices = df['low'].values
            
            # Find pivot points
            pivot_highs = self._find_pivot_highs(high_prices, settings.support_resistance_periods)
            pivot_lows = self._find_pivot_lows(low_prices, settings.support_resistance_periods)
            
            # Convert to support/resistance levels
            current_price = df['close'].iloc[-1]
            
            for i, level in enumerate(pivot_highs):
                if level > 0:
                    levels.append(SupportResistanceLevel(
                        level=Decimal(str(round(level, 2))),
                        level_type="Resistance",
                        strength=SignalStrength.MODERATE,
                        touch_count=1,
                        first_touch=df.index[i],
                        last_touch=df.index[i],
                        distance_percent=Decimal(str(round(((level - current_price) / current_price) * 100, 2)))
                    ))
            
            for i, level in enumerate(pivot_lows):
                if level > 0:
                    levels.append(SupportResistanceLevel(
                        level=Decimal(str(round(level, 2))),
                        level_type="Support",
                        strength=SignalStrength.MODERATE,
                        touch_count=1,
                        first_touch=df.index[i],
                        last_touch=df.index[i],
                        distance_percent=Decimal(str(round(((level - current_price) / current_price) * 100, 2)))
                    ))
            
            # Sort by distance from current price
            levels.sort(key=lambda x: abs(float(x.distance_percent)))
            
            return levels[:10]  # Return closest 10 levels
            
        except Exception as e:
            logger.error("Error calculating support/resistance", error=str(e))
            return []
    
    # Signal Generation
    
    def generate_trading_signals(self, analysis_result: TechnicalAnalysisResult) -> List[TradingSignal]:
        """Generate trading signals based on technical analysis"""
        signals = []
        
        try:
            # Trend-following signals
            trend_signal = self._generate_trend_signal(analysis_result)
            if trend_signal:
                signals.append(trend_signal)
            
            # Momentum signals
            momentum_signal = self._generate_momentum_signal(analysis_result)
            if momentum_signal:
                signals.append(momentum_signal)
            
            # Mean reversion signals
            mean_reversion_signal = self._generate_mean_reversion_signal(analysis_result)
            if mean_reversion_signal:
                signals.append(mean_reversion_signal)
            
            return signals
            
        except Exception as e:
            logger.error("Error generating trading signals", error=str(e))
            return []
    
    # Comprehensive Analysis
    
    async def analyze_symbol(self, symbol: str, ohlcv_data: List[OHLCV], timeframe: TimeFrame) -> TechnicalAnalysisResult:
        """Perform comprehensive technical analysis for a symbol"""
        try:
            logger.info("Starting technical analysis", symbol=symbol, timeframe=timeframe)
            
            # Prepare data
            df = self.prepare_dataframe(ohlcv_data)
            
            if not self.validate_data_sufficiency(df):
                raise ValueError(f"Insufficient data for analysis: {len(df)} periods")
            
            # Calculate all indicators
            moving_averages = self.calculate_moving_averages(df)
            macd = self.calculate_macd(df)
            rsi = self.calculate_rsi(df)
            bollinger_bands = self.calculate_bollinger_bands(df)
            stochastic = self.calculate_stochastic(df)
            adx = self.calculate_adx(df)
            volume_indicators = self.calculate_volume_indicators(df)
            
            # Pattern recognition
            candlestick_patterns = []
            support_resistance = []
            
            if settings.enable_pattern_recognition:
                candlestick_patterns = self.detect_candlestick_patterns(df)
                support_resistance = self.calculate_support_resistance(df)
            
            # Calculate overall scores and signals
            current_price = Decimal(str(df['close'].iloc[-1]))
            previous_close = Decimal(str(df['close'].iloc[-2]))
            price_change = current_price - previous_close
            price_change_percent = (price_change / previous_close) * 100
            
            # Generate overall signal
            overall_signal, trend_direction, trend_strength = self._calculate_overall_signal(
                moving_averages, macd, rsi, bollinger_bands, stochastic, adx
            )
            
            # Calculate sentiment scores
            bullish_score, bearish_score, volatility_score = self._calculate_sentiment_scores(
                moving_averages, macd, rsi, bollinger_bands, stochastic, adx, volume_indicators
            )
            
            # Create analysis result
            result = TechnicalAnalysisResult(
                symbol=symbol,
                timeframe=timeframe,
                current_price=current_price,
                previous_close=previous_close,
                price_change=price_change,
                price_change_percent=price_change_percent,
                moving_averages=moving_averages,
                macd=macd,
                rsi=rsi,
                bollinger_bands=bollinger_bands,
                stochastic=stochastic,
                adx=adx,
                volume_indicators=volume_indicators,
                candlestick_patterns=candlestick_patterns,
                support_resistance=support_resistance,
                overall_signal=overall_signal,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                bullish_score=bullish_score,
                bearish_score=bearish_score,
                volatility_score=volatility_score
            )
            
            logger.info("Technical analysis completed", 
                       symbol=symbol,
                       overall_signal=overall_signal,
                       bullish_score=bullish_score,
                       bearish_score=bearish_score)
            
            return result
            
        except Exception as e:
            logger.error("Error in technical analysis", symbol=symbol, error=str(e))
            raise
    
    # Helper Methods
    
    def _detect_rsi_bullish_divergence(self, df: pd.DataFrame, rsi_values: np.ndarray) -> bool:
        """Detect RSI bullish divergence (simplified)"""
        # This is a simplified implementation
        # In practice, you'd want more sophisticated divergence detection
        return False
    
    def _detect_rsi_bearish_divergence(self, df: pd.DataFrame, rsi_values: np.ndarray) -> bool:
        """Detect RSI bearish divergence (simplified)"""
        return False
    
    def _calculate_vpt(self, df: pd.DataFrame) -> np.ndarray:
        """Calculate Volume Price Trend"""
        vpt = np.zeros(len(df))
        for i in range(1, len(df)):
            price_change_pct = (df['close'].iloc[i] - df['close'].iloc[i-1]) / df['close'].iloc[i-1]
            vpt[i] = vpt[i-1] + (df['volume'].iloc[i] * price_change_pct)
        return vpt
    
    def _determine_pattern_strength(self, reliability: float) -> SignalStrength:
        """Determine pattern strength based on reliability"""
        if reliability >= 0.8:
            return SignalStrength.VERY_STRONG
        elif reliability >= 0.6:
            return SignalStrength.STRONG
        elif reliability >= 0.4:
            return SignalStrength.MODERATE
        else:
            return SignalStrength.WEAK
    
    def _find_pivot_highs(self, prices: np.ndarray, window: int) -> np.ndarray:
        """Find pivot high points"""
        pivots = np.zeros(len(prices))
        for i in range(window, len(prices) - window):
            if all(prices[i] >= prices[i-j] for j in range(1, window+1)) and \
               all(prices[i] >= prices[i+j] for j in range(1, window+1)):
                pivots[i] = prices[i]
        return pivots
    
    def _find_pivot_lows(self, prices: np.ndarray, window: int) -> np.ndarray:
        """Find pivot low points"""
        pivots = np.zeros(len(prices))
        for i in range(window, len(prices) - window):
            if all(prices[i] <= prices[i-j] for j in range(1, window+1)) and \
               all(prices[i] <= prices[i+j] for j in range(1, window+1)):
                pivots[i] = prices[i]
        return pivots
    
    def _generate_trend_signal(self, analysis: TechnicalAnalysisResult) -> Optional[TradingSignal]:
        """Generate trend-following signal"""
        # Simplified trend signal generation
        return None
    
    def _generate_momentum_signal(self, analysis: TechnicalAnalysisResult) -> Optional[TradingSignal]:
        """Generate momentum-based signal"""
        # Simplified momentum signal generation
        return None
    
    def _generate_mean_reversion_signal(self, analysis: TechnicalAnalysisResult) -> Optional[TradingSignal]:
        """Generate mean reversion signal"""
        # Simplified mean reversion signal generation
        return None
    
    def _calculate_overall_signal(self, ma_data, macd_data, rsi_data, bb_data, stoch_data, adx_data) -> Tuple[SignalType, str, SignalStrength]:
        """Calculate overall trading signal"""
        bullish_signals = 0
        bearish_signals = 0
        
        # Analyze each indicator
        if ma_data and ma_data.golden_cross:
            bullish_signals += 2
        if ma_data and ma_data.death_cross:
            bearish_signals += 2
            
        if macd_data and macd_data.bullish_crossover:
            bullish_signals += 1
        if macd_data and macd_data.bearish_crossover:
            bearish_signals += 1
            
        if rsi_data:
            if rsi_data.oversold:
                bullish_signals += 1
            if rsi_data.overbought:
                bearish_signals += 1
                
        # Determine overall signal
        if bullish_signals > bearish_signals + 1:
            return SignalType.BUY, "Bullish", SignalStrength.MODERATE
        elif bearish_signals > bullish_signals + 1:
            return SignalType.SELL, "Bearish", SignalStrength.MODERATE
        else:
            return SignalType.HOLD, "Neutral", SignalStrength.WEAK
    
    def _calculate_sentiment_scores(self, ma_data, macd_data, rsi_data, bb_data, stoch_data, adx_data, vol_data) -> Tuple[float, float, float]:
        """Calculate bullish, bearish, and volatility scores"""
        bullish_score = 50.0
        bearish_score = 50.0
        volatility_score = 50.0
        
        # Adjust scores based on indicators
        if rsi_data:
            if rsi_data.oversold:
                bullish_score += 10
            elif rsi_data.overbought:
                bearish_score += 10
        
        if bb_data:
            if bb_data.squeeze:
                volatility_score -= 20
            else:
                volatility_score += 10
        
        # Normalize scores
        bullish_score = max(0, min(100, bullish_score))
        bearish_score = max(0, min(100, bearish_score))
        volatility_score = max(0, min(100, volatility_score))
        
        return bullish_score, bearish_score, volatility_score
