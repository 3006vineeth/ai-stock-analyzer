# AI Stock Analyzer — Design Specification

## Overview
AI-powered stock analysis platform for Indian stock market (NSE/BSE).
Produces professional, explainable, evidence-based analysis reports.

---

## Architecture

```
ai-stock-analyzer/
├── backend/          FastAPI + Python + Pandas + NumPy
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Settings, API keys
│   │   ├── routers/
│   │   │   ├── stocks.py     # Stock search, snapshot
│   │   │   ├── analysis.py   # Full analysis report
│   │   │   └── chat.py       # AI chat follow-up
│   │   ├── services/
│   │   │   ├── data_fetcher.py      # Yahoo Finance / NSE data
│   │   │   ├── technical.py         # TA indicators, patterns
│   │   │   ├── fundamental.py     # Financial metrics
│   │   │   ├── sentiment.py       # News sentiment
│   │   │   ├── chart_patterns.py  # Pattern detection
│   │   │   ├── candlestick.py   # Candlestick patterns
│   │   │   └── ai_analyzer.py   # GPT reasoning layer
│   │   └── models/
│   │       └── schemas.py    # Pydantic models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         Next.js 14 + React + TypeScript + Tailwind CSS
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx    # Root layout with theme provider
│   │   │   ├── page.tsx      # Landing / search page
│   │   │   └── analysis/
│   │   │       └── [ticker]/page.tsx   # Analysis report page
│   │   ├── components/
│   │   │   ├── SearchBar.tsx
│   │   │   ├── CompanySnapshot.tsx
│   │   │   ├── ExecutiveSummary.tsx
│   │   │   ├── TechnicalAnalysis.tsx
│   │   │   ├── CandlestickPatterns.tsx
│   │   │   ├── ChartPatterns.tsx
│   │   │   ├── TrendStrength.tsx
│   │   │   ├── MomentumAnalysis.tsx
│   │   │   ├── FundamentalAnalysis.tsx
│   │   │   ├── NewsSentiment.tsx
│   │   │   ├── RiskAssessment.tsx
│   │   │   ├── TradingPlan.tsx
│   │   │   ├── AIConfidence.tsx
│   │   │   ├── StockChart.tsx
│   │   │   └── AIChat.tsx
│   │   ├── lib/
│   │   │   ├── api.ts        # API client
│   │   │   └── utils.ts      # Helpers
│   │   └── types/
│   │       └── index.ts      # TypeScript interfaces
│   ├── package.json
│   └── tailwind.config.ts
└── README.md
```

---

## Backend API Contract

### GET /api/stocks/search?q={query}
Search stocks by name or ticker. Returns array of matches.

```json
{
  "results": [
    { "name": "Reliance Industries", "nse_symbol": "RELIANCE.NS", "bse_symbol": "RELIANCE.BO", "sector": "Energy", "industry": "Oil & Gas" }
  ]
}
```

### GET /api/stocks/{ticker}/snapshot
Company snapshot with basic metrics.

```json
{
  "name": "Reliance Industries",
  "nse_symbol": "RELIANCE.NS",
  "current_price": 2874.50,
  "change": 12.30,
  "change_percent": 0.43,
  "market_cap": "19.4T INR",
  "sector": "Energy",
  "industry": "Oil & Gas",
  "pe_ratio": 24.5,
  "pb_ratio": 2.3,
  "dividend_yield": 0.35,
  "week_52_high": 3210.00,
  "week_52_low": 2200.00,
  "avg_volume": 8500000
}
```

### POST /api/analysis/{ticker}
Generate full analysis report.

```json
{
  "ticker": "RELIANCE.NS",
  "report": {
    "executive_summary": "...",
    "technical_analysis": { ... },
    "candlestick_patterns": [...],
    "chart_patterns": [...],
    "trend_strength": "Bullish",
    "momentum_analysis": { ... },
    "fundamental_analysis": { ... },
    "news_sentiment": { ... },
    "risk_assessment": { "score": 5, "reasoning": "..." },
    "trading_plan": { ... },
    "ai_confidence": { ... }
  }
}
```

### POST /api/chat
Follow-up chat with analysis context.

```json
{ "ticker": "RELIANCE.NS", "message": "Why is RSI important?" }
```

---

## Data Sources
- **Yahoo Finance** (via plugin): prices, historical data, financials (`.NS` / `.BO` suffixes)
- **NSE India** (web scraping fallback): stock list, company info
- **News API**: sentiment analysis

---

## Technical Analysis Stack
- `yfinance` for data fetching
- `pandas`, `numpy` for computation
- Custom implementations for: EMA, SMA, RSI, MACD, Bollinger Bands, Supertrend, ADX, ATR, VWAP, Volume Profile
- Pattern detection algorithms for candlestick and chart patterns

---

## AI Layer
- GPT-4o / GPT-4o-mini for reasoning and report generation
- Structured JSON output with explanations
- Chat maintains context of the analysis report

---

## Frontend Design

### Theme
- Dark mode default (professional trading aesthetic)
- Colors: Slate-900 bg, Slate-100 text, Emerald-500 bullish, Rose-500 bearish
- Accent: Indigo-500 for AI highlights
- Cards with subtle borders, glass-morphism on overlay elements

### Pages
1. **Home**: Search bar centered, trending stocks, recent analyses
2. **Analysis Dashboard**: Full report with expandable cards, TradingView chart, chat panel

### Key Components
- StockChart: Lightweight Charts by TradingView (or custom with lightweight-charts library)
- AIChat: Chat panel with markdown support, typing indicator
- Analysis Cards: Expandable sections with confidence badges

---

## Stock Ticker Mapping (Indian Market)
| Company | NSE | BSE |
|---------|-----|-----|
| Reliance Industries | RELIANCE.NS | RELIANCE.BO |
| Tata Motors | TATAMOTORS.NS | TATAMOTORS.BO |
| Infosys | INFY.NS | INFY.BO |
| HDFC Bank | HDFCBANK.NS | HDFCBANK.BO |
| ICICI Bank | ICICIBANK.NS | ICICIBANK.BO |
| TCS | TCS.NS | TCS.BO |
| Adani Enterprises | ADANIENT.NS | ADANIENT.BO |
| State Bank of India | SBIN.NS | SBIN.BO |
| Bharti Airtel | BHARTIARTL.NS | BHARTIARTL.BO |
| Kotak Mahindra Bank | KOTAKBANK.NS | KOTAKBANK.BO |

