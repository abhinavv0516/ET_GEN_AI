import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import GraphState
from src.db.vector_store import get_similar_patterns

def generate_alert(state: GraphState) -> GraphState:
    ticker = state["ticker"]
    tech = state.get("technical_signals", {})
    fund = state.get("fundamental_signals", {})
    score = state.get("scoring_result", {})
    
    conviction = score.get("conviction_score", 50)
    rating = score.get("rating", "HOLD")
    similar = get_similar_patterns(conviction)
    similar_text = "\n".join([f"- {s}" for s in similar]) if similar else "No matching historical patterns found."
    
    if not os.environ.get("GOOGLE_API_KEY"):
        return {"final_alert": f"[{rating}] {ticker} looks interesting with a conviction score of {int(conviction)}.\n\nNote: API Key missing, full alert generation skipped. Historical patterns indicate:\n{similar_text}"}

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI investment advisor for Indian retail investors. Write a plain-English, easy to understand, high-conviction alert about a stock."),
        ("user", "Ticker: {ticker}\nTechnical Signals: {tech}\nFundamental Summary: {fund}\nOverall Score: {score}/100\nRating: {rating}\nHistorical Patterns: {similar}\n\nProvide a 3-paragraph compelling alert explaining the context, why it matters, and the final recommendation.")
    ])
    
    chain = prompt | llm
    
    try:
        response = chain.invoke({
            "ticker": ticker,
            "tech": tech.get("signals", []),
            "fund": fund.get("summary", ""),
            "score": conviction,
            "rating": rating,
            "similar": similar_text
        })
        alert = response.content
    except Exception as e:
        alert = f"Alert generation failed due to API error: {str(e)}"
        
    return {"final_alert": alert}
