import requests
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from app.models.schemas import NewsItem, NewsSentiment, SentimentCategory

class SentimentAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def _mock_news(self, ticker: str, company_name: str) -> List[Dict[str, Any]]:
        """Generate mock news when no real API is available."""
        base_name = company_name.split()[0] if company_name else ticker
        
        positive_templates = [
            f"{base_name} reports strong Q3 earnings, beats estimates by 8%",
            f"{base_name} announces expansion into new markets",
            f"{base_name} receives analyst upgrade from major brokerage",
            f"{base_name} secures major government contract worth 500 Cr",
            f"{base_name} debt reduction plan on track, Moody's positive",
        ]
        
        neutral_templates = [
            f"{base_name} maintains guidance for FY2024-25",
            f"{base_name} board meeting scheduled next week",
            f"{base_name} trading volume higher than average today",
            f"Sector outlook for {base_name}'s industry remains stable",
            f"{base_name} announces dividend declaration date",
        ]
        
        negative_templates = [
            f"{base_name} faces margin pressure from rising input costs",
            f"{base_name} underperforms sector peers in Q3",
            f"Foreign investors reduce stake in {base_name}",
            f"Regulatory scrutiny increases for {base_name}'s sector",
            f"{base_name} misses revenue target by 3%",
        ]
        
        news = []
        for i in range(2):
            news.append({"title": random.choice(positive_templates), "sentiment": "Positive"})
        for i in range(2):
            news.append({"title": random.choice(neutral_templates), "sentiment": "Neutral"})
        for i in range(1):
            news.append({"title": random.choice(negative_templates), "sentiment": "Negative"})
        
        random.shuffle(news)
        return news[:5]
    
    def analyze(self, ticker: str, company_name: str = "") -> NewsSentiment:
        raw_news = self._mock_news(ticker, company_name)
        
        items = []
        pos_count = 0
        neg_count = 0
        neu_count = 0
        
        for item in raw_news:
            sentiment = item["sentiment"]
            if sentiment == "Positive":
                pos_count += 1
                cat = SentimentCategory.POSITIVE
                impact = "Likely positive price impact in short term"
            elif sentiment == "Negative":
                neg_count += 1
                cat = SentimentCategory.NEGATIVE
                impact = "Could create selling pressure"
            else:
                neu_count += 1
                cat = SentimentCategory.NEUTRAL
                impact = "Minimal immediate impact expected"
            
            items.append(NewsItem(
                title=item["title"],
                source="Financial News",
                sentiment=cat,
                impact=impact
            ))
        
        # Overall sentiment
        if pos_count > neg_count:
            overall = SentimentCategory.POSITIVE
            summary = f"News flow is predominantly positive ({pos_count} positive, {neg_count} negative, {neu_count} neutral)."
        elif neg_count > pos_count:
            overall = SentimentCategory.NEGATIVE
            summary = f"News flow has negative tilt ({pos_count} positive, {neg_count} negative, {neu_count} neutral)."
        else:
            overall = SentimentCategory.NEUTRAL
            summary = f"News flow is balanced ({pos_count} positive, {neg_count} negative, {neu_count} neutral)."
        
        return NewsSentiment(
            overall=overall,
            items=items,
            summary=summary
        )
