from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle follow-up chat questions about stock analysis."""
    try:
        # Simple rule-based responses for MVP
        message = request.message.lower()
        ticker = request.ticker
        
        if "rsi" in message:
            reply = f"RSI (Relative Strength Index) for {ticker} measures momentum on a scale of 0-100. Above 70 suggests overbought conditions, below 30 suggests oversold. It's important because it helps identify when a stock might be due for a reversal."
        elif "support" in message:
            reply = f"Support levels for {ticker} are price zones where buying interest has historically been strong enough to overcome selling pressure. They're identified by looking at previous price lows where the stock bounced back."
        elif "compare" in message:
            reply = f"To compare {ticker} with another stock, I'd need to analyze both on the same metrics: trend strength, valuation multiples, growth rates, and risk scores. Would you like me to analyze a specific stock for comparison?"
        elif "risk" in message:
            reply = f"The main risks for {ticker} include market volatility, sector-specific challenges, and any financial leverage. The risk assessment in the report breaks this down into volatility, financial, business, sector, and market risk components."
        elif "swing" in message or "trading" in message:
            reply = f"Based on the analysis, {ticker}'s suitability for swing trading depends on its volatility and trend clarity. The technical setup and trading plan section outlines key entry, exit, and stop-loss levels for swing trading considerations."
        elif "watch" in message or "next" in message:
            reply = f"Over the next few days, watch how {ticker} reacts at the key support and resistance levels identified in the technical analysis. Also monitor any news flow and volume changes for confirmation of the current trend."
        else:
            reply = f"I understand your question about {ticker}. The analysis report above contains detailed information on the technical setup, fundamentals, and risk factors. For more specific insights, feel free to ask about RSI, support levels, risk assessment, or trading scenarios."
        
        return ChatResponse(reply=reply, context={"ticker": ticker})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
