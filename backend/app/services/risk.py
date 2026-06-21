import pandas as pd
import numpy as np
from typing import Dict, Any
from app.models.schemas import RiskAssessment

class RiskAnalyzer:
    def __init__(self, df: pd.DataFrame, info: Dict[str, Any]):
        self.df = df.copy()
        self.df.columns = [c.lower() for c in self.df.columns]
        self.info = info
    
    def analyze(self) -> RiskAssessment:
        # Volatility risk (from ATR)
        close = self.df['close'].iloc[-1]
        high_low = self.df['high'] - self.df['low']
        high_close = abs(self.df['high'] - self.df['close'].shift())
        low_close = abs(self.df['low'] - self.df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=14).mean().iloc[-1]
        
        volatility_pct = (atr / close) * 100 if close > 0 else 0
        if volatility_pct > 5:
            volatility_risk = "High — daily swings exceed 5% of price"
        elif volatility_pct > 2.5:
            volatility_risk = "Moderate — daily swings between 2.5-5%"
        else:
            volatility_risk = "Low — daily swings under 2.5%"
        
        # Financial risk
        debt_equity = self.info.get("debtToEquity")
        if debt_equity is not None:
            de_ratio = debt_equity / 100
            if de_ratio > 2:
                financial_risk = "High — debt-to-equity exceeds 2x"
            elif de_ratio > 1:
                financial_risk = "Moderate — elevated leverage"
            else:
                financial_risk = "Low — manageable debt levels"
        else:
            financial_risk = "Unknown — data unavailable"
        
        # Business risk (from sector)
        sector = self.info.get("sector", "Unknown")
        cyclical_sectors = ["Materials", "Energy", "Automotive", "Infrastructure"]
        defensive_sectors = ["FMCG", "Healthcare", "Utilities", "Consumer"]
        
        if sector in cyclical_sectors:
            business_risk = "Moderate-High — cyclical sector exposure"
        elif sector in defensive_sectors:
            business_risk = "Low — defensive sector provides stability"
        else:
            business_risk = "Moderate — sector-dependent risks"
        
        # Sector risk
        sector_risk = f"{sector} sector faces typical industry risks including competition and regulatory changes"
        
        # Market risk
        beta = self.info.get("beta")
        if beta is not None:
            if beta > 1.3:
                market_risk = f"High — beta of {beta:.2f} means amplified market moves"
            elif beta > 0.8:
                market_risk = f"Moderate — beta of {beta:.2f} tracks market closely"
            else:
                market_risk = f"Low — beta of {beta:.2f} below market sensitivity"
        else:
            market_risk = "Unknown — beta data unavailable"
        
        # Overall score (1-10)
        score = 5  # base
        
        if volatility_pct > 5: score += 2
        elif volatility_pct > 2.5: score += 1
        else: score -= 1
        
        if debt_equity is not None and debt_equity / 100 > 2: score += 2
        elif debt_equity is not None and debt_equity / 100 > 1: score += 1
        else: score -= 1
        
        if sector in cyclical_sectors: score += 1
        elif sector in defensive_sectors: score -= 1
        
        if beta is not None and beta > 1.3: score += 1
        elif beta is not None and beta < 0.8: score -= 1
        
        score = max(1, min(10, score))
        debt_equity_str = (
            f"{debt_equity:.2f}"
            if debt_equity is not None
            else "N/A"
        )

        beta_str = (
            f"{beta:.2f}"
            if beta is not None
            else "N/A"
        )
        reasoning = (
            f"Risk score of {score}/10 based on: "
            f"volatility ({volatility_pct:.1f}%), "
            f"leverage ({debt_equity_str}), "
            f"sector ({sector}), "
            f"and market sensitivity (beta {beta_str})."
        )
        
        return RiskAssessment(
            score=score,
            volatility_risk=volatility_risk,
            financial_risk=financial_risk,
            business_risk=business_risk,
            sector_risk=sector_risk,
            market_risk=market_risk,
            reasoning=reasoning
        )
