import streamlit as st
import yfinance as yf
from datetime import date, timedelta
import pandas as pd
import datetime as dt 


st.title("Stock Market Data Fetch")
# st.subheader("Top 200 Companies's Stock Data")
st.markdown("")

# Placeholder for top 200 companies' ticker symbols
top_200_tickers = [
    "AAPL", "NVDA", "MSFT", "GOOG", "AMZN", "2222.SR", "META", "TSLA", "AVGO", "TSM",
    "BRK-B", "WMT", "JPM", "LLY", "V", "XOM", "MA", "UNH", "ORCL", "TCEHY",
    "COST", "HD", "PG", "NFLX", "MC.PA", "BAC", "JNJ", "NVO", "CRM", "SAP",
    "ABBV", "1398.HK", "ASML", "CVX", "RMS.PA", "KO", "TMUS", "WFC", "600519.SS", "MRK",
    "005930.KS", "IHC.AE", "CSCO", "TM", "ROG.SW", "601288.SS", "MS", "NOW", "ACN", "AXP",
    "TMO", "0941.HK", "ISRG", "NESN.SW", "0857.HK", "IBM", "LIN", "AZN", "RELIANCE.NS", "PEP",
    "BABA", "SHEL", "MCD", "GE", "601988.SS", "AMD", "ABT", "GS", "601939.SS", "NVS",
    "DIS", "PM", "OR.PA", "ADBE", "CAT", "QCOM", "HSBC", "TXN", "DHR", "RY",
    "TCS.NS", "INTU", "PLTR", "VZ", "BKNG", "SIE.DE", "RTX", "CBA.AX", "PRX.AS", "T",
    "300750.SZ", "IDEXY", "ARM", "AMAT", "DTE.DE", "SPGI", "BLK", "ANET", "SU.PA", "C",
    "PFE", "HDB", "LOW", "FMX", "PDD", "AMGN", "SYK", "NEE", "BSX", "KKR",
    "HON", "PGR", "UNP", "UBER", "CMCSA", "SCHW", "MUFG", "3968.HK", "UL", "TJX",
    "COP", "ETN", "SHOP", "TTE", "AIR.PA", "BX", "BA", "SNY", "BHP", "601628.SS",
    "SONY", "DE", "ALV.DE", "3690.HK", "0883.HK", "ADP", "CDI.PA", "FI", "MU", "LMT",
    "PANW", "EL.PA", "APP", "GILD", "BMY", "601318.SS", "BHARTIARTL.NS", "MDT", "XIACF", "6501.T",
    "UPS", "GEV", "UBS", "ADI", "002594.SZ", "VRTX", "CB", "MRVL", "SBUX", "MMC",
    "CFR.SW", "6861.T", "NKE", "LRCX", "1120.SR", "ABBN.SW", "PLD", "KLAC", "6098.T", "TD",
    "000660.KS", "601088.SS", "IBN", "CEG", "SAF.PA", "SPOT", "RIO", "TAQA.AE", "MSTR", "ENB",
    "600900.SS", "AI.PA", "9983.T", "SMFG", "600028.SS", "APO", "MELI", "INTC", "PYPL", "BUD",
    "SO", "D05.SI", "ELV", "RELX", "SHW", "AMT", "EQIX", "BN", "CRWD", "MO"
]

# Button 1: Select Ticker Symbol
selected_ticker = st.selectbox("Select Ticker Symbol", top_200_tickers)

st.markdown("")

# Button 2: Start Date with manual input
col1, col2 = st.columns(2)
with col1:
    start_date_input = st.text_input("Start Date (YYYY-MM-DD)", value="2000-01-01")

# Button 3: End date with manual input
with col2:
    end_date_input = st.text_input("End Date (YYYY-MM-DD)", value="2025-01-01")

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
st.sidebar.info("This app fetches stock market data for the top 200 companies. Select a ticker symbol,type start date and end date to view the data.")



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
