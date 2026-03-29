import math
from src.state import GraphState

def score_signals(state: GraphState) -> GraphState:
    tech = state.get("technical_signals", {})
    fund = state.get("fundamental_signals", {})
    
    tech_score = tech.get("bullish_score", 0) # e.g. -4 to +4
    fund_score = fund.get("sentiment_score", 0) # e.g. -10 to +10
    
    # Normalize to -50 to +50 each
    tech_normalized = max(-50, min(50, (math.copysign(1, tech_score) * min(abs(tech_score), 4) / 4.0) * 50 if tech_score else 0))
    fund_normalized = fund_score * 5.0
    
    combined = 50 + (tech_normalized + fund_normalized) / 2
    conviction_score = max(0, min(100, combined))
    
    # Determine rating
    if conviction_score > 75:
        rating = "STRONG BUY"
    elif conviction_score > 60:
        rating = "BUY"
    elif conviction_score < 25:
        rating = "STRONG SELL"
    elif conviction_score < 40:
        rating = "SELL"
    else:
        rating = "HOLD"
        
    return {
        "scoring_result": {
            "conviction_score": conviction_score,
            "rating": rating,
            "tech_normalized": tech_normalized,
            "fund_normalized": fund_normalized
        }
    }
