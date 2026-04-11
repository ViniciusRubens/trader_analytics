import streamlit as st
from dotenv import load_dotenv

from engine.agents import AITradingTeam
from services.finance_service import MarketDataService
from interface.charts import StockVisualizer
from interface.layout import AppLayout

# Load environment variables (.env file with API Keys like GROQ_API_KEY)
load_dotenv()

# Configure the main Streamlit page settings
st.set_page_config(
    page_title = "Trader Analytics", 
    page_icon = "📊", 
    layout = "wide" # Required for full-screen columns control
)

def main():
    """Main function to orchestrate the application flow."""
    # Initialize the instances
    layout = AppLayout()
    finance_service = MarketDataService()
    visualizer = StockVisualizer()
    ai_team = AITradingTeam()

    layout.apply_custom_style()

    empty_l, central_col, empty_r = st.columns([1, 2, 1])

    with central_col:
        layout.render_top_bar()
        st.divider() # Visual separation
        ticker = layout.render_header()

        if st.button("Analyze Ticker", use_container_width = True):
            if ticker:
                with st.spinner(f"Fetching real-time data and AI insights for {ticker}. Please wait..."):
                    try:
                        # Step A: Fetch Market Data
                        historical_data = finance_service.fetch_data(ticker)
                        
                        if historical_data.empty:
                            st.error(f"No data found for '{ticker}'. Please verify the symbol.")
                            return

                        # Step B: Run AI Analysis
                        st.subheader("AI-Generated Analysis")
                        ai_response = ai_team.analyze_ticker(ticker)
                        st.markdown(ai_response)
                        
                        st.divider()

                        # Step C: Render Visualizations
                        st.subheader("Data Visualization")
                        visualizer.plot_stock_price(historical_data, ticker)
                        visualizer.plot_candlestick(historical_data, ticker)
                        visualizer.plot_moving_averages(historical_data, ticker)
                        visualizer.plot_volume(historical_data, ticker)
                        
                    except Exception as e:
                        if "Rate limited" in str(e) or "YFRateLimitError" in str(type(e).__name__):
                            st.warning("⏳ **Request limit reached!** Yahoo Finance has temporarily blocked our access. Please wait a few minutes before trying to analyze another ticker.")
                        else:
                            st.error("An error occurred during the analysis.")
                            st.exception(e)
            else:
                st.warning("⚠️ Please enter a valid ticker symbol before analyzing.")

if __name__ == "__main__":
    main()