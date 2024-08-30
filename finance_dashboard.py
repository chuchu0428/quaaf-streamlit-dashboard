import streamlit as st
import yfinance as yf
import pandas as pd

# Function to fetch data for a specific ticker with one year of data
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

# Streamlit UI for Industry Indices
def display_index_dashboard():
    st.title('Industry Indices Dashboard')
    indices = ['^DJI', '^GSPC', '^IXIC', '^RUT']  # Dow Jones, S&P 500, NASDAQ, Russell 2000
    selected_index = st.sidebar.selectbox('Select an Index', indices)
    index_data, _ = fetch_data(selected_index)
    st.write(f"Data for {selected_index}")
    st.dataframe(index_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'EMA_20', 'Volatility', 'RSI', 'Upper Bollinger', 'Lower Bollinger']])
    st.line_chart(index_data[['Close', 'SMA_20', 'EMA_20']])

# Streamlit UI for Stocks
def display_stock_dashboard():
    st.title('Stocks Dashboard')
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Example stocks
    selected_stock = st.sidebar.selectbox('Select a Stock', stocks)
    stock_data, metrics = fetch_data(selected_stock, with_extra_metrics=True)
    st.write(f"Data for {selected_stock}")
    st.dataframe(stock_data[['Open', 'High', 'Low', 'Close', 'Volume']])
    for label, value in metrics.items():
        st.metric(label=label, value=value)
    st.line_chart(stock_data['Close'])

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
