from fastapi import APIRouter, HTTPException, Query
print("LOADED STOCKS ROUTER")
from typing import List, Optional
print("LOADED STOCKS ROUTER")
from app.models.schemas import StockSearchResponse, StockSearchResult, StockSnapshot
print("LOADED STOCKS ROUTER")
from app.config import INDIAN_STOCKS
print("LOADED STOCKS ROUTER")
from app.services.twelve_data_service import TwelveDataService
print("LOADED STOCKS ROUTER")

router = APIRouter(prefix="/stocks", tags=["stocks"])
service = TwelveDataService()

@router.get("/search", response_model=StockSearchResponse)
async def search_stocks(q: str = Query(..., min_length=1, description="Stock name or ticker to search")):
    """Search for stocks by name or ticker symbol."""
    q_lower = q.lower()
    results = []
    
    for stock in INDIAN_STOCKS:
        if q_lower in stock["name"].lower() or q_lower in stock["nse_symbol"].lower() or q_lower in stock["bse_symbol"].lower():
            results.append(StockSearchResult(**stock))
    
    # Augment with Twelve Data symbol search for Indian exchanges
    try:
        td_results = await service.search_stock(q)
        if td_results and "data" in td_results:
            for item in td_results["data"]:
                sym = item.get("symbol", "")
                if sym.endswith(".NS") or sym.endswith(".BO"):
                    if not any(r.nse_symbol == sym for r in results):
                        results.append(StockSearchResult(
                            name=item.get("instrument_name", sym),
                            nse_symbol=sym,
                            bse_symbol=sym.replace(".NS", ".BO") if sym.endswith(".NS") else sym,
                            sector=item.get("sector", "N/A"),
                            industry=item.get("industry", "N/A")
                        ))
    except Exception:
        # Do not let external search failure break local search
        pass
    
    return StockSearchResponse(results=results)


@router.get("/{ticker}/snapshot", response_model=StockSnapshot)
async def get_snapshot(ticker: str):

    print("="*60)
    print("ROUTE CALLED:", ticker)

    if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
        ticker += ".NS"

    print("Calling service...")

    snapshot = await service.get_snapshot(ticker)

    print("SERVICE RETURNED:")
    print(snapshot)

    print("TYPE:", type(snapshot))

    print("Creating StockSnapshot model...")

    model = StockSnapshot(**snapshot)

    print("MODEL CREATED SUCCESSFULLY")

    return model