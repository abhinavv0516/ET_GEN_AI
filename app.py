import streamlit as st
import plotly.graph_objects as go
from src.graph import build_graph

st.set_page_config(page_title="OmniInvest AI", layout="wide")

st.title("📈 OmniInvest AI Intelligence System")
st.markdown("Multi-Agent AI Pipeline for Indian Retail Investors")

# Sidebar inputs
with st.sidebar:
    st.header("Pipeline Settings")
    ticker_input = st.text_input("Enter Ticker (e.g., RELIANCE.NS, TCS.NS)", value="RELIANCE.NS")
    run_button = st.button("Run Analysis", type="primary")
    
    st.markdown("---")
    st.markdown("""
    **Agents in Pipeline:**
    1. 📡 Market Data Ingestion
    2. 📊 Technical Pattern Recognition
    3. 📰 Fundamental Signal Extraction
    4. ⚖️ Signal Scoring
    5. 🔔 Plain-English Alert Gen
    """)

if run_button:
    if not ticker_input:
        st.warning("Please enter a ticker symbol.")
    else:
        with st.spinner(f"Running LangGraph Pipeline for {ticker_input}..."):
            try:
                app = build_graph()
                initial_state = {"ticker": ticker_input}
                
                # Run the graph
                final_state = app.invoke(initial_state)
                
                # Fetch results from state
                history_df = final_state.get("raw_data", {}).get("history")
                alert_text = final_state.get("final_alert", "No alert generated.")
                scoring = final_state.get("scoring_result", {})
                tech = final_state.get("technical_signals", {})
                fund = final_state.get("fundamental_signals", {})
                
                st.success("Analysis Complete!")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("Price Chart & Technicals")
                    if history_df is not None and not history_df.empty:
                        fig = go.Figure()
                        # Candlestick
                        fig.add_trace(go.Candlestick(
                            x=history_df.index,
                            open=history_df['Open'],
                            high=history_df['High'],
                            low=history_df['Low'],
                            close=history_df['Close'],
                            name='Price'
                        ))
                        # SMAs if they were calculated
                        if 'SMA_50' in history_df.columns:
                            fig.add_trace(go.Scatter(x=history_df.index, y=history_df['SMA_50'], name='50 SMA', line=dict(color='orange')))
                        if 'SMA_200' in history_df.columns:
                            fig.add_trace(go.Scatter(x=history_df.index, y=history_df['SMA_200'], name='200 SMA', line=dict(color='blue')))
                            
                        fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark", height=500)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Could not fetch historical price data.")
                        
                with col2:
                    st.subheader("AI Intelligence Summary")
                    
                    rating = scoring.get("rating", "N/A")
                    score = scoring.get("conviction_score", 0)
                    
                    st.metric("Conviction Score", f"{int(score)}/100", rating)
                    
                    st.markdown("### 🔔 Alert Summary")
                    st.info(alert_text)
                    
                st.markdown("---")
                
                # Detailed breakdown
                with st.expander("Detailed Signal Breakdown", expanded=False):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("#### Technical Signals")
                        for sig in tech.get("signals", []):
                            st.markdown(f"- {sig}")
                            
                    with c2:
                        st.markdown("#### Fundamental Extraction")
                        st.markdown(fund.get("summary", "No fundamental data."))
            except Exception as e:
                st.error(f"Pipeline failed: {str(e)}")
