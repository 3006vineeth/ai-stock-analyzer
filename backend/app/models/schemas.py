from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

# ── Search ──────────────────────────────────────────────────────

class StockSearchResult(BaseModel):
    name: str
    nse_symbol: str
    bse_symbol: str
    sector: str
    industry: str

class StockSearchResponse(BaseModel):
    results: List[StockSearchResult]

# ── Snapshot ─────────────────────────────────────────────────────

class StockSnapshot(BaseModel):
    name: str
    nse_symbol: str
    current_price: float
    change: float
    change_percent: float
    market_cap: str
    sector: str
    industry: str
    pe_ratio: Optional[float]
    pb_ratio: Optional[float]
    dividend_yield: Optional[float]
    week_52_high: Optional[float]
    week_52_low: Optional[float]
    avg_volume: Optional[int]

# ── Technical ────────────────────────────────────────────────────

class TechnicalIndicator(BaseModel):
    name: str
    value: Any
    signal: str
    explanation: str

class TechnicalAnalysis(BaseModel):
    trend: str
    support_levels: List[float]
    resistance_levels: List[float]
    indicators: List[TechnicalIndicator]
    summary: str

# ── Patterns ───────────────────────────────────────────────────

class CandlestickPattern(BaseModel):
    name: str
    detected: bool
    significance: str
    confirmation_needed: str

class ChartPattern(BaseModel):
    name: str
    detected: bool
    confidence: float
    reasoning: str

# ── Trend & Momentum ────────────────────────────────────────────

class TrendStrength(str, Enum):
    STRONG_BULLISH = "Strong Bullish"
    BULLISH = "Bullish"
    NEUTRAL = "Neutral"
    BEARISH = "Bearish"
    STRONG_BEARISH = "Strong Bearish"

class MomentumAnalysis(BaseModel):
    price_momentum: str
    volume_momentum: str
    relative_strength: str
    volatility: str
    summary: str

# ── Fundamental ─────────────────────────────────────────────────

class FundamentalMetrics(BaseModel):
    revenue_growth: Optional[str]
    profit_growth: Optional[str]
    eps: Optional[float]
    roe: Optional[float]
    roce: Optional[float]
    debt_to_equity: Optional[float]
    free_cash_flow: Optional[str]
    promoter_holding: Optional[float]
    institutional_holding: Optional[float]
    quarterly_performance: str
    annual_performance: str
    valuation_assessment: str

# ── Sentiment ───────────────────────────────────────────────────

class SentimentCategory(str, Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"

class NewsItem(BaseModel):
    title: str
    source: str
    sentiment: SentimentCategory
    impact: str

class NewsSentiment(BaseModel):
    overall: SentimentCategory
    items: List[NewsItem]
    summary: str

# ── Risk ─────────────────────────────────────────────────────────

class RiskAssessment(BaseModel):
    score: int = Field(..., ge=1, le=10)
    volatility_risk: str
    financial_risk: str
    business_risk: str
    sector_risk: str
    market_risk: str
    reasoning: str

# ── Trading Plan ───────────────────────────────────────────────

class TradingPlan(BaseModel):
    entry_zone: str
    key_support: str
    key_resistance: str
    upside_scenario: str
    downside_scenario: str
    stop_loss_area: str
    risk_reward: str
    disclaimer: str = "This is an analytical scenario, not financial advice."

# ── AI Confidence ──────────────────────────────────────────────

class AIConfidence(BaseModel):
    trend: float = Field(..., ge=0, le=1)
    technical_setup: float = Field(..., ge=0, le=1)
    fundamental_quality: float = Field(..., ge=0, le=1)
    overall: float = Field(..., ge=0, le=1)
    reasoning: str

# ── Executive Summary ──────────────────────────────────────────

class ExecutiveSummary(BaseModel):
    overall_trend: str
    strengths: List[str]
    weaknesses: List[str]
    market_sentiment: str
    short_term_outlook: str
    long_term_outlook: str
    key_risks: List[str]

# ── Full Report ────────────────────────────────────────────────

class AnalysisReport(BaseModel):
    ticker: str
    timestamp: str
    snapshot: StockSnapshot
    executive_summary: ExecutiveSummary
    technical_analysis: TechnicalAnalysis
    candlestick_patterns: List[CandlestickPattern]
    chart_patterns: List[ChartPattern]
    trend_strength: str
    momentum_analysis: MomentumAnalysis
    fundamental_analysis: FundamentalMetrics
    news_sentiment: NewsSentiment
    risk_assessment: RiskAssessment
    trading_plan: TradingPlan
    ai_confidence: AIConfidence

# ── Chat ───────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    ticker: str
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    reply: str
    context: Optional[Dict[str, Any]] = None
