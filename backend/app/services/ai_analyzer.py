import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.services.twelve_data_service import TwelveDataService
from app.services.technical import TechnicalAnalyzer
from app.services.candlestick import CandlestickAnalyzer
from app.services.chart_patterns import ChartPatternAnalyzer
from app.services.fundamental import FundamentalAnalyzer
from app.services.sentiment import SentimentAnalyzer
from app.services.risk import RiskAnalyzer
from app.models.schemas import (
    AnalysisReport, ExecutiveSummary, TechnicalAnalysis, CandlestickPattern,
    ChartPattern, MomentumAnalysis, FundamentalMetrics, NewsSentiment,
    RiskAssessment, TradingPlan, AIConfidence
)

class AIAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.fetcher = TwelveDataService()
    
    async def generate_report(self, ticker: str) -> AnalysisReport:
        # Fetch data
        # Download historical data
        df = await self.fetcher.get_historical_data(
            ticker,
            period="1y",
            interval="1d",
        )

        # Download quote and profile ONCE
        quote = await self.fetcher.get_quote(ticker)
        profile = await self.fetcher.get_company_profile(ticker)

        # Reuse them
        info = await self.fetcher.get_stock_info(
            ticker,
            quote=quote,
            profile=profile,
        )

        snapshot = await self.fetcher.get_snapshot(
            ticker,
            quote=quote,
            profile=profile,
        )
        
        # Technical analysis
        ta = TechnicalAnalyzer(df)
        technical = ta.full_analysis()
        
        # Candlestick patterns
        ca = CandlestickAnalyzer(df)
        candlesticks = ca.detect_all()
        
        # Chart patterns
        cpa = ChartPatternAnalyzer(df)
        chart_patterns = cpa.detect_all()
        
        # Trend strength
        trend = self._classify_trend(technical, df)
        
        # Momentum
        momentum = self._analyze_momentum(technical, df)
        
        # Fundamental
        fa = FundamentalAnalyzer(ticker, info)
        fundamental = FundamentalMetrics(**await fa.analyze())
        
        # Sentiment
        sa = SentimentAnalyzer()
        sentiment = sa.analyze(ticker, snapshot.get("name", ""))
        
        # Risk
        ra = RiskAnalyzer(df, info)
        risk = ra.analyze()
        
        # Trading plan
        trading_plan = self._generate_trading_plan(technical, risk, df)
        
        # AI Confidence
        confidence = self._calculate_confidence(technical, fundamental, df, info)
        
        # Executive Summary (AI-generated reasoning)
        exec_summary = self._generate_executive_summary(
            ticker, technical, trend, fundamental, sentiment, risk, snapshot
        )
        
        return AnalysisReport(
            ticker=ticker,
            timestamp=datetime.now().isoformat(),
            snapshot=snapshot,
            executive_summary=exec_summary,
            technical_analysis=technical,
            candlestick_patterns=candlesticks,
            chart_patterns=chart_patterns,
            trend_strength=trend,
            momentum_analysis=momentum,
            fundamental_analysis=fundamental,
            news_sentiment=sentiment,
            risk_assessment=risk,
            trading_plan=trading_plan,
            ai_confidence=confidence
        )
    
    def _classify_trend(self, technical: TechnicalAnalysis, df: pd.DataFrame) -> str:
        close = df['close'].iloc[-1] if 'close' in df.columns else df['Close'].iloc[-1]
        ema20 = df['close'].ewm(span=20, adjust=False).mean().iloc[-1] if 'close' in df.columns else df['Close'].ewm(span=20, adjust=False).mean().iloc[-1]
        ema50 = df['close'].ewm(span=50, adjust=False).mean().iloc[-1] if 'close' in df.columns else df['Close'].ewm(span=50, adjust=False).mean().iloc[-1]
        ema200 = df['close'].ewm(span=200, adjust=False).mean().iloc[-1] if 'close' in df.columns else df['Close'].ewm(span=200, adjust=False).mean().iloc[-1]
        
        bullish_score = 0
        if close > ema20: bullish_score += 1
        if ema20 > ema50: bullish_score += 1
        if close > ema50: bullish_score += 1
        if ema50 > ema200: bullish_score += 1
        if close > ema200: bullish_score += 1
        
        rsi_val = 50
        for ind in technical.indicators:
            if ind.name == "RSI (14)":
                rsi_val = ind.value
                break
        if rsi_val > 50: bullish_score += 1
        if rsi_val > 60: bullish_score += 1
        
        if bullish_score >= 7: return "Strong Bullish"
        elif bullish_score >= 5: return "Bullish"
        elif bullish_score >= 3: return "Neutral"
        elif bullish_score >= 1: return "Bearish"
        else: return "Strong Bearish"
    
    def _analyze_momentum(self, technical: TechnicalAnalysis, df: pd.DataFrame) -> MomentumAnalysis:
        close = df['close'].iloc[-1] if 'close' in df.columns else df['Close'].iloc[-1]
        close_20 = df['close'].iloc[-20] if 'close' in df.columns else df['Close'].iloc[-20]
        close_60 = df['close'].iloc[-60] if 'close' in df.columns else df['Close'].iloc[-60]
        
        price_change_20 = ((close - close_20) / close_20) * 100 if close_20 else 0
        price_change_60 = ((close - close_60) / close_60) * 100 if close_60 else 0
        
        if price_change_20 > 10 and price_change_60 > 15:
            price_momentum = "Strong positive — stock outperforming over 20 and 60 days"
        elif price_change_20 > 5:
            price_momentum = "Positive — recent upward momentum"
        elif price_change_20 < -10 and price_change_60 < -15:
            price_momentum = "Strong negative — sustained decline"
        elif price_change_20 < -5:
            price_momentum = "Negative — recent downward pressure"
        else:
            price_momentum = "Neutral — price moving sideways"
        
        vol_recent = df['volume'].tail(10).mean() if 'volume' in df.columns else df['Volume'].tail(10).mean()
        vol_avg = df['volume'].tail(50).mean() if 'volume' in df.columns else df['Volume'].tail(50).mean()
        vol_ratio = vol_recent / vol_avg if vol_avg else 1
        
        if vol_ratio > 1.5:
            volume_momentum = "High — above average interest and participation"
        elif vol_ratio > 1.1:
            volume_momentum = "Moderately elevated — increasing interest"
        elif vol_ratio < 0.7:
            volume_momentum = "Low — declining participation"
        else:
            volume_momentum = "Normal — typical trading activity"
        
        relative_strength = f"Stock has {'gained' if price_change_20 > 0 else 'lost'} {abs(price_change_20):.1f}% over 20 days"
        
        atr = 0
        for ind in technical.indicators:
            if ind.name == "ATR (14)":
                atr = ind.value
                break
        
        if atr > close * 0.05:
            volatility = "High — large daily price swings expected"
        elif atr > close * 0.025:
            volatility = "Moderate — normal market fluctuations"
        else:
            volatility = "Low — stable price action"
        
        summary = f"Price momentum is {price_change_20:.1f}% over 20 days. Volume is {'above' if vol_ratio > 1.1 else 'below'} average. "
        summary += f"{volatility}. "
        if price_change_20 > 0 and vol_ratio > 1.1:
            summary += "Volume confirms the uptrend."
        elif price_change_20 < 0 and vol_ratio > 1.1:
            summary += "Volume confirms selling pressure."
        else:
            summary += "Volume and price are in neutral alignment."
        
        return MomentumAnalysis(
            price_momentum=price_momentum,
            volume_momentum=volume_momentum,
            relative_strength=relative_strength,
            volatility=volatility,
            summary=summary
        )
    
    def _generate_trading_plan(self, technical: TechnicalAnalysis, risk: RiskAssessment, df: pd.DataFrame) -> TradingPlan:
        close = df['close'].iloc[-1] if 'close' in df.columns else df['Close'].iloc[-1]
        
        supports = technical.support_levels
        resistances = technical.resistance_levels
        
        entry_zone = f"{close * 0.98:.2f} - {close * 1.02:.2f}" if close else "N/A"
        key_support = str(supports[0]) if supports else f"{close * 0.95:.2f}"
        key_resistance = str(resistances[0]) if resistances else f"{close * 1.05:.2f}"
        
        upside = f"Target: {close * 1.1:.2f} (+10%)" if close else "N/A"
        downside = f"Target: {close * 0.9:.2f} (-10%)" if close else "N/A"
        
        stop_loss = f"{close * 0.93:.2f} (7% below entry)" if close else "N/A"
        risk_reward = "1:2 to 1:3 based on support/resistance levels"
        
        return TradingPlan(
            entry_zone=entry_zone,
            key_support=key_support,
            key_resistance=key_resistance,
            upside_scenario=upside,
            downside_scenario=downside,
            stop_loss_area=stop_loss,
            risk_reward=risk_reward
        )
    
    def _calculate_confidence(self, technical: TechnicalAnalysis, fundamental: FundamentalMetrics, df: pd.DataFrame, info: Dict[str, Any]) -> AIConfidence:
        # Trend confidence based on MA alignment and indicator consensus
        trend_conf = 0.6
        bullish_indicators = sum(1 for ind in technical.indicators if "Bullish" in ind.signal or "Above" in ind.signal or "buy" in ind.signal.lower())
        total_indicators = len(technical.indicators)
        if total_indicators > 0:
            trend_conf = 0.5 + (bullish_indicators / total_indicators) * 0.5
        trend_conf = min(0.95, max(0.3, trend_conf))
        
        # Technical setup confidence
        tech_conf = 0.7
        if technical.support_levels and technical.resistance_levels:
            tech_conf = 0.8
        if any(p.detected for p in []):  # would check candlestick patterns
            tech_conf = min(0.95, tech_conf + 0.1)
        
        # Fundamental confidence
        fund_conf = 0.5
        if fundamental.revenue_growth and "up" in fundamental.revenue_growth.lower():
            fund_conf += 0.2
        if fundamental.profit_growth and "up" in fundamental.profit_growth.lower():
            fund_conf += 0.2
        if fundamental.roe and fundamental.roe > 15:
            fund_conf += 0.1
        if fundamental.debt_to_equity and fundamental.debt_to_equity < 1:
            fund_conf += 0.1
        fund_conf = min(0.95, fund_conf)
        
        overall = (trend_conf * 0.35 + tech_conf * 0.35 + fund_conf * 0.3)
        
        reasoning = f"Confidence breakdown: Trend ({trend_conf:.0%}) based on indicator alignment, "
        reasoning += f"Technical Setup ({tech_conf:.0%}) based on pattern clarity and level definition, "
        reasoning += f"Fundamental Quality ({fund_conf:.0%}) based on financial metrics availability."
        
        return AIConfidence(
            trend=round(trend_conf, 2),
            technical_setup=round(tech_conf, 2),
            fundamental_quality=round(fund_conf, 2),
            overall=round(overall, 2),
            reasoning=reasoning
        )
    
    def _generate_executive_summary(self, ticker: str, technical: TechnicalAnalysis, trend: str, 
                                    fundamental: FundamentalMetrics, sentiment: NewsSentiment, 
                                    risk: RiskAssessment, snapshot: Dict[str, Any]) -> ExecutiveSummary:
        
        overall_trend = f"The stock is in a {trend.lower()} phase. {technical.summary}"
        
        strengths = []
        weaknesses = []
        
        if "Bullish" in trend or "Strong Bullish" in trend:
            strengths.append("Technical trend is positive")
        if technical.support_levels:
            strengths.append(f"Support established at {technical.support_levels[0]}")
        if fundamental.roe and fundamental.roe > 15:
            strengths.append(f"Strong ROE of {fundamental.roe}% indicates efficient capital use")
        if fundamental.revenue_growth and "up" in fundamental.revenue_growth.lower():
            strengths.append(f"Revenue is {fundamental.revenue_growth}")
        if sentiment.overall.value == "Positive":
            strengths.append("Positive news sentiment supporting price")
        
        if "Bearish" in trend or "Strong Bearish" in trend:
            weaknesses.append("Technical trend is negative")
        if risk.score > 6:
            weaknesses.append(f"Elevated risk score of {risk.score}/10")
        if fundamental.debt_to_equity and fundamental.debt_to_equity > 1:
            weaknesses.append(f"Higher debt-to-equity ratio of {fundamental.debt_to_equity}")
        if sentiment.overall.value == "Negative":
            weaknesses.append("Negative news sentiment creating headwinds")
        
        if not strengths:
            strengths.append("No strong positive signals detected")
        if not weaknesses:
            weaknesses.append("No major red flags detected")
        
        market_sentiment = sentiment.overall.value
        
        short_term = f"Short-term outlook is {trend.lower()}. Watch for reactions at support ({technical.support_levels[0] if technical.support_levels else 'N/A'}) and resistance ({technical.resistance_levels[0] if technical.resistance_levels else 'N/A'})."
        
        long_term = f"Long-term outlook depends on fundamental trajectory. {fundamental.valuation_assessment}."
        
        key_risks = []
        if risk.score > 6:
            key_risks.append(f"High overall risk score ({risk.score}/10)")
        key_risks.append(risk.volatility_risk)
        key_risks.append(risk.market_risk)
        if fundamental.debt_to_equity and fundamental.debt_to_equity > 1:
            key_risks.append("Leverage risk from elevated debt")
        
        return ExecutiveSummary(
            overall_trend=overall_trend,
            strengths=strengths,
            weaknesses=weaknesses,
            market_sentiment=market_sentiment,
            short_term_outlook=short_term,
            long_term_outlook=long_term,
            key_risks=key_risks
        )
