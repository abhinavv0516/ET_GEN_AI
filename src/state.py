from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage

class GraphState(TypedDict):
    """
    Represents the state of our investment intelligence pipeline.
    """
    ticker: str
    raw_data: Dict[str, Any]  # Store history and info from yfinance
    news: List[Dict[str, str]] # List of news articles [{title, link, publisher, relatedTickers}]
    technical_signals: Dict[str, Any] # Indicators & pattern results
    fundamental_signals: Dict[str, Any] # Sentiment and fundamental impact
    scoring_result: Dict[str, Any] # Combined scoring
    final_alert: str # Plain-english alert message
    messages: List[BaseMessage] # Optionally track LLM steps/thinking
