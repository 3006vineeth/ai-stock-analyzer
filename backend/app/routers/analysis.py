from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalysisReport
from app.services.ai_analyzer import AIAnalyzer

router = APIRouter(prefix="/analysis", tags=["analysis"])
analyzer = AIAnalyzer()

@router.post("/{ticker}", response_model=AnalysisReport)
async def analyze_stock(ticker: str):
    """Generate full AI analysis report for a stock."""
    try:
        # Ensure .NS suffix if not provided
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
            ticker = ticker + ".NS"
        
        print("="*80)
        print("ANALYSIS STARTED")
        print("Ticker:", ticker)

        report = await analyzer.generate_report(ticker)

        print("REPORT GENERATED")
        print(report)

        return report
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )