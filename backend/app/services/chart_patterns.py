import pandas as pd
import numpy as np
from typing import List
from app.models.schemas import ChartPattern

class ChartPatternAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df.columns = [c.lower() for c in self.df.columns]
        self.prices = self.df['close'].values
        self.highs = self.df['high'].values
        self.lows = self.df['low'].values
    
    def _find_peaks(self, data: np.ndarray, order: int = 5) -> tuple:
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(data, distance=order)
        troughs, _ = find_peaks(-data, distance=order)
        return peaks, troughs
    
    def detect_triangle(self) -> ChartPattern:
        if len(self.prices) < 40:
            return ChartPattern(name="Triangle", detected=False, confidence=0, reasoning="")
        
        recent = self.prices[-40:]
        highs_recent = self.highs[-40:]
        lows_recent = self.lows[-40:]
        
        # Find trendlines
        high_trend = np.polyfit(range(len(highs_recent)), highs_recent, 1)
        low_trend = np.polyfit(range(len(lows_recent)), lows_recent, 1)
        
        # Converging = triangle
        converging = abs(high_trend[0] - low_trend[0]) < 0.001
        
        detected = converging and (high_trend[0] < 0 or low_trend[0] > 0)
        
        return ChartPattern(
            name="Triangle",
            detected=detected,
            confidence=0.6 if detected else 0,
            reasoning="Converging trendlines suggest consolidation" if detected else "No clear converging pattern"
        )
    
    def detect_channel(self) -> ChartPattern:
        if len(self.prices) < 30:
            return ChartPattern(name="Channel", detected=False, confidence=0, reasoning="")
        
        recent = self.prices[-30:]
        highs_recent = self.highs[-30:]
        lows_recent = self.lows[-30:]
        
        high_trend = np.polyfit(range(len(highs_recent)), highs_recent, 1)
        low_trend = np.polyfit(range(len(lows_recent)), lows_recent, 1)
        
        parallel = abs(high_trend[0] - low_trend[0]) < 0.002
        detected = parallel and abs(high_trend[0]) > 0.0005
        
        return ChartPattern(
            name="Channel",
            detected=detected,
            confidence=0.65 if detected else 0,
            reasoning=f"Parallel {'ascending' if high_trend[0] > 0 else 'descending'} channel detected" if detected else "No clear parallel channel"
        )
    
    def detect_double_top(self) -> ChartPattern:
        if len(self.prices) < 60:
            return ChartPattern(name="Double Top", detected=False, confidence=0, reasoning="")
        
        try:
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(self.highs[-60:], distance=10, prominence=np.std(self.highs[-60:]) * 0.5)
            
            if len(peaks) >= 2:
                peak_values = self.highs[-60:][peaks]
                # Check if two peaks are at similar levels
                sorted_peaks = sorted(peak_values, reverse=True)[:2]
                similar = abs(sorted_peaks[0] - sorted_peaks[1]) / sorted_peaks[0] < 0.03
                
                detected = similar and len(peaks) >= 2
                return ChartPattern(
                    name="Double Top",
                    detected=detected,
                    confidence=0.7 if detected else 0,
                    reasoning="Two peaks at similar resistance levels" if detected else "No matching double top formation"
                )
        except Exception:
            pass
        
        return ChartPattern(name="Double Top", detected=False, confidence=0, reasoning="")
    
    def detect_double_bottom(self) -> ChartPattern:
        if len(self.prices) < 60:
            return ChartPattern(name="Double Bottom", detected=False, confidence=0, reasoning="")
        
        try:
            from scipy.signal import find_peaks
            troughs, _ = find_peaks(-self.lows[-60:], distance=10, prominence=np.std(self.lows[-60:]) * 0.5)
            
            if len(troughs) >= 2:
                trough_values = self.lows[-60:][troughs]
                sorted_troughs = sorted(trough_values)[:2]
                similar = abs(sorted_troughs[0] - sorted_troughs[1]) / sorted_troughs[0] < 0.03
                
                detected = similar and len(troughs) >= 2
                return ChartPattern(
                    name="Double Bottom",
                    detected=detected,
                    confidence=0.7 if detected else 0,
                    reasoning="Two troughs at similar support levels" if detected else "No matching double bottom formation"
                )
        except Exception:
            pass
        
        return ChartPattern(name="Double Bottom", detected=False, confidence=0, reasoning="")
    
    def detect_head_and_shoulders(self) -> ChartPattern:
        if len(self.prices) < 80:
            return ChartPattern(name="Head and Shoulders", detected=False, confidence=0, reasoning="")
        
        try:
            from scipy.signal import find_peaks
            peaks, _ = find_peaks(self.highs[-80:], distance=10, prominence=np.std(self.highs[-80:]) * 0.3)
            
            if len(peaks) >= 3:
                peak_values = self.highs[-80:][peaks]
                # Need three peaks with middle one highest
                if len(peak_values) >= 3:
                    # Get last 3 significant peaks
                    last_three = sorted(range(len(peak_values)), key=lambda i: peaks[i])[-3:]
                    three_vals = [peak_values[i] for i in last_three]
                    
                    # Middle should be highest
                    hs = three_vals[1] > three_vals[0] and three_vals[1] > three_vals[2]
                    # Shoulders should be similar
                    shoulders = abs(three_vals[0] - three_vals[2]) / max(three_vals[0], three_vals[2]) < 0.05
                    
                    detected = hs and shoulders
                    return ChartPattern(
                        name="Head and Shoulders",
                        detected=detected,
                        confidence=0.6 if detected else 0,
                        reasoning="Three peaks with middle peak higher than shoulders" if detected else "No head and shoulders formation"
                    )
        except Exception:
            pass
        
        return ChartPattern(name="Head and Shoulders", detected=False, confidence=0, reasoning="")
    
    def detect_cup_and_handle(self) -> ChartPattern:
        if len(self.prices) < 100:
            return ChartPattern(name="Cup and Handle", detected=False, confidence=0, reasoning="")
        
        # Simplified: look for U-shape followed by small pullback
        recent = self.prices[-100:]
        
        # Find minimum point (cup bottom)
        min_idx = np.argmin(recent[:60])
        left_side = recent[:min_idx]
        right_side = recent[min_idx:min_idx+40]
        
        # Cup shape: prices decline then rise
        cup_shape = len(left_side) > 10 and len(right_side) > 10 and \
                    recent[min_idx] < np.mean(left_side[:10]) and recent[min_idx] < np.mean(right_side[-10:])
        
        # Handle: small pullback after cup completion
        handle = False
        if len(recent) > min_idx + 40:
            handle_section = recent[min_idx+40:]
            if len(handle_section) > 5:
                handle = np.max(handle_section) < np.max(right_side) and np.min(handle_section) > recent[min_idx]
        
        detected = cup_shape and handle
        return ChartPattern(
            name="Cup and Handle",
            detected=detected,
            confidence=0.55 if detected else 0,
            reasoning="U-shaped cup with handle consolidation" if detected else "No cup and handle pattern"
        )
    
    def detect_all(self) -> List[ChartPattern]:
        return [
            self.detect_triangle(),
            self.detect_channel(),
            self.detect_double_top(),
            self.detect_double_bottom(),
            self.detect_head_and_shoulders(),
            self.detect_cup_and_handle(),
        ]
