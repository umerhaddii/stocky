import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import pandas as pd
import datetime as dt 


st.title("Stock Market Data Fetch")
# st.subheader("Top 100 Companies's Stock Data")
st.markdown("")

# Placeholder for top 100 companies' ticker symbols
top_100_tickers = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "JNJ", "JPM", "V",
    "UNH", "XOM", "ORCL", "MA", "NVO", "COST", "HD", "PG", "NFLX", "NVDA",
    "AVGO", "LLY", "WMT", "TSM", "BAC", "PYPL", "DIS", "CRM", "TMUS", "ABT",
    "CVX", "PFE", "INTC", "VZ", "MRK", "KO", "PEP", "CMCSA", "TXN", "ADBE",
    "ACN", "TMO", "ABBV", "MCD", "NEE", "SBUX", "AMGN", "DHR", "HON", "LMT",
    "CAT", "UNP", "BA", "IBM", "CSCO", "UPS", "INTU", "MDLZ", "LOW", "SO",
    "CVS", "T", "MS", "QCOM", "BHP", "BMY", "LIN", "RTX", "COP", "PM",
    "AMD", "MDLX", "DE", "AMT", "D", "AMAT", "CL", "SCHW", "NOW", "EW",
    "LRCX", "GM", "FDX", "MU", "DUK", "BKNG", "AXP", "TJX", "SGP", "ISRG"
]

# Button 1: Select Ticker Symbol
selected_ticker = st.selectbox("Select Ticker Symbol", top_100_tickers)

st.markdown("")

# Button 2: Start Date with manual input
col1, col2 = st.columns(2)
with col1:
    start_date_input = st.text_input("Start Date (YYYY-MM-DD)", value="2007-01-01")

# Button 3: End date with manual input
with col2:
    end_date_input = st.text_input("End Date (YYYY-MM-DD)", value="2024-12-01")

try:
    start_date = dt.datetime.strptime(start_date_input, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end_date_input, "%Y-%m-%d").date()
except ValueError:
    st.error("Invalid date format. Please use YYYY-MM-DD.")

st.markdown("")

# Button 4: Fetch Data
if st.button("Fetch Data", use_container_width=True):
    # Fetch data for the selected ticker symbol and date range
    data = yf.download(selected_ticker, start=start_date, end=end_date)

    # add clear button
    if st.button("Clear"):
        st.session_state.clear()


    # Display the data in a table
    st.write(data)

    # Download the data as a CSV file
    csv = data.to_csv(index=True)
    st.download_button("Download CSV", csv, file_name=f"{selected_ticker}_{start_date}_{end_date}.csv")



# Sidebar with additional information

# Set the sidebar header with bold green text
st.sidebar.markdown(
    "<h1 style='color: #28a745; font-weight: bold; font-size: 48px;'>stocky</h1>", 
    unsafe_allow_html=True
)
st.sidebar.markdown("")
st.sidebar.markdown("## About")
st.sidebar.info("This app fetches stock market data for the top 100 companies. Select a ticker symbol,type start date and end date to view the data.")



st.sidebar.markdown("")
st.sidebar.caption(
    "Built by [Umer Haddii](https://www.linkedin.com/in/umerhaddii)"
)


linkedin = "https://raw.githubusercontent.com/umerhaddii/stocky/main/images/linkedin.gif"
kaggle = "https://raw.githubusercontent.com/umerhaddii/stocky/main/images/kaggle.gif"
share = "https://raw.githubusercontent.com/umerhaddii/stocky/main/images/share.gif"

st.sidebar.caption(
    f"""
        <div style='display: flex; align-items: center;'>
            <a href = 'https://www.linkedin.com/in/umerhaddii'><img src='{linkedin}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
            <a href = 'https://www.kaggle.com/umerhaddii'><img src='{kaggle}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href = 'www.youtube.com/@umerhaddii007'><img src='{share}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            
        </div>
        """,
    unsafe_allow_html=True,
)
