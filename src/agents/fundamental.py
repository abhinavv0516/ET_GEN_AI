import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.state import GraphState

def analyze_fundamentals(state: GraphState) -> GraphState:
    news = state.get("news", [])
    ticker_info = state["raw_data"].get("info", {})
    
    # Check if GOOGLE_API_KEY is set
    if not os.environ.get("GOOGLE_API_KEY"):
        return {"fundamental_signals": {"summary": "API Key missing, fundamental analysis skipped.", "sentiment_score": 0}}

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert financial analyst. Analyze the following news and company info to determine the fundamental outlook. Output a JSON object with 'summary' (str) and 'sentiment_score' (int from -10 to 10)."),
        ("user", "Company Info: {info}\nRecent News: {news}")
    ])
    
    structured_llm = llm.with_structured_output(
        schema={
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Brief summary of fundamental and news sentiment."},
                "sentiment_score": {"type": "integer", "description": "Score from -10 (very negative) to 10 (very positive)."}
            },
            "required": ["summary", "sentiment_score"]
        }
    )
    
    chain = prompt | structured_llm
    
    try:
        if not news and not ticker_info:
            result = {"summary": "No fundamental data available.", "sentiment_score": 0}
        else:
            news_text = "\n".join([f"- {n.get('title', '')} ({n.get('publisher', '')})" for n in news[:5]])
            info_text = f"Sector: {ticker_info.get('sector')}, Industry: {ticker_info.get('industry')}, Market Cap: {ticker_info.get('marketCap')}"
            
            result = chain.invoke({"info": info_text, "news": news_text})
    except Exception as e:
        result = {"summary": f"Error analyzing fundamentals: {str(e)}", "sentiment_score": 0}
        
    return {"fundamental_signals": result}
