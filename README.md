# AI Stock Analyzer

AI-powered stock analysis platform for the Indian stock market. Get professional-grade analysis reports in seconds.

## Features

- **Company Snapshot** — Live price, market cap, ratios, and key metrics
- **AI Executive Summary** — Overall trend, strengths, weaknesses, risks
- **Technical Analysis** — 20+ indicators (RSI, MACD, Bollinger, Supertrend, ADX, ATR, VWAP, Volume Profile, EMAs, SMAs)
- **Candlestick Pattern Detection** — Hammer, Doji, Engulfing, Morning Star, Evening Star, Harami, Marubozu
- **Chart Pattern Detection** — Triangle, Channel, Double Top, Double Bottom, Head & Shoulders, Cup & Handle
- **Trend Strength Classification** — Strong Bullish to Strong Bearish
- **Momentum Analysis** — Price, volume, relative strength, volatility
- **Fundamental Analysis** — Revenue, profit, EPS, ROE, ROCE, debt, FCF, holdings
- **News & Sentiment** — Categorized news with impact assessment
- **Risk Assessment** — Multi-factor scoring (1-10) with detailed breakdown
- **Trading Plan** — Entry zones, support/resistance, scenarios, risk:reward
- **AI Confidence Scores** — Trend, technical setup, fundamental quality
- **AI Chat** — Follow-up questions with context-aware responses

## Architecture

```
ai-stock-analyzer/
├── backend/          FastAPI + Python
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Analysis engines
│   │   └── models/         # Pydantic schemas
│   ├── requirements.txt
│   └── start.bat / start.sh
├── frontend/         Next.js 14 + React + TypeScript + Tailwind
│   ├── src/
│   │   ├── app/           # Pages
│   │   ├── components/    # UI components
│   │   ├── lib/           # API client + utils
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── start.bat / start.sh
└── design/
    └── design.md
```

## Quick Start

### Backend

```bash
cd backend

# Windows
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh
```

The backend will:
1. Create a Python virtual environment
2. Install dependencies
3. Start the FastAPI server on `http://localhost:8000`
4. Open `http://localhost:8000/docs` for interactive API docs

### Frontend

```bash
cd frontend

# Windows
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh
```

The frontend will:
1. Install npm dependencies
2. Build the static site to `dist/`
3. Start a preview server on `http://localhost:3000`

## Data Sources

- **Yahoo Finance** — Historical prices, company info, financials (via `yfinance`)
- Indian stocks use `.NS` (NSE) and `.BO` (BSE) suffixes

## Supported Stocks

The platform includes 30 top Indian stocks:
- Reliance Industries, Tata Motors, Infosys, TCS
- HDFC Bank, ICICI Bank, Axis Bank, Kotak Mahindra Bank
- Adani Enterprises, SBI, Bharti Airtel
- Larsen & Toubro, Asian Paints, Maruti Suzuki, Mahindra & Mahindra
- Sun Pharma, Wipro, HCL Technologies, Bajaj Finance
- Tata Steel, JSW Steel, UltraTech Cement, Power Grid, NTPC
- Titan, Nestle India, Hindustan Zinc, Coal India
- And more...

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stocks/search?q={query}` | Search stocks by name/ticker |
| GET | `/api/stocks/{ticker}/snapshot` | Company snapshot |
| POST | `/api/analysis/{ticker}` | Full analysis report |
| POST | `/api/chat` | AI chat follow-up |

## Technology Stack

**Backend:**
- FastAPI
- Python 3.10+
- yfinance, pandas, numpy
- Pydantic
- Uvicorn

**Frontend:**
- Next.js 14 (App Router)
- React 18 + TypeScript
- Tailwind CSS
- Lucide React icons

## Development Notes

- The backend uses mock news data for the MVP (no live news API key required)
- Chart pattern detection uses `scipy.signal.find_peaks` for local extrema
- All analysis modules are self-contained and can be tested independently
- The frontend is exported as a static site for easy deployment

## License

MIT
