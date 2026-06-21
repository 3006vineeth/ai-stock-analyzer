import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY", "")
API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY", "")

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
    {"name": "Axis Bank", "nse_symbol": "AXISBANK.NS", "bse_symbol": "AXISBANK.BO", "sector": "Financial Services", "industry": "Banking"},
    {"name": "Hindustan Unilever", "nse_symbol": "HINDUNILVR.NS", "bse_symbol": "HINDUNILVR.BO", "sector": "FMCG", "industry": "Consumer Goods"},
    {"name": "ITC", "nse_symbol": "ITC.NS", "bse_symbol": "ITC.BO", "sector": "FMCG", "industry": "Consumer Goods"},
    {"name": "Larsen & Toubro", "nse_symbol": "LT.NS", "bse_symbol": "LT.BO", "sector": "Infrastructure", "industry": "Construction"},
    {"name": "Asian Paints", "nse_symbol": "ASIANPAINT.NS", "bse_symbol": "ASIANPAINT.BO", "sector": "Materials", "industry": "Paints"},
    {"name": "Maruti Suzuki", "nse_symbol": "MARUTI.NS", "bse_symbol": "MARUTI.BO", "sector": "Automotive", "industry": "Auto Manufacturers"},
    {"name": "Mahindra & Mahindra", "nse_symbol": "M&M.NS", "bse_symbol": "M&M.BO", "sector": "Automotive", "industry": "Auto Manufacturers"},
    {"name": "Sun Pharma", "nse_symbol": "SUNPHARMA.NS", "bse_symbol": "SUNPHARMA.BO", "sector": "Healthcare", "industry": "Pharmaceuticals"},
    {"name": "Wipro", "nse_symbol": "WIPRO.NS", "bse_symbol": "WIPRO.BO", "sector": "IT", "industry": "IT Services"},
    {"name": "HCL Technologies", "nse_symbol": "HCLTECH.NS", "bse_symbol": "HCLTECH.BO", "sector": "IT", "industry": "IT Services"},
    {"name": "Bajaj Finance", "nse_symbol": "BAJFINANCE.NS", "bse_symbol": "BAJFINANCE.BO", "sector": "Financial Services", "industry": "Finance"},
    {"name": "Tata Steel", "nse_symbol": "TATASTEEL.NS", "bse_symbol": "TATASTEEL.BO", "sector": "Materials", "industry": "Steel"},
    {"name": "JSW Steel", "nse_symbol": "JSWSTEEL.NS", "bse_symbol": "JSWSTEEL.BO", "sector": "Materials", "industry": "Steel"},
    {"name": "UltraTech Cement", "nse_symbol": "ULTRACEMCO.NS", "bse_symbol": "ULTRACEMCO.BO", "sector": "Materials", "industry": "Cement"},
    {"name": "Power Grid Corp", "nse_symbol": "POWERGRID.NS", "bse_symbol": "POWERGRID.BO", "sector": "Utilities", "industry": "Power"},
    {"name": "NTPC", "nse_symbol": "NTPC.NS", "bse_symbol": "NTPC.BO", "sector": "Utilities", "industry": "Power"},
    {"name": "Titan Company", "nse_symbol": "TITAN.NS", "bse_symbol": "TITAN.BO", "sector": "Consumer", "industry": "Jewelry"},
    {"name": "Nestle India", "nse_symbol": "NESTLEIND.NS", "bse_symbol": "NESTLEIND.BO", "sector": "FMCG", "industry": "Food Products"},
    {"name": "Hindustan Zinc", "nse_symbol": "HINDZINC.NS", "bse_symbol": "HINDZINC.BO", "sector": "Materials", "industry": "Metals & Mining"},
    {"name": "Coal India", "nse_symbol": "COALINDIA.NS", "bse_symbol": "COALINDIA.BO", "sector": "Materials", "industry": "Coal"},
]
