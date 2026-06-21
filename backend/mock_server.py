import json
from datetime import datetime, timedelta
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Stock Analyzer - Mock Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INDIAN_STOCKS = [
    {"name": "Reliance Industries", "nse_symbol": "RELIANCE.NS", "bse_symbol": "RELIANCE.BO", "sector": "Energy", "industry": "Oil & Gas"},
    {"name": "Tata Motors", "nse_symbol": "TATAMOTORS.NS", "bse_symbol": "TATAMOTORS.BO", "sector": "Automotive", "industry": "Auto Manufacturers"},
    {"name": "Infosys", "nse_symbol": "INFY.NS", "bse_symbol": "INFY.BO", "sector": "IT", "industry": "IT Services"},
    {"name": "HDFC Bank", "nse_symbol": "HDFCBANK.NS", "bse_symbol": "HDFCBANK.BO", "sector": "Financial Services", "industry": "Banking"},
    {"name": "ICICI Bank", "nse_symbol": "ICICIBANK.NS", "bse_symbol": "ICICIBANK.BO", "sector": "Financial Services", "industry": "Banking"},
    {"name": "Tata Consultancy Services", "nse_symbol": "TCS.NS", "bse_symbol": "TCS.BO", "sector": "IT", "industry": "IT Services"},
    {"name": "Adani Enterprises", "nse_symbol": "ADANIENT.NS", "bse_symbol": "ADANIENT.BO", "sector": "Conglomerate", "industry": "Diversified"},
    {"name": "State Bank of India", "nse_symbol": "SBIN.NS", "bse_symbol": "SBIN.BO", "sector": "Financial Services", "industry": "Banking"},
    {"name": "Bharti Airtel", "nse_symbol": "BHARTIARTL.NS", "bse_symbol": "BHARTIARTL.BO", "sector": "Telecom", "industry": "Telecommunications"},
    {"name": "Kotak Mahindra Bank", "nse_symbol": "KOTAKBANK.NS", "bse_symbol": "KOTAKBANK.BO", "sector": "Financial Services", "industry": "Banking"},
]

@app.get("/api/stocks/search")
async def search_stocks(q: str):
    q_lower = q.lower()
    results = [s for s in INDIAN_STOCKS if q_lower in s["name"].lower() or q_lower in s["nse_symbol"].lower()]
    return {"results": results}

@app.get("/api/stocks/{ticker}/snapshot")
async def get_snapshot(ticker: str):
    stock = next((s for s in INDIAN_STOCKS if s["nse_symbol"] == ticker or s["bse_symbol"] == ticker), None)
    if not stock:
        stock = INDIAN_STOCKS[0]
    return {
        "name": stock["name"],
        "nse_symbol": stock["nse_symbol"],
        "current_price": round(random.uniform(500, 3000), 2),
        "change": round(random.uniform(-50, 50), 2),
        "change_percent": round(random.uniform(-3, 3), 2),
        "market_cap": f"{random.uniform(1, 20):.1f}T INR",
        "sector": stock["sector"],
        "industry": stock["industry"],
        "pe_ratio": round(random.uniform(15, 40), 2),
        "pb_ratio": round(random.uniform(1.5, 5), 2),
        "dividend_yield": round(random.uniform(0.1, 2.5), 2),
        "week_52_high": round(random.uniform(3000, 4000), 2),
        "week_52_low": round(random.uniform(400, 900), 2),
        "avg_volume": random.randint(5000000, 15000000),
    }

@app.post("/api/analysis/{ticker}")
async def analyze_stock(ticker: str):
    stock = next((s for s in INDIAN_STOCKS if s["nse_symbol"] == ticker or s["bse_symbol"] == ticker), INDIAN_STOCKS[0])
    price = round(random.uniform(500, 3000), 2)
    
    return {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "executive_summary": {
            "overall_trend": f"{stock['name']} is currently in a bullish phase with strong momentum above key moving averages.",
            "strengths": ["Strong revenue growth", "Healthy balance sheet", "Positive sector outlook"],
            "weaknesses": ["High valuation multiples", "Sector concentration risk"],
            "market_sentiment": "Positive",
            "short_term_outlook": "Consolidation expected with support at lower levels",
            "long_term_outlook": "Favorable given structural growth drivers",
            "key_risks": ["Market volatility", "Regulatory changes", "Competition intensity"]
        },
        "technical_analysis": {
            "trend": "Uptrend",
            "support_levels": [round(price * 0.95, 2), round(price * 0.90, 2)],
            "resistance_levels": [round(price * 1.05, 2), round(price * 1.10, 2)],
            "indicators": [
                {"name": "RSI (14)", "value": round(random.uniform(40, 65), 2), "signal": "Neutral", "explanation": "RSI in neutral zone suggesting balanced momentum"},
                {"name": "MACD", "value": {"macd": 2.5, "signal": 1.8, "histogram": 0.7, "trend": "Bullish"}, "signal": "Bullish", "explanation": "MACD line above signal line"},
                {"name": "Bollinger Bands", "value": {"upper": round(price * 1.08, 2), "middle": price, "lower": round(price * 0.92, 2), "position": "Within Bands", "bandwidth": 8.5}, "signal": "Within Bands", "explanation": "Price trading within normal bands"},
                {"name": "EMA 20", "value": round(price * 0.98, 2), "signal": "Above Price", "explanation": "Price above EMA 20 indicating short-term strength"},
                {"name": "EMA 50", "value": round(price * 0.95, 2), "signal": "Above Price", "explanation": "Price above EMA 50 indicating medium-term strength"},
            ],
            "summary": "Overall technical picture is bullish with price above key moving averages and MACD confirming positive momentum."
        },
        "candlestick_patterns": [
            {"name": "Hammer", "detected": random.choice([True, False]), "significance": "Bullish reversal at support", "confirmation_needed": "Wait for next candle"},
            {"name": "Doji", "detected": random.choice([True, False]), "significance": "Indecision", "confirmation_needed": "Wait for breakout"},
            {"name": "Engulfing", "detected": random.choice([True, False]), "significance": "Bullish engulfing", "confirmation_needed": "Volume confirmation"},
            {"name": "Morning Star", "detected": False, "significance": "Strong bullish reversal", "confirmation_needed": "Close above first candle"},
            {"name": "Evening Star", "detected": False, "significance": "Strong bearish reversal", "confirmation_needed": "Close below first candle"},
            {"name": "Harami", "detected": random.choice([True, False]), "significance": "Potential reversal", "confirmation_needed": "Breakout"},
            {"name": "Marubozu", "detected": random.choice([True, False]), "significance": "Strong directional move", "confirmation_needed": "Watch for continuation"},
            {"name": "Shooting Star", "detected": False, "significance": "Bearish reversal at resistance", "confirmation_needed": "Close below low"},
        ],
        "chart_patterns": [
            {"name": "Triangle", "detected": random.choice([True, False]), "confidence": 0.6, "reasoning": "Converging trendlines"},
            {"name": "Channel", "detected": random.choice([True, False]), "confidence": 0.65, "reasoning": "Parallel trendlines"},
            {"name": "Double Top", "detected": False, "confidence": 0, "reasoning": "No matching formation"},
            {"name": "Double Bottom", "detected": random.choice([True, False]), "confidence": 0.7, "reasoning": "Two troughs at similar levels"},
            {"name": "Head and Shoulders", "detected": False, "confidence": 0, "reasoning": "No formation"},
            {"name": "Cup and Handle", "detected": False, "confidence": 0, "reasoning": "No pattern"},
        ],
        "trend_strength": random.choice(["Strong Bullish", "Bullish", "Neutral"]),
        "momentum_analysis": {
            "price_momentum": "Positive — recent upward momentum",
            "volume_momentum": "Moderately elevated — increasing interest",
            "relative_strength": "Stock has gained 5.2% over 20 days",
            "volatility": "Moderate — normal market fluctuations",
            "summary": "Price and volume momentum align positively, supporting the current uptrend."
        },
        "fundamental_analysis": {
            "revenue_growth": "12.5%",
            "profit_growth": "8.3%",
            "eps": 45.2,
            "roe": 18.5,
            "roce": 16.2,
            "debt_to_equity": 0.8,
            "free_cash_flow": "1.2B INR",
            "promoter_holding": 52.3,
            "institutional_holding": 28.5,
            "quarterly_performance": "Revenue up 5.2% QoQ",
            "annual_performance": "Revenue growing at 12.5% YoY",
            "valuation_assessment": "Fairly valued within typical market ranges"
        },
        "news_sentiment": {
            "overall": random.choice(["Positive", "Neutral"]),
            "items": [
                {"title": f"{stock['name']} reports strong Q3 earnings", "source": "Financial News", "sentiment": "Positive", "impact": "Likely positive price impact"},
                {"title": f"{stock['name']} announces expansion", "source": "Business Today", "sentiment": "Positive", "impact": "Growth catalyst"},
                {"title": "Sector outlook remains stable", "source": "Economic Times", "sentiment": "Neutral", "impact": "Minimal immediate impact"},
            ],
            "summary": "News flow is predominantly positive with 2 positive and 1 neutral items."
        },
        "risk_assessment": {
            "score": random.randint(3, 7),
            "volatility_risk": "Moderate — daily swings between 2.5-5%",
            "financial_risk": "Low — manageable debt levels",
            "business_risk": "Moderate — sector-dependent risks",
            "sector_risk": "IT sector faces typical industry risks",
            "market_risk": "Moderate — beta of 1.1 tracks market closely",
            "reasoning": "Risk score based on volatility, leverage, and market sensitivity."
        },
        "trading_plan": {
            "entry_zone": f"{round(price * 0.98, 2)} - {round(price * 1.02, 2)}",
            "key_support": str(round(price * 0.95, 2)),
            "key_resistance": str(round(price * 1.05, 2)),
            "upside_scenario": f"Target: {round(price * 1.1, 2)} (+10%)",
            "downside_scenario": f"Target: {round(price * 0.9, 2)} (-10%)",
            "stop_loss_area": f"{round(price * 0.93, 2)} (7% below entry)",
            "risk_reward": "1:2 to 1:3",
            "disclaimer": "This is an analytical scenario, not financial advice."
        },
        "ai_confidence": {
            "trend": round(random.uniform(0.65, 0.85), 2),
            "technical_setup": round(random.uniform(0.6, 0.8), 2),
            "fundamental_quality": round(random.uniform(0.55, 0.75), 2),
            "overall": round(random.uniform(0.6, 0.8), 2),
            "reasoning": "Confidence based on indicator alignment, pattern clarity, and financial metrics."
        }
    }

@app.post("/api/chat")
async def chat(request: dict):
    message = request.get("message", "").lower()
    ticker = request.get("ticker", "")
    
    if "rsi" in message:
        reply = f"RSI for {ticker} measures momentum. Above 70 = overbought, below 30 = oversold. It helps identify potential reversals."
    elif "support" in message:
        reply = f"Support levels for {ticker} are price zones where buying interest overcomes selling pressure."
    elif "risk" in message:
        reply = f"Main risks for {ticker} include market volatility, sector competition, and regulatory changes."
    else:
        reply = f"I can help with questions about {ticker}'s technical setup, fundamentals, risks, or trading scenarios. What would you like to know?"
    
    return {"reply": reply, "context": {"ticker": ticker}}

@app.get("/")
async def root():
    return {"message": "AI Stock Analyzer Mock Server", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
