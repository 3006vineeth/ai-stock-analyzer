import pandas as pd
from typing import Dict, Any, Optional
from app.services.twelve_data_service import TwelveDataService

class FundamentalAnalyzer:
    def __init__(self, symbol: str, info: Dict[str, Any]):
        self.symbol = symbol
        self.info = info
        self.fetcher = TwelveDataService()
    
    async def analyze(self):
        info = self.info
        financials = await self.fetcher.get_financials(self.symbol)
        holders = await self.fetcher.get_holders(self.symbol)
        
        # Revenue growth calculation
        revenue = financials.get("revenue", {})
        revenue_growth = None
        if revenue and len(revenue) >= 2:
            years = sorted(revenue.keys(), reverse=True)
            if len(years) >= 2 and revenue[years[1]] and revenue[years[1]] != 0:
                growth = ((revenue[years[0]] - revenue[years[1]]) / abs(revenue[years[1]])) * 100
                revenue_growth = f"{growth:.1f}%"
        
        # Profit growth
        profit = financials.get("profit", {})
        profit_growth = None
        if profit and len(profit) >= 2:
            years = sorted(profit.keys(), reverse=True)
            if len(years) >= 2 and profit[years[1]] and profit[years[1]] != 0:
                growth = ((profit[years[0]] - profit[years[1]]) / abs(profit[years[1]])) * 100
                profit_growth = f"{growth:.1f}%"
        
        # EPS
        eps = financials.get("eps", {})
        latest_eps = None
        if eps:
            years = sorted(eps.keys(), reverse=True)
            if years:
                latest_eps = eps[years[0]]
        
        # ROE
        roe = info.get("returnOnEquity")
        if roe:
            roe = round(roe * 100, 2)
        
        # ROCE (approximate from ROE or calculate)
        roce = info.get("returnOnAssets")
        if roce:
            roce = round(roce * 100, 2)
        
        # Debt to equity
        debt_to_equity = info.get("debtToEquity")
        if debt_to_equity:
            debt_to_equity = round(debt_to_equity / 100, 2)  # Yahoo returns as percentage
        
        # Free cash flow
        fcf = financials.get("free_cash_flow", {})
        fcf_str = None
        if fcf:
            years = sorted(fcf.keys(), reverse=True)
            if years and fcf[years[0]]:
                val = fcf[years[0]]
                fcf_str = f"{val/1e9:.2f}B INR" if abs(val) >= 1e9 else f"{val/1e6:.2f}M INR"
        
        # Holdings
        promoter_holding = info.get("heldPercentInsiders")
        if promoter_holding:
            promoter_holding = round(promoter_holding * 100, 2)
        
        institutional_holding = info.get("heldPercentInstitutions")
        if institutional_holding:
            institutional_holding = round(institutional_holding * 100, 2)
        
        # Quarterly performance
        q_rev = financials.get("quarterly_revenue", {})
        q_profit = financials.get("quarterly_profit", {})
        quarterly_perf = "Data unavailable"
        if q_rev and len(q_rev) >= 2:
            q_years = sorted(q_rev.keys(), reverse=True)
            if len(q_years) >= 2:
                q_growth = ((q_rev[q_years[0]] - q_rev[q_years[1]]) / abs(q_rev[q_years[1]])) * 100 if q_rev[q_years[1]] else 0
                quarterly_perf = f"Revenue {'up' if q_growth > 0 else 'down'} {abs(q_growth):.1f}% QoQ"
        
        # Annual performance
        annual_perf = "Data unavailable"
        if revenue and len(revenue) >= 2:
            years = sorted(revenue.keys(), reverse=True)
            if len(years) >= 2:
                a_growth = ((revenue[years[0]] - revenue[years[1]]) / abs(revenue[years[1]])) * 100 if revenue[years[1]] else 0
                annual_perf = f"Revenue {'growing' if a_growth > 0 else 'declining'} at {abs(a_growth):.1f}% YoY"
        
        # Valuation assessment
        pe = info.get("trailingPE")
        pb = info.get("priceToBook")
        valuation = ""
        if pe and pb:
            if pe < 15 and pb < 3:
                valuation = "Appears undervalued relative to peers"
            elif pe > 30 or pb > 5:
                valuation = "Appears richly valued; premium pricing"
            else:
                valuation = "Fairly valued within typical market ranges"
        else:
            valuation = "Insufficient data for valuation assessment"
        
        return {
            "revenue_growth": revenue_growth,
            "profit_growth": profit_growth,
            "eps": latest_eps,
            "roe": roe,
            "roce": roce,
            "debt_to_equity": debt_to_equity,
            "free_cash_flow": fcf_str,
            "promoter_holding": promoter_holding,
            "institutional_holding": institutional_holding,
            "quarterly_performance": quarterly_perf,
            "annual_performance": annual_perf,
            "valuation_assessment": valuation,
        }
