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
import logging

st.title("Stock Market Data Fetch")
st.markdown("")

# Updated tickers list
top_400_tickers = [
    "MSFT", "AAPL", "NVDA", "AMZN", "GOOG", "2222.SR", "META", "BRK-B", "AVGO", "TSM",
    "TSLA", "WMT", "LLY", "JPM", "V", "TCEHY", "MA", "NFLX", "XOM", "COST", "ORCL", "PG",
    "JNJ", "UNH", "HD", "SAP", "ABBV", "1398.HK", "NVO", "BAC", "KO", "BABA", "PLTR",
    "RMS.PA", "TMUS", "MC.PA", "NESN.SW", "ASML", "600519.SS", "PM", "ROG.SW", "CRM",
    "601288.SS", "005930.KS", "TM", "CVX", "IHC.AE", "WFC", "OR.PA", "CSCO", "0941.HK",
    "ABT", "NVS", "AZN", "IBM", "RELIANCE.NS", "MCD", "GE", "601939.SS", "LIN", "PRX.AS",
    "MRK", "601988.SS", "NOW", "HSBC", "SHEL", "T", "0857.HK", "AXP", "MS", "ACN", "ISRG",
    "HDB", "SIE.DE", "VZ", "PEP", "CBA.AX", "XIACF", "INTU", "UBER", "GS", "DTE.DE",
    "FMX", "RTX", "RY", "IDEXY", "BKNG", "BX", "DIS", "PGR", "ADBE", "ALV.DE", "AMD",
    "TMO", "UL", "PDD", "SPGI", "BSX", "SONY", "QCOM", "CAT", "AMGN", "SCHW", "TXN",
    "002594.SZ", "TCS.NS", "SYK", "TJX", "BLK", "MUFG", "DHR", "3968.HK", "300750.SZ",
    "BA", "NEE", "AIR.PA", "HON", "PFE", "SU.PA", "SNY", "EL.PA", "SPOT", "C", "BHARTIARTL.NS",
    "DE", "UNP", "ARM", "GILD", "SHOP", "BUD", "VRTX", "CMCSA", "TTE", "LOW", "AMAT", "PANW",
    "BHP", "ADP", "IBN", "AI.PA", "601318.SS", "601628.SS", "ETN", "6501.T", "MELI", "COP",
    "SAF.PA", "CB", "ANET", "IBE.MC", "TD", "MMC", "LMT", "CRWD", "MDT", "GEV", "KKR",
    "MSTR", "SAN", "0883.HK", "6861.T", "AMT", "3690.HK", "CS.PA", "APP", "CFR.SW", "1120.SR",
    "BMY", "ENB", "FI", "RELX", "9983.T", "CME", "ZURN.SW", "MO", "SO", "ABBN.SW", "7974.T",
    "ICE", "601088.SS", "600900.SS", "RIO", "WELL", "ADI", "4519.T", "UBS", "PLD", "APH",
    "BNP.PA", "TAQA.AE", "SBUX", "ISP.MI", "LRCX", "BTI", "DUK", "CDI.PA", "WM", "D05.SI",
    "KLAC", "UCG.MI", "ELV", "INVE-B.ST", "0728.HK", "000660.KS", "CI", "SMFG", "MU", "SHW",
    "BAM", "INTC", "TT", "MCK", "ENEL.MI", "600028.SS", "MDLZ", "RR.L", "DASH", "NKE",
    "9432.T", "MUV2.DE", "EQIX", "HCA", "CTAS", "CVS", "AJG", "CDNS", "SBIN.NS", "SE",
    "MCO", "6098.T", "BN", "TRI", "RACE", "UPS", "FTNT", "GSK", "TDG", "LSEG.L", "1299.HK",
    "ORLY", "CSL.AX", "BBVA", "PH", "DG.PA", "SBER.ME", "RSG", "ABNB", "CEG", "CSU.TO",
    "APO", "000333.SZ", "RHM.F", "AON", "IBKR", "MMM", "8766.T", "INFY", "WBC.AX", "BP",
    "ATCO-B.ST", "9984.T", "CL", "GD", "WMB", "PBR", "SNPS", "8058.T", "ECL", "NAB.AX",
    "COF", "SCCO", "8001.T", "NGG", "ITW", "BMO", "601328.SS", "9433.T", "NOC", "ZTS",
    "CP", "NTES", "CMG", "BA.L", "000858.SZ", "MAR", "MSI", "601658.SS", "2454.TW", "BBCA.JK",
    "8035.T", "2317.TW", "CRH", "WDAY", "ADNOCGAS.AE", "DELL", "EPD", "PNC", "PYPL", "REGN",
    "7011.T", "BAJFINANCE.NS", "ENR.F", "USB", "HINDUNILVR.NS", "EQNR", "CNI", "ITC.NS",
    "DEO", "BNS", "ITUB", "601899.SS", "AZO", "HOLN.SW", "7010.SR", "RCL", "ING", "HWM",
    "CARR", "APD", "MFG", "0981.HK", "4063.T", "2082.SR", "MRK.DE", "EOG", "EMR", "CNQ",
    "SPG", "ROP", "SHL.DE", "TRV", "DB1.DE", "CM", "NU", "ADSK", "KMI", "601166.SS", "LICI.NS",
    "CPRT", "LYG", "BK", "HO.PA", "JCI", "MNST", "BCS", "WES.AX", "ANZ.AX", "MBG.DE", "CPG.L",
    "AEP", "NEM", "0388.HK", "HLT", "AFL", "ET", "ROSN.ME", "COR", "ACA.PA", "DLR", "VOLV-A.ST",
    "AEM", "O39.SI", "SNOW", "BN.PA", "G.MI", "VOW3.DE", "SGO.PA", "8031.T", "1180.SR", "LKOH.ME",
    "207940.KS", "2914.T", "CABK.MC", "WMMVF", "TEAM", "III.L", "MFC", "LT.NS", "DSV.VI", "CHTR",
    "MRVL", "PAYX", "CSX", "373220.KS", "UMG.AS", "TRP", "MPLX", "GBTC", "SREN.SW", "DB", "ALL",
    "AMX", "NWG", "PSA", "FDX", "FCX", "LNG", "BMW.DE", "LONN.SW", "MET"
]

# Simplified ticker selection without search
selected_ticker = st.selectbox("Select Ticker Symbol", top_400_tickers)

st.markdown("")

# Button 2: Start Date with manual input
col1, col2 = st.columns(2)
with col1:
    start_date_input = st.text_input("Start Date (YYYY-MM-DD)", value="2000-01-01")

# Button 3: End date with manual input
with col2:
    end_date_input = st.text_input("End Date (YYYY-MM-DD)", value="2025-05-01")

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

# Configure logging
logging.getLogger('yfinance').setLevel(logging.CRITICAL)

def fetch_stock_data(start_date, end_date):
    try:
        # Simple data fetch with minimal parameters
        data = yf.download(
            tickers=selected_ticker,
            start=start_date,
            end=end_date,
            auto_adjust=False
        )
        
        if data is None or data.empty:
            st.warning(f"No data available for {selected_ticker}")
            return None
            
        # Basic data formatting
        data = data.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adj_close',
            'Volume': 'volume'
        })
        
        # Format dates
        data = data.reset_index()
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        data = data.rename(columns={'Date': 'date'})
        
        return data[['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']]
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

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
                    progress_text.text(f"Fetching data for {selected_ticker}...")
                    
                    data = fetch_stock_data(start_date, end_date)
                    
                    if data is not None and not data.empty:
                        progress_text.empty()
                        st.session_state.data = data
                        st.session_state.last_ticker = selected_ticker
                        st.success(f"Data fetched successfully for {selected_ticker}!")
                    else:
                        st.error(f"Failed to fetch data for {selected_ticker}. Please try again.")
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
        mime="text/csv",
        type="primary" 
    )

# Sidebar with additional information

st.sidebar.markdown(
    "<h1 style='color: #28a745; font-weight: bold; font-size: 60px;'>stocky</h1>", 
    unsafe_allow_html=True
)
st.sidebar.markdown("")
st.sidebar.markdown("## About")
st.sidebar.info("This app fetches stock market data for the top 400 companies worldwide, including US, European, and Asian markets. Select a ticker symbol, type start date and end date to view the data.")

st.sidebar.markdown("")
st.sidebar.markdown("<h1 style='color: #00A1E8; font-weight: bold; font-size: 20px;'>Built by Umer Haddii</h1>", 
    unsafe_allow_html=True)

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
