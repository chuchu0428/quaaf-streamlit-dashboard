import streamlit as st
import yfinance as yf
import pandas as pd

# Sector to stocks mapping for a subset of S&P 500
sector_to_stocks = {
    'Communication Services': [
        'ATVI', 'GOOGL', 'GOOG', 'T', 'CTL', 'CHTR', 'CMCSA', 'DISCA', 'DISCK', 'DISH', 'EA', 'FB', 'FOXA', 'FOX', 'IPG', 
        'LYV', 'NFLX', 'NWSA', 'NWS', 'OMC', 'TMUS', 'TTWO', 'TWTR', 'VZ', 'VIAC', 'DIS'],
    'Consumer Discretionary': [
    'AAP', 'AMZN', 'APTV', 'AZO', 'BBY', 'BKNG', 'BWA', 'CCL', 'CMG', 'DHI', 'DRI', 'EBAY', 'ETSY', 'EXPE', 'F', 
    'FORD', 'GM', 'GRMN', 'HAS', 'HD', 'HLT', 'IP', 'KMX', 'LEG', 'LEN', 'LVS', 'M', 'MAR', 'MCD', 'MGM', 'MHK', 
    'NCLH', 'NKE', 'NVR', 'ORLY', 'PHM', 'PVH', 'RCL', 'RL', 'ROST', 'SBUX', 'SNA', 'TGT', 'TIF', 'TJX', 'TPR', 
    'UAA', 'UA', 'ULTA', 'VFC', 'WHR', 'WYNN', 'YUM'
],
    'Consumer Staples': [
    'ADM', 'BF.B', 'CAG', 'CHD', 'CL', 'CLX', 'COST', 'CPB', 'CAG', 'CVS', 'DPS', 'EL', 'GIS', 'HSY', 'HRL', 
    'K', 'KHC', 'KMB', 'KO', 'KR', 'LW', 'MDLZ', 'MKC', 'MNST', 'MO', 'PEP', 'PG', 'PM', 'SYY', 'SJM', 'TAP', 
    'TSN', 'WBA', 'WMT', 'WAG'
],
    'Energy': [
    'APA', 'BKR', 'COG', 'COP', 'CVX', 'CXO', 'DVN', 'EOG', 'FANG', 'FTI', 'HAL', 'HES', 'HFC', 'KMI', 'MPC', 
    'MRO', 'NBL', 'NOV', 'OKE', 'OXY', 'PSX', 'PXD', 'SLB', 'VLO', 'WMB', 'XEC', 'XOM'
],
    'Financials': [
    'AFL', 'AIG', 'AIZ', 'AJG', 'ALL', 'AMG', 'AON', 'AXP', 'BAC', 'BEN', 'BK', 'BLK', 'BRO', 'C', 'CB', 
    'CBOE', 'CINF', 'CIT', 'CFG', 'CME', 'CMA', 'COF', 'DFS', 'ETFC', 'FRC', 'FITB', 'GL', 'GS', 'HIG', 
    'HBAN', 'ICE', 'IVZ', 'JPM', 'KEY', 'L', 'LNC', 'MCO', 'MET', 'MKTX', 'MMC', 'MS', 'MTB', 'NDAQ', 
    'NTRS', 'PFG', 'PGR', 'PNC', 'PRU', 'RE', 'RF', 'RJF', 'SBNY', 'SCHW', 'SIVB', 'SPGI', 'STT', 'TROW', 
    'TRV', 'UNM', 'USB', 'WFC', 'WRB', 'ZION'
],
    'Health Care': [
    'ABT', 'ABBV', 'ABMD', 'A', 'ALXN', 'ALGN', 'ABC', 'AMGN', 'ANTM', 'BAX', 'BDX', 'BIIB', 'BSX', 'BMY', 'CAH',
    'CNC', 'CERN', 'CI', 'COO', 'CVS', 'DHR', 'DVA', 'XRAY', 'EW', 'GILD', 'HCA', 'HSIC', 'HOLX', 'HUM', 'IDXX',
    'ILMN', 'INCY', 'ISRG', 'IQV', 'JNJ', 'LH', 'LLY', 'MCK', 'MDT', 'MRK', 'MTD', 'MYL', 'PDCO', 'PKI', 'PRGO',
    'PFE', 'DGX', 'REGN', 'RMD', 'SYK', 'MOH', 'TMO', 'UNH', 'UHS', 'VAR', 'VRTX', 'WAT', 'WCG', 'ZBH', 'ZTS'
],
    'Industrials': [
    'MMM', 'ALK', 'ALLE', 'AAL', 'AME', 'AOS', 'ARNC', 'BA', 'CHRW', 'CAT', 'CTAS', 'CPRT', 'CSX', 'CMI', 
    'DE', 'DAL', 'DOV', 'ETN', 'EMR', 'EFX', 'EXPD', 'FAST', 'FDX', 'FLS', 'FLR', 'FTV', 'FBHS', 'GD', 
    'GE', 'GWW', 'HON', 'HII', 'IEX', 'INFO', 'ITW', 'IR', 'JCI', 'J', 'KSU', 'LMT', 'MAS', 'NLSN', 
    'NSC', 'NOC', 'ODFL', 'PCAR', 'PH', 'PNR', 'PWR', 'RTX', 'RSG', 'RHI', 'ROK', 'ROL', 'ROP', 'SNA', 
    'LUV', 'SWK', 'TXT', 'TDG', 'TT', 'TDY', 'UNP', 'UAL', 'UPS', 'URI', 'VRSK', 'WAB', 'WM', 'XYL'
],
    'Information Technology': [
    'AAPL', 'ACN', 'ADBE', 'ADI', 'ADP', 'ADS', 'AKAM', 'AMD', 'ANET', 'ANSS', 'APH', 'APTV', 'AVGO', 'BR', 
    'CDNS', 'CDW', 'CERN', 'CRM', 'CSCO', 'CTXS', 'DXC', 'ENPH', 'EPAM', 'FIS', 'FISV', 'FLT', 'FTNT', 'GLW', 
    'GOOGL', 'GOOG', 'HPE', 'HPQ', 'IBM', 'INTC', 'INTU', 'IPGP', 'IT', 'JKHY', 'JNPR', 'KEYS', 'KLAC', 'LRCX', 
    'MA', 'MCHP', 'MSFT', 'MSI', 'NTAP', 'NLOK', 'NVDA', 'ORCL', 'PAYC', 'PAYX', 'PYPL', 'QCOM', 'QRVO', 'RHT', 
    'CRM', 'STX', 'SWKS', 'SNPS', 'TEL', 'TXN', 'TYL', 'V', 'VRSN', 'WDC', 'WU', 'XLNX', 'XRX', 'ZBRA'
],
    'Materials': [
    'APD', 'ALB', 'AMCR', 'AVY', 'BALL', 'BLL', 'CF', 'CTVA', 'DOW', 'DD', 'EMN', 'ECL', 'FMC', 'FCX', 'IP', 
    'IFF', 'LIN', 'LYB', 'MLM', 'NEM', 'NUE', 'PKG', 'PPG', 'SEE', 'SHW', 'VMC', 'WRK', 'WLK', 'WY'
],
    'Real Estate': [
    'AMT', 'ARE', 'AVB', 'BXP', 'CBRE', 'CCI', 'DLR', 'DRE', 'EQIX', 'EQR', 'ESS', 'EXR', 'FRT', 'HST', 
    'IRM', 'KIM', 'MAA', 'PLD', 'PSA', 'O', 'REG', 'SBAC', 'SPG', 'SLG', 'UDR', 'VTR', 'VNO', 'WELL', 'WY'
],
    'Utilities': [
    'AES', 'AEE', 'AEP', 'AWK', 'ATO', 'CNP', 'CMS', 'ED', 'D', 'DTE', 'DUK', 'EIX', 'ETR', 'EVRG', 'ES', 
    'EXC', 'FE', 'LNT', 'NEE', 'NI', 'NRG', 'PNW', 'PPL', 'PEG', 'SRE', 'SO', 'WEC', 'XEL'
]
}

# Function to fetch data for a specific stock with one year of data
def fetch_data(ticker, with_extra_metrics=False):
    data = yf.Ticker(ticker)
    hist = data.history(period="1y")  # Fetch data for the past year
    hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
    hist['EMA_20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    hist['Volatility'] = hist['Close'].rolling(window=20).std()
    hist['RSI'] = calculate_rsi(hist)
    upper_band, lower_band = calculate_bollinger_bands(hist)
    hist['Upper Bollinger'] = upper_band
    hist['Lower Bollinger'] = lower_band

    extra_metrics = {}
    if with_extra_metrics:
        extra_metrics = fetch_financial_metrics(data)

    return hist, extra_metrics

# Calculate RSI
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate Bollinger Bands
def calculate_bollinger_bands(data, window=20, num_of_std=2):
    sma = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()
    upper_band = sma + (rolling_std * num_of_std)
    lower_band = sma - (rolling_std * num_of_std)
    return upper_band, lower_band

# Fetch financial metrics from Yahoo Finance
def fetch_financial_metrics(stock):
    info = stock.info
    return {
        'Earnings Per Share': info.get('trailingEps', 'N/A'),
        'Price-to-Earnings Ratio': info.get('trailingPE', 'N/A'),
        'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') is not None else 'N/A',
        'Price-to-Book Ratio': info.get('priceToBook', 'N/A'),
        'Debt-to-Equity Ratio': info.get('debtToEquity', 'N/A')
    }

# Streamlit UI for Stocks with Sector Selection
def display_stock_dashboard():
    st.title('Stocks Dashboard')
    sectors = list(sector_to_stocks.keys())
    selected_sector = st.sidebar.selectbox('Select a Sector', sectors)
    stocks = sector_to_stocks[selected_sector]
    selected_stock = st.sidebar.selectbox('Select a Stock from ' + selected_sector, stocks)
    stock_data, metrics = fetch_data(selected_stock, with_extra_metrics=True)
    st.write(f"Data for {selected_stock}")
    st.dataframe(stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'EMA_20', 'Volatility', 'RSI', 'Upper Bollinger', 'Lower Bollinger']])
    for label, value in metrics.items():
        st.metric(label=label, value=value)
    st.line_chart(stock_data[['Close', 'SMA_20', 'EMA_20']])
def display_index_dashboard():
    st.title('Industry Indices Dashboard')
    indices = ['^DJI', '^GSPC', '^IXIC', '^RUT']  # Dow Jones, S&P 500, NASDAQ, Russell 2000
    selected_index = st.sidebar.selectbox('Select an Index', indices)
    index_data, _ = fetch_data(selected_index)
    st.write(f"Data for {selected_index}")
    st.dataframe(index_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'EMA_20', 'Volatility', 'RSI', 'Upper Bollinger', 'Lower Bollinger']])
    st.line_chart(index_data[['Close', 'SMA_20', 'EMA_20']])

# Main function to control the dashboard
def main():
    st.sidebar.title('Dashboard Selection')
    dashboard_type = st.sidebar.radio('Choose a Dashboard', ('Industry Indices', 'Stocks'))

    if dashboard_type == 'Industry Indices':
        display_index_dashboard()
    elif dashboard_type == 'Stocks':
        display_stock_dashboard()

if __name__ == "__main__":
    main()
