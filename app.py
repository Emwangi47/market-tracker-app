import streamlit as st
import yfinance as yf 
import pandas as pd

# Set up the web app title and description

st.set_page_config(page_title="Market Tracker", page_icon="📈", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* This targets the main background */
    .stApp {
        background-color: #6165F2; /* A dark light blue */
    }
    
    /* This targets the sidebar background */
    [data-testid="stSidebar"] {
        background-color: #cce6ff;
    }
</style>
""", unsafe_allow_html=True)
# ------------------


st.title("📈 Live Market Tracker Dashboard")
st.write("Track your portfolio aginst the 7-day Movine Average in real-time.")

# Sidebar for user input
st.sidebar.header("Settings")

# This creates a text box on the left side of the screen
ticker_input = st.sidebar.text_input("Enter Stock Tickers (comma separated)", "AAPL, MSFT, GOOGL, MSFT, AMZN, TSLA, NVDA, META, JPM, V, UNH") 
# Clean up user input into neat Python list 
tickers = [ticker.strip().upper() for ticker in ticker_input.split(",")]

# Dropdown meny to select how far back the chart goes
time_period = st.sidebar.selectbox(
    "Select Time Period:", 
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"], 
    index=2
)

# Main Dashboard Loop
for ticker in tickers:
    st.subheader(f"📊 {ticker}")

    # Fetch data for the past 30 days
    stock = yf.Ticker(ticker)
    history = stock.history(period=time_period)

    if history.empty:
        st.warning(f"Could not fetch data for {ticker}. Please check the ticker symbol and try again.")
        continue

    # Calculate the 7-day moving average
    history['7MA'] = history['Close'].rolling(window=7).mean()
    history['30MA'] = history['Close'].rolling(window=30).mean()

    # Get the lastest data
    latest_price = history.iloc[-1]['Close']
    latest_ma = history.iloc[-1]['7MA']

    # Create columns for clean layour
    col1, col2, col3 = st.columns(3)

    # Display massive numbers (Metrics)
    col1.metric("Current Price", f"${latest_price:.2f}")
    col2.metric("7-Day MA", f"${latest_ma:.2f}")

    # Logic for Alert Status (Red or Green Boxes)
    if latest_price < latest_ma:
       col3.error("🚨 STATUS: BELOW AVERAGE")
    else:
       col3.success("✅ STATUS: ABOVE AVERAGE")

    # 5 Plotting the Chart
    # We grab the Close price, 7MA 30MA columns and tells Steamlit to draw it.
    chart_data = history[['Close', '7MA', '30MA']]
    st.line_chart(chart_data)

    st.divider()
    


 
