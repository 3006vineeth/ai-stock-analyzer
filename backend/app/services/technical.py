import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from app.models.schemas import (
    TechnicalIndicator, TechnicalAnalysis, CandlestickPattern, 
    ChartPattern, MomentumAnalysis, TrendStrength
)

class TechnicalAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df.columns = [c.lower() for c in self.df.columns]
    
    # ── Moving Averages ─────────────────────────────────────
    
    def ema(self, period: int) -> pd.Series:
        return self.df['close'].ewm(span=period, adjust=False).mean()
    
    def sma(self, period: int) -> pd.Series:
        return self.df['close'].rolling(window=period).mean()
    
    def calculate_all_mas(self) -> Dict[str, float]:
        return {
            "EMA_20": round(self.ema(20).iloc[-1], 2),
            "EMA_50": round(self.ema(50).iloc[-1], 2),
            "EMA_100": round(self.ema(100).iloc[-1], 2),
            "EMA_200": round(self.ema(200).iloc[-1], 2),
            "SMA_20": round(self.sma(20).iloc[-1], 2),
            "SMA_50": round(self.sma(50).iloc[-1], 2),
        }
    
    # ── RSI ─────────────────────────────────────────────────
    
    def rsi(self, period: int = 14) -> float:
        delta = self.df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2)
    
    def rsi_signal(self, rsi_val: float) -> str:
        if rsi_val > 70: return "Overbought"
        if rsi_val < 30: return "Oversold"
        return "Neutral"
    
    # ── MACD ──────────────────────────────────────────────
    
    def macd(self) -> Dict[str, float]:
        ema12 = self.ema(12)
        ema26 = self.ema(26)
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            "macd": round(macd_line.iloc[-1], 4),
            "signal": round(signal_line.iloc[-1], 4),
            "histogram": round(histogram.iloc[-1], 4),
            "trend": "Bullish" if macd_line.iloc[-1] > signal_line.iloc[-1] else "Bearish"
        }
    
    # ── Bollinger Bands ───────────────────────────────────
    
    def bollinger_bands(self, period: int = 20, std_dev: int = 2) -> Dict[str, float]:
        sma = self.sma(period)
        std = self.df['close'].rolling(window=period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        close = self.df['close'].iloc[-1]
        return {
            "upper": round(upper.iloc[-1], 2),
            "middle": round(sma.iloc[-1], 2),
            "lower": round(lower.iloc[-1], 2),
            "position": "Above Upper" if close > upper.iloc[-1] else "Below Lower" if close < lower.iloc[-1] else "Within Bands",
            "bandwidth": round((upper.iloc[-1] - lower.iloc[-1]) / sma.iloc[-1] * 100, 2),
        }
    
    # ── Supertrend ──────────────────────────────────────────
    
    def supertrend(self, period: int = 10, multiplier: float = 3.0) -> Dict[str, Any]:
        hl2 = (self.df['high'] + self.df['low']) / 2
        atr = self._atr(period)
        
        upper_band = hl2 + (multiplier * atr)
        lower_band = hl2 - (multiplier * atr)
        
        st = np.zeros(len(self.df))
        direction = np.zeros(len(self.df))
        
        for i in range(1, len(self.df)):
            if self.df['close'].iloc[i] > upper_band.iloc[i-1]:
                direction[i] = 1
            elif self.df['close'].iloc[i] < lower_band.iloc[i-1]:
                direction[i] = -1
            else:
                direction[i] = direction[i-1]
            
            if direction[i] == 1:
                st[i] = max(lower_band.iloc[i], st[i-1] if direction[i-1] == 1 else lower_band.iloc[i])
            else:
                st[i] = min(upper_band.iloc[i], st[i-1] if direction[i-1] == -1 else upper_band.iloc[i])
        
        return {
            "value": round(st[-1], 2),
            "direction": "Bullish" if direction[-1] == 1 else "Bearish",
            "signal": "Buy" if direction[-1] == 1 and direction[-2] == -1 else "Sell" if direction[-1] == -1 and direction[-2] == 1 else "Hold"
        }
    
    # ── ADX ─────────────────────────────────────────────────
    
    def adx(self, period: int = 14) -> Dict[str, float]:
        high = self.df['high']
        low = self.df['low']
        close = self.df['close']
        
        plus_dm = high.diff()
        minus_dm = -low.diff()
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        plus_dm = plus_dm.where(plus_dm > minus_dm, 0)
        minus_dm = minus_dm.where(minus_dm > plus_dm, 0)
        
        atr = self._atr(period)
        
        plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(period).mean() / atr)
        dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
        adx = dx.rolling(period).mean()
        
        return {
            "adx": round(adx.iloc[-1], 2),
            "plus_di": round(plus_di.iloc[-1], 2),
            "minus_di": round(minus_di.iloc[-1], 2),
            "trend_strength": "Strong" if adx.iloc[-1] > 25 else "Weak"
        }
    
    # ── ATR ─────────────────────────────────────────────────
    
    def _atr(self, period: int = 14) -> pd.Series:
        high_low = self.df['high'] - self.df['low']
        high_close = abs(self.df['high'] - self.df['close'].shift())
        low_close = abs(self.df['low'] - self.df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()
    
    def atr(self, period: int = 14) -> float:
        return round(self._atr(period).iloc[-1], 2)
    
    # ── VWAP ────────────────────────────────────────────────
    
    def vwap(self) -> Dict[str, float]:
        typical_price = (self.df['high'] + self.df['low'] + self.df['close']) / 3
        vwap = (typical_price * self.df['volume']).cumsum() / self.df['volume'].cumsum()
        close = self.df['close'].iloc[-1]
        return {
            "vwap": round(vwap.iloc[-1], 2),
            "position": "Above VWAP" if close > vwap.iloc[-1] else "Below VWAP",
            "deviation_pct": round((close - vwap.iloc[-1]) / vwap.iloc[-1] * 100, 2)
        }
    
    # ── Volume Profile ──────────────────────────────────────
    
    def volume_profile(self, bins: int = 20) -> Dict[str, Any]:
        prices = self.df['close']
        volumes = self.df['volume']
        
        hist, edges = np.histogram(prices, bins=bins, weights=volumes)
        poc_idx = np.argmax(hist)
        poc = (edges[poc_idx] + edges[poc_idx + 1]) / 2
        
        # Value area (70% of volume)
        sorted_idx = np.argsort(hist)[::-1]
        cumsum = 0
        total_vol = hist.sum()
        value_area_idx = []
        for idx in sorted_idx:
            cumsum += hist[idx]
            value_area_idx.append(idx)
            if cumsum >= total_vol * 0.7:
                break
        
        value_area_low = min([edges[i] for i in value_area_idx])
        value_area_high = max([edges[i+1] for i in value_area_idx])
        
        return {
            "poc": round(poc, 2),
            "value_area_low": round(value_area_low, 2),
            "value_area_high": round(value_area_high, 2),
        }
    
    # ── Support / Resistance ────────────────────────────────
    
    def find_support_resistance(self, lookback: int = 60) -> Tuple[List[float], List[float]]:
        recent = self.df.tail(lookback)
        
        # Find local minima (support)
        lows = recent['low']
        supports = []
        for i in range(1, len(lows) - 1):
            if lows.iloc[i] < lows.iloc[i-1] and lows.iloc[i] < lows.iloc[i+1]:
                supports.append(lows.iloc[i])
        
        # Find local maxima (resistance)
        highs = recent['high']
        resistances = []
        for i in range(1, len(highs) - 1):
            if highs.iloc[i] > highs.iloc[i-1] and highs.iloc[i] > highs.iloc[i+1]:
                resistances.append(highs.iloc[i])
        
        # Cluster nearby levels
        supports = self._cluster_levels(supports, threshold=0.02)
        resistances = self._cluster_levels(resistances, threshold=0.02)
        
        return supports, resistances
    
    def _cluster_levels(self, levels: List[float], threshold: float = 0.02) -> List[float]:
        if not levels:
            return []
        levels = sorted(levels)
        clusters = [[levels[0]]]
        for level in levels[1:]:
            if abs(level - clusters[-1][-1]) / clusters[-1][-1] < threshold:
                clusters[-1].append(level)
            else:
                clusters.append([level])
        return [round(sum(c) / len(c), 2) for c in clusters]
    
    # ── Trend Analysis ──────────────────────────────────────
    
    def analyze_trend(self) -> str:
        ema20 = self.ema(20).iloc[-1]
        ema50 = self.ema(50).iloc[-1]
        ema200 = self.ema(200).iloc[-1]
        close = self.df['close'].iloc[-1]
        
        if close > ema20 > ema50 > ema200:
            return "Strong Uptrend"
        elif close > ema20 > ema50:
            return "Uptrend"
        elif close < ema20 < ema50 < ema200:
            return "Strong Downtrend"
        elif close < ema20 < ema50:
            return "Downtrend"
        else:
            return "Sideways/Consolidation"
    
    # ── Full Technical Analysis ───────────────────────────
    
    def full_analysis(self) -> TechnicalAnalysis:
        mas = self.calculate_all_mas()
        rsi_val = self.rsi()
        macd_data = self.macd()
        bb = self.bollinger_bands()
        st = self.supertrend()
        adx_data = self.adx()
        atr_val = self.atr()
        vwap_data = self.vwap()
        vp = self.volume_profile()
        supports, resistances = self.find_support_resistance()
        trend = self.analyze_trend()
        
        indicators = [
            TechnicalIndicator(name="RSI (14)", value=rsi_val, signal=self.rsi_signal(rsi_val), explanation=f"RSI at {rsi_val} indicates {'overbought conditions' if rsi_val > 70 else 'oversold conditions' if rsi_val < 30 else 'neutral momentum'}"),
            TechnicalIndicator(name="MACD", value=macd_data, signal=macd_data["trend"], explanation=f"MACD line ({macd_data['macd']}) {'above' if macd_data['trend'] == 'Bullish' else 'below'} signal line ({macd_data['signal']})"),
            TechnicalIndicator(name="Bollinger Bands", value=bb, signal=bb["position"], explanation=f"Price is {bb['position']} with bandwidth {bb['bandwidth']}%"),
            TechnicalIndicator(name="Supertrend", value=st["value"], signal=st["direction"], explanation=f"Supertrend indicates {st['direction']} trend"),
            TechnicalIndicator(name="ADX (14)", value=adx_data["adx"], signal=adx_data["trend_strength"], explanation=f"ADX at {adx_data['adx']} suggests {adx_data['trend_strength'].lower()} trend strength"),
            TechnicalIndicator(name="ATR (14)", value=atr_val, signal="High" if atr_val > self.df['close'].iloc[-1] * 0.03 else "Normal", explanation=f"ATR of {atr_val} indicates {'elevated' if atr_val > self.df['close'].iloc[-1] * 0.03 else 'normal'} volatility"),
            TechnicalIndicator(name="VWAP", value=vwap_data["vwap"], signal=vwap_data["position"], explanation=f"Price is {vwap_data['position']} by {vwap_data['deviation_pct']}%"),
            TechnicalIndicator(name="Volume Profile POC", value=vp["poc"], signal="Key Level", explanation=f"Point of Control at {vp['poc']} with value area {vp['value_area_low']} - {vp['value_area_high']}"),
        ]
        
        for name, value in mas.items():
            indicators.append(TechnicalIndicator(
                name=name, value=value, 
                signal="Above Price" if value < self.df['close'].iloc[-1] else "Below Price",
                explanation=f"{name} at {value} acts as {'support' if value < self.df['close'].iloc[-1] else 'resistance'}"
            ))
        
        summary = f"Overall trend is {trend}. "
        if trend in ["Strong Uptrend", "Uptrend"]:
            summary += "Multiple moving averages align bullishly. "
        elif trend in ["Strong Downtrend", "Downtrend"]:
            summary += "Multiple moving averages align bearishly. "
        else:
            summary += "Moving averages are mixed, suggesting consolidation. "
        
        summary += f"RSI shows {self.rsi_signal(rsi_val)} conditions. MACD confirms {macd_data['trend']} momentum. "
        summary += f"ADX at {adx_data['adx']} indicates {adx_data['trend_strength'].lower()} trend strength."
        
        return TechnicalAnalysis(
            trend=trend,
            support_levels=supports[:5],
            resistance_levels=resistances[:5],
            indicators=indicators,
            summary=summary
        )
