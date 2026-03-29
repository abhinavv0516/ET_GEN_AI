import yfinance as yf
from src.state import GraphState

def ingest_market_data(state: GraphState) -> GraphState:
    """
    LangGraph node exactly for fetching multi-modal market data.
    """
    ticker_symbol = state["ticker"]
    stock = yf.Ticker(ticker_symbol)
    
    # Get last 1 year of daily data
    hist = stock.history(period="1y")
    
    # Get basic info
    try:
        info = stock.info
    except Exception:
        info = {}
    
    # Get recent news
    try:
        raw_news = stock.news
    except Exception:
        raw_news = []
        
    news = []
    for item in raw_news:
        # yf news contains keys like 'title', 'link', 'publisher', 'relatedTickers'
        news.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "publisher": item.get("publisher", ""),
            "uuid": item.get("uuid", "")
        })
    
    raw_data = {
        "history": hist, # Pandas DataFrame
        "info": info
    }
    
    return {"raw_data": raw_data, "news": news}
