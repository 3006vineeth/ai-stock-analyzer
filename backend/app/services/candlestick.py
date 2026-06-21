import pandas as pd
import numpy as np
from typing import List
from app.models.schemas import CandlestickPattern

class CandlestickAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df.columns = [c.lower() for c in self.df.columns]
        self.last = self.df.iloc[-1]
        self.prev = self.df.iloc[-2] if len(self.df) > 1 else None
        self.prev2 = self.df.iloc[-3] if len(self.df) > 2 else None
    
    def _body(self, row) -> float:
        return abs(row['close'] - row['open'])
    
    def _upper_shadow(self, row) -> float:
        return row['high'] - max(row['open'], row['close'])
    
    def _lower_shadow(self, row) -> float:
        return min(row['open'], row['close']) - row['low']
    
    def _is_bullish(self, row) -> bool:
        return row['close'] > row['open']
    
    def _is_bearish(self, row) -> bool:
        return row['close'] < row['open']
    
    def detect_hammer(self) -> CandlestickPattern:
        body = self._body(self.last)
        lower = self._lower_shadow(self.last)
        upper = self._upper_shadow(self.last)
        
        detected = lower > 2 * body and upper < body * 0.5 and self._is_bullish(self.last)
        return CandlestickPattern(
            name="Hammer",
            detected=detected,
            significance="Bullish reversal at support",
            confirmation_needed="Wait for next candle to close above hammer's high"
        )
    
    def detect_shooting_star(self) -> CandlestickPattern:
        body = self._body(self.last)
        upper = self._upper_shadow(self.last)
        lower = self._lower_shadow(self.last)
        
        detected = upper > 2 * body and lower < body * 0.5 and self._is_bearish(self.last)
        return CandlestickPattern(
            name="Shooting Star",
            detected=detected,
            significance="Bearish reversal at resistance",
            confirmation_needed="Wait for next candle to close below shooting star's low"
        )
    
    def detect_doji(self) -> CandlestickPattern:
        body = self._body(self.last)
        range_val = self.last['high'] - self.last['low']
        
        detected = body < range_val * 0.1 and range_val > 0
        return CandlestickPattern(
            name="Doji",
            detected=detected,
            significance="Indecision, potential reversal or continuation",
            confirmation_needed="Wait for breakout above high or below low"
        )
    
    def detect_engulfing(self) -> CandlestickPattern:
        if self.prev is None:
            return CandlestickPattern(name="Engulfing", detected=False, significance="", confirmation_needed="")
        
        prev_body = self._body(self.prev)
        curr_body = self._body(self.last)
        
        bullish = self._is_bearish(self.prev) and self._is_bullish(self.last) and \
                  self.last['close'] > self.prev['open'] and self.last['open'] < self.prev['close']
        bearish = self._is_bullish(self.prev) and self._is_bearish(self.last) and \
                  self.last['close'] < self.prev['open'] and self.last['open'] > self.prev['close']
        
        detected = bullish or bearish
        return CandlestickPattern(
            name="Engulfing",
            detected=detected,
            significance="Bullish engulfing" if bullish else "Bearish engulfing" if bearish else "",
            confirmation_needed="Volume confirmation on next candle"
        )
    
    def detect_morning_star(self) -> CandlestickPattern:
        if self.prev is None or self.prev2 is None:
            return CandlestickPattern(name="Morning Star", detected=False, significance="", confirmation_needed="")
        
        first_bearish = self._is_bearish(self.prev2) and self._body(self.prev2) > 0
        second_small = self._body(self.last) < self._body(self.prev2) * 0.5
        third_bullish = self._is_bullish(self.last) and self.last['close'] > (self.prev2['open'] + self.prev2['close']) / 2
        
        detected = first_bearish and second_small and third_bullish
        return CandlestickPattern(
            name="Morning Star",
            detected=detected,
            significance="Strong bullish reversal pattern",
            confirmation_needed="Price should close above the middle of the first candle"
        )
    
    def detect_evening_star(self) -> CandlestickPattern:
        if self.prev is None or self.prev2 is None:
            return CandlestickPattern(name="Evening Star", detected=False, significance="", confirmation_needed="")
        
        first_bullish = self._is_bullish(self.prev2) and self._body(self.prev2) > 0
        second_small = self._body(self.last) < self._body(self.prev2) * 0.5
        third_bearish = self._is_bearish(self.last) and self.last['close'] < (self.prev2['open'] + self.prev2['close']) / 2
        
        detected = first_bullish and second_small and third_bearish
        return CandlestickPattern(
            name="Evening Star",
            detected=detected,
            significance="Strong bearish reversal pattern",
            confirmation_needed="Price should close below the middle of the first candle"
        )
    
    def detect_harami(self) -> CandlestickPattern:
        if self.prev is None:
            return CandlestickPattern(name="Harami", detected=False, significance="", confirmation_needed="")
        
        prev_body = self._body(self.prev)
        curr_body = self._body(self.last)
        
        bullish = self._is_bearish(self.prev) and self._is_bullish(self.last) and \
                  curr_body < prev_body * 0.5 and self.last['close'] > self.prev['low'] and self.last['open'] < self.prev['high']
        bearish = self._is_bullish(self.prev) and self._is_bearish(self.last) and \
                  curr_body < prev_body * 0.5 and self.last['close'] > self.prev['low'] and self.last['open'] < self.prev['high']
        
        detected = bullish or bearish
        return CandlestickPattern(
            name="Harami",
            detected=detected,
            significance="Bullish harami" if bullish else "Bearish harami" if bearish else "",
            confirmation_needed="Breakout in direction of the harami"
        )
    
    def detect_marubozu(self) -> CandlestickPattern:
        body = self._body(self.last)
        range_val = self.last['high'] - self.last['low']
        upper = self._upper_shadow(self.last)
        lower = self._lower_shadow(self.last)
        
        detected = body > range_val * 0.9 and upper < body * 0.05 and lower < body * 0.05
        return CandlestickPattern(
            name="Marubozu",
            detected=detected,
            significance="Bullish Marubozu" if self._is_bullish(self.last) else "Bearish Marubozu",
            confirmation_needed="Strong directional move; watch for continuation"
        )
    
    def detect_all(self) -> List[CandlestickPattern]:
        return [
            self.detect_hammer(),
            self.detect_shooting_star(),
            self.detect_doji(),
            self.detect_engulfing(),
            self.detect_morning_star(),
            self.detect_evening_star(),
            self.detect_harami(),
            self.detect_marubozu(),
        ]
