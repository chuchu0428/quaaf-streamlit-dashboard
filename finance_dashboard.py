import streamlit as st
import yfinance as yf
import pandas as pd

# Function to fetch data for a specific index with one year of data
def fetch_index_data(ticker):
    index = yf.Ticker(ticker)
    hist = index.history(period="1y")  # Fetch data for the past year
    # Calculate moving averages and volatility
    hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
    hist['EMA_20'] = hist['Close'].ewm(span=20, adjust=False).mean()
    hist['Volatility'] = hist['Close'].rolling(window=20).std()
    return hist

# Function to fetch data for a specific stock with one year of data
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")  # Fetch data for the past year
    # Additional data from Yahoo Finance
    info = stock.info
    extra_metrics = {
        'PE Ratio': info.get('trailingPE', 'N/A'),
        'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') is not None else 'N/A',
        'Beta': info.get('beta', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A')
    }
    return hist, extra_metrics


# Streamlit UI for Industry Indices
def display_index_dashboard():
    st.title('Industry Indices Dashboard')
    indices = ['^DJI', '^GSPC', '^IXIC', '^RUT']  # Dow Jones, S&P 500, NASDAQ, Russell 2000
    selected_index = st.sidebar.selectbox('Select an Index', indices)
    index_data = fetch_index_data(selected_index)
    st.write(f"Data for {selected_index}")
    st.dataframe(index_data[['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_20', 'EMA_20', 'Volatility']])
    st.line_chart(index_data[['Close', 'SMA_20', 'EMA_20']])

# Streamlit UI for Stocks
def display_stock_dashboard():
    st.title('Stocks Dashboard')
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Example stocks
    selected_stock = st.sidebar.selectbox('Select a Stock', stocks)
    stock_data, metrics = fetch_stock_data(selected_stock)
    st.write(f"Data for {selected_stock}")
    st.dataframe(stock_data[['Open', 'High', 'Low', 'Close', 'Volume']])
    st.metric(label="PE Ratio", value=metrics['PE Ratio'])
    st.metric(label="Dividend Yield", value=metrics['Dividend Yield'])
    st.metric(label="Beta", value=metrics['Beta'])
    st.metric(label="Market Cap", value=metrics['Market Cap'])
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
