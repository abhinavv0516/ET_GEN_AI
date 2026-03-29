from langgraph.graph import StateGraph, START, END
from src.state import GraphState
from src.agents.ingestion import ingest_market_data
from src.agents.technical import technical_analysis
from src.agents.fundamental import analyze_fundamentals
from src.agents.scoring import score_signals
from src.agents.alert import generate_alert

def build_graph():
    graph = StateGraph(GraphState)
    
    graph.add_node("ingestion", ingest_market_data)
    graph.add_node("technical", technical_analysis)
    graph.add_node("fundamental", analyze_fundamentals)
    graph.add_node("scoring", score_signals)
    graph.add_node("alert", generate_alert)
    
    graph.add_edge(START, "ingestion")
    graph.add_edge("ingestion", "technical")
    graph.add_edge("ingestion", "fundamental")
    graph.add_edge("technical", "scoring")
    graph.add_edge("fundamental", "scoring")
    graph.add_edge("scoring", "alert")
    graph.add_edge("alert", END)
    
    return graph.compile()
