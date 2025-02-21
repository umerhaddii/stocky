import streamlit as st
import yfinance as yf
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from datetime import date, timedelta
import pandas as pd
import datetime as dt 
import time
from requests.exceptions import RequestException
import backoff  

st.title("Stock Market Data Fetch")
st.markdown("")

# Updated tickers list
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

# Simplified ticker selection without search
selected_ticker = st.selectbox("Select Ticker Symbol", top_200_tickers)

st.markdown("")

# Button 2: Start Date with manual input
col1, col2 = st.columns(2)
with col1:
    start_date_input = st.text_input("Start Date (YYYY-MM-DD)", value="2000-01-01")

# Button 3: End date with manual input
with col2:
    end_date_input = st.text_input("End Date (YYYY-MM-DD)", value="2025-02-20")

try:
    start_date = dt.datetime.strptime(start_date_input, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end_date_input, "%Y-%m-%d").date()
except ValueError:
    st.error("Invalid date format. Please use YYYY-MM-DD.")

st.markdown("")

# Create a custom session with retries
def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    return session

def fetch_stock_data(ticker, start_date, end_date):
    try:
        session = create_session()
        ticker_obj = yf.Ticker(ticker, session=session)
        
        # Fetch data with adjusted close
        data = ticker_obj.history(
            start=start_date,
            end=end_date,
            interval="1d",
            auto_adjust=False,  # Set to False to get both adjusted and unadjusted prices
            actions=True
        )
        
        if data is None or data.empty:
            st.warning(f"No data available for {ticker} in the specified date range.")
            return None
            
        # Rename columns to match requirements
        data = data.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adj_close',
            'Volume': 'volume'
        })
        
        # Ensure all required columns are present
        required_columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        if not all(col in data.columns for col in required_columns):
            st.warning("Retrieved data is missing required columns.")
            return None
        
        # Reset index to make date a column and rename it
        data = data.reset_index()
        data = data.rename(columns={'Date': 'date'})
        
        # Select and reorder columns
        data = data[['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]
        
        return data
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None
    finally:
        if session:
            session.close()

# Add this after initial imports
if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_ticker' not in st.session_state:
    st.session_state.last_ticker = None

# Replace the Fetch Data button logic with:
col1, col2 = st.columns([4, 1])
with col1:
    if st.button("Fetch Data", use_container_width=True):
        with st.spinner(f'Fetching data for {selected_ticker}...'):
            try:
                start_date = dt.datetime.strptime(start_date_input, "%Y-%m-%d").date()
                end_date = dt.datetime.strptime(end_date_input, "%Y-%m-%d").date()
                
                if end_date < start_date:
                    st.error("End date must be after start date")
                else:
                    progress_text = st.empty()
                    progress_text.text("Initializing data fetch...")
                    
                    data = fetch_stock_data(selected_ticker, start_date, end_date)
                    
                    if data is not None and not data.empty:
                        progress_text.empty()
                        st.session_state.data = data
                        st.session_state.last_ticker = selected_ticker
                        st.success("Data fetched successfully!")
                    else:
                        st.error("Failed to fetch data. Please try again.")
                    progress_text.empty()
                    
            except ValueError:
                st.error("Invalid date format. Please use YYYY-MM-DD.")

with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state.data = None
        st.session_state.last_ticker = None
        st.rerun()

# Add this after the buttons
if st.session_state.data is not None:
    st.write(f"### Stock Data for {st.session_state.last_ticker}")
    st.write(st.session_state.data)
    
    # Add column descriptions
    st.write("### Column Descriptions")
    descriptions = {
        'date': 'Date of the trading day',
        'open': 'The price at market open',
        'high': 'The highest price for that day',
        'low': 'The lowest price for that day',
        'close': 'The price at market close, adjusted for splits',
        'adj_close': 'Closing price adjusted for splits and dividend distributions (CRSP standards)',
        'volume': 'The number of shares traded on that day'
    }
    st.table(pd.DataFrame(descriptions.items(), columns=['Column', 'Description']))
    
    # Export CSV with formatted columns
    csv = st.session_state.data.to_csv(index=False)
    st.download_button(
        "Download CSV",
        csv,
        file_name=f"{st.session_state.last_ticker}_{start_date}_{end_date}.csv",
        mime="text/csv"
    )

# Sidebar with additional information

# Set the sidebar header with bold green text
st.sidebar.markdown(
    "<h1 style='color: #28a745; font-weight: bold; font-size: 48px;'>stocky</h1>", 
    unsafe_allow_html=True
)
st.sidebar.markdown("")
st.sidebar.markdown("## About")
st.sidebar.info("This app fetches stock market data for the top 200 companies worldwide, including US, European, and Asian markets. Select a ticker symbol, type start date and end date to view the data.")

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
            <a href = 'https://linktr.ee/umerhaddii'><img src='{share}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            
        </div>
        """,
    unsafe_allow_html=True,
)
