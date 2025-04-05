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
top_300_tockers = [
"Apple",  "Microsoft",  "NVIDIA",  "Amazon", "Alphabet (Google)", "Saudi Aramco", "Meta Platforms (Facebook)", "Berkshire Hathaway", "Tesla", "TSMC", "Broadcom", "Walmart", "Eli Lilly", "Visa",
 "JPMorgan Chase", "Tencent", "UnitedHealth", "Exxon Mobil", "Mastercard", "Costco", "Procter & Gamble", "Johnson & Johnson", "Netflix", "Oracle", "Home Depot", "AbbVie", "ICBC", 
"Coca-Cola", "SAP", "LVMH", "T-Mobile US", "Alibaba", "Novo Nordisk", "Kweichow Moutai", "Bank of America", "Nestlé", "Hermès", "ASML", "Samsung", "Chevron", "Agricultural Bank of China", 
"Roche", "International Holding Company", "China Mobile", "Philip Morris International", "Salesforce", "China Construction Bank", "Cisco", "Abbott Laboratories", "McDonald", "Bank of China", 
"AstraZeneca", "IBM", "Toyota", "Novartis", "Linde", "Merck", "L'Oréal", "Pepsico", "Wells Fargo", "PetroChina", "Shell", "AT&T", "Reliance Industries", "HSBC", "Prosus", "Verizon", "Accenture",
 "General Electric", "Deutsche Telekom", "Palantir", "Fomento Económico Mexicano", "HDFC Bank", "Thermo Fisher Scientific", "American Express", "Intuitive Surgical", "Morgan Stanley", "Siemens", 
"Amgen", "Intuit", "RTX", "Royal Bank Of Canada", "Commonwealth Bank", "Blackstone Group", "Inditex", "Progressive", "Walt Disney", "Unilever", "ServiceNow", "Adobe", "BYD", "CM Bank", "CATL", "Goldman Sachs", 
"PDD Holdings (Pinduoduo)", "Xiaomi", "QUALCOMM", "Booking Holdings (Booking.com)", "Allianz SE", "Tata Consultancy Services", "AMD", "S&P Global", "Texas Instruments", "Nextera Energy", "Caterpillar", 
"TJX Companies", "Uber", "Gilead Sciences", "Sony", "Boston Scientific", "TotalEnergies", "Stryker Corporation", "Pfizer", "Danaher", "Mitsubishi UFJ Financial", "Union Pacific Corporation", "BlackRock", 
"Sanofi", "Airbus", "Comcast", "Charles Schwab", "Lowe's Companies", "Honeywell", "Meituan", "CNOOC", "Bharti Airtel", "Vertex Pharmaceuticals", "EssilorLuxottica", "China Life Insurance", "Ping An Insurance", 
"Anheuser-Busch Inbev", "Deere & Company (John Deere)", "Automatic Data Processing", "Schneider Electric", "Marsh & McLennan Companies", "Bristol-Myers Squibb", "Chubb", "Fiserv", "Citigroup", "Air Liquide", 
"ConocoPhillips", "ICICI Bank", "Al Rajhi Bank", "BHP Group", "Medtronic", "Iberdrola", "Applied Materials", "American Tower", "Spotify", "Boeing", "China Shenhua Energy", "Palo Alto Networks", "Lockheed Martin", 
"Toronto Dominion Bank", "Safran", "Shopify", "Southern Company", "Elevance Health", "China Telecom", "Eaton", "Dior", "China Yangtze Power", "Hitachi", "TAQA", "Altria Group", "Enbridge", "Fast Retailing", 
"Zurich Insurance Group", "MercadoLibre", "Starbucks", "Welltower", "Arm Holdings", "Duke Energy", "Compagnie Financière Richemont", "SK Hynix", "CME Group", "DBS Group", "Prologis", "Waste Management", 
"Rio Tinto", "Intercontinental Exchange", "Keyence", "Sinopec", "AXA", "RELX", "Santander", "British American Tobacco", "Cigna", "ABB", "Intel", "Mondelez", "KKR & Co.", "McKesson", "UBS", "BNP Paribas", 
"Nike", "Investor AB", "Sherwin-Williams", "Petrobras", "United Parcel Service", "Enel", "AIA", "HCA Healthcare", "Arthur J. Gallagher & Co.", "Analog Devices", "Sumitomo Mitsui Financial Group", "Arista Networks", 
"Aon", "NTT (Nippon Telegraph & Telephone)", "Munich RE (Münchener Rück)", "Intesa Sanpaolo", "CVS Health", "State Bank of India", "BP", "CrowdStrike", "O'Reilly Automotive", "Nintendo", "Cintas", "Midea", "KLA", 
"Strategy (MicroStrategy)", "London Stock Exchange", "Lam Research", "Brookfield Corporation", "Ferrari", "UniCredit", "Thomson Reuters", "Recruit", "Equinix", "AppLovin", "Colgate-Palmolive", "Chugai Pharmaceutical", 
"Sberbank", "GE Vernova", "GlaxoSmithKline", "CSL", "Republic Services", "Bank of Communications", "Brookfield Asset Management", "Moody's", "Micron Technology", "Amphenol", "Trane Technologies", "Rolls-Royce Holdings", 
"Banco Bilbao Vizcaya Argentaria", "Wuliangye Yibin", "Northrop Grumman", "TransDigm", "Infosys", "Postal Savings Bank of China", "MediaTek", "Vinci", "Mitsubishi Corporation", "DoorDash", "3M", "Zoetis", 
"Atlas Copco", "Tokio Marine", "Ecolab", "Motorola Solutions", "General Dynamics", "Enterprise Products", "Williams Companies", "Parker-Hannifin", "ACWA POWER Company", "Airbnb", "Illinois Tool Works", 
"Canadian Pacific Railway", "Fortinet", "Constellation Software", "SoftBank", "Bank of Montreal", "National Grid", "Westpac Banking", "KDDI", "NetEase", "Foxconn (Hon Hai Precision Industry)", 
"Chipotle Mexican Grill", "Cadence Design Systems", "Bajaj Finance", "Equinor", "Bank Central Asia", "ADNOC Gas", "Regeneron Pharmaceuticals", "Itōchū Shōji", "National Australia Bank", "Southern Copper", 
"Apollo Global Management", "Interactive Brokers", "Hindustan Unilever", "Zijin Mining", "Sea Limited", "Saudi Telecom Company", "AutoZone", "EOG Resources", "PNC Financial Services", "Canadian National Railway", 
"Industrial Bank", "Synopsys", "ITC"
]

# Simplified ticker selection without search
selected_ticker = st.selectbox("Select Ticker Symbol", top_300_tickers)

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
st.sidebar.info("This app fetches stock market data for the top 300 companies worldwide, including US, European, and Asian markets. Select a ticker symbol, type start date and end date to view the data.")

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
