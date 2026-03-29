import random

def get_similar_patterns(conviction_score: float) -> list[str]:
    """
    Simulates querying ChromaDB for historical similar patterns.
    Returns 1-2 examples of similar alerts and their historical performance.
    """
    if conviction_score > 70:
        return [
            "Similar pattern on TATAMOTORS (Nov 2023) -> +12% in 2 weeks (Success)",
            "Similar pattern on HINDALCO (Feb 2024) -> +8% in 1 month (Success)"
        ]
    elif conviction_score < 30:
        return [
            "Similar pattern on PAYTM (June 2023) -> -15% in 1 month (Success Prediction)",
            "Similar pattern on YESBANK (Jan 2024) -> -8% in 2 weeks (Success Prediction)"
        ]
    else:
        return [
            "Similar pattern on ITC (Sep 2023) -> +2% in 1 month (Neutral)"
        ]
