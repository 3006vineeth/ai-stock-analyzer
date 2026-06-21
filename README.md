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

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/3006vineeth/ai-stock-analyzer.git
cd ai-stock-analyzer
```

---

## 2. Get a Free Twelve Data API Key

1. Visit https://twelvedata.com
2. Create a free account.
3. Copy your API key from the dashboard.

---

## 3. Configure Environment Variables

Copy the example environment file.

### Windows (PowerShell)

```powershell
Copy-Item .env.example .env
```

### Linux / macOS

```bash
cp .env.example .env
```

Open the `.env` file and replace:

```env
TWELVEDATA_API_KEY=YOUR_TWELVEDATA_API_KEY
```

with

```env
TWELVEDATA_API_KEY=your_actual_api_key
```

---

## 4. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## 5. Start the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API:

```
http://localhost:8000
```

Swagger API Documentation:

```
http://localhost:8000/docs
```

---

## 6. Install Frontend Dependencies

Open a new terminal.

```bash
cd frontend
npm install
```

---

## 7. Start the Frontend

```bash
npm run dev
```

Frontend:

```
http://localhost:3000
```

---

# 📡 API Endpoints

### Search Stocks

```http
GET /api/stocks/search?q=TCS
```

---

### Company Snapshot

```http
GET /api/stocks/TCS.NS/snapshot
```

---

### AI Stock Analysis

```http
POST /api/analysis/TCS.NS
```

---

### AI Chat

```http
POST /api/chat
```

---

# 🏗 Architecture

| Layer | Previous | Current |
|--------|----------|----------|
| Market Data | yfinance | Twelve Data REST API |
| Data Service | DataFetcher | TwelveDataService |
| HTTP Client | requests | httpx.AsyncClient |
| Backend | FastAPI | FastAPI |
| Frontend | Next.js | Next.js + TypeScript |
| Technical Analysis | Pandas | Pandas |
| Caching | Basic Dictionary | TTL Cache |
| Error Handling | Basic Exceptions | Structured Logging + HTTPException |
| Historical Data | yfinance | Twelve Data → yfinance-compatible DataFrame |

---

# 📊 Features

- 🔍 Indian Stock Search
- 📈 Real-time Company Snapshot
- 📉 Technical Analysis
- 🕯 Candlestick Pattern Detection
- 📊 Chart Pattern Recognition
- 📈 Trend & Momentum Analysis
- 💰 Fundamental Analysis
- 📰 AI-powered News Sentiment
- ⚠ Risk Assessment
- 🎯 AI-generated Trading Plan
- 🤖 AI Confidence Score
- 💬 Interactive AI Chat Assistant

---

# ⚙ Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

## Backend

- FastAPI
- Pandas
- NumPy
- HTTPX
- Twelve Data API

---

# 📁 Project Structure

```text
ai-stock-analyzer/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── start.bat
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── design/
├── .env.example
├── .gitignore
└── README.md
```

---

# 📝 Notes

- Uses the **Twelve Data REST API** as the market data provider.
- Historical market data is converted into a **yfinance-compatible DataFrame**, allowing all existing technical analysis modules to work without modification.
- Implements **TTL-based caching** to reduce API requests and improve response times.
- Designed specifically for **Indian stock market analysis** with support for NSE-listed stocks.
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
