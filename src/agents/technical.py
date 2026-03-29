import pandas as pd
import ta
from src.state import GraphState

def technical_analysis(state: GraphState) -> GraphState:
    df = state["raw_data"].get("history")
    
    if df is None or df.empty:
        return {"technical_signals": {"error": "No historical data available"}}
        
    df = df.copy()
    
    # Calculate simple moving averages
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
    
    # Calculate RSI
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    # Get the latest values
    latest = df.iloc[-1]
    
    # Simple logic to determine trend
    price = latest['Close']
    sma50 = latest['SMA_50']
    sma200 = latest['SMA_200']
    rsi = latest['RSI']
    
    signals = []
    bullish_score = 0
    
    if pd.notna(sma50) and pd.notna(sma200):
        if sma50 > sma200:
            signals.append("Golden Cross (SMA 50 > SMA 200)")
            bullish_score += 1
        elif sma50 < sma200:
            signals.append("Death Cross (SMA 50 < SMA 200)")
            bullish_score -= 1
            
        if price > sma50:
            signals.append("Price above 50-day SMA")
            bullish_score += 1
        else:
            signals.append("Price below 50-day SMA")
            bullish_score -= 1
            
    if pd.notna(rsi):
        if rsi < 30:
            signals.append(f"Oversold (RSI: {rsi:.2f})")
            bullish_score += 2
        elif rsi > 70:
            signals.append(f"Overbought (RSI: {rsi:.2f})")
            bullish_score -= 2
        else:
            signals.append(f"Neutral RSI: {rsi:.2f}")
            
    return {
        "technical_signals": {
            "bullish_score": bullish_score,
            "signals": signals,
            "latest_price": float(price)
        }
    }
