import json
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px

def get_stock_data(ticker):
    """
    Fetch stock data for a given ticker with comprehensive error handling
    """
    # List of possible suffixes to try
    suffixes = ['.NS', '.BO', '']
    
    # Try different suffixes and exchanges
    for suffix in suffixes:
        try:
            # Construct full ticker symbol
            full_ticker = ticker + suffix
            
            # Fetch stock data
            stock_data = yf.Ticker(full_ticker)
            historical_data = stock_data.history(period='1y')
            
            # Check if data is not empty
            if not historical_data.empty:
                # Additional validation
                if len(historical_data) > 0:
                    return historical_data, full_ticker
        except Exception as e:
            # Log the error for debugging
            st.write(f"Error fetching data for {full_ticker}: {e}")
            continue
    
    # If no data found after all attempts
    st.error(f"Could not retrieve data for ticker {ticker}")
    return None, None

def calculate_technical_indicators(data):
    """
    Calculate various technical indicators
    """
    close_prices = data['Close']
    
    # Simple Moving Averages
    sma_20 = close_prices.rolling(window=20).mean().iloc[-1]
    sma_50 = close_prices.rolling(window=50).mean().iloc[-1]
    
    # Exponential Moving Averages
    ema_20 = close_prices.ewm(span=20, adjust=False).mean().iloc[-1]
    ema_50 = close_prices.ewm(span=50, adjust=False).mean().iloc[-1]
    
    # RSI Calculation
    delta = close_prices.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    # MACD Calculation
    short_EMA = close_prices.ewm(span=12, adjust=False).mean()
    long_EMA = close_prices.ewm(span=26, adjust=False).mean()
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    macd_histogram = MACD - signal
    
    return {
        'Last Close Price': close_prices.iloc[-1],
        '20-day SMA': sma_20,
        '50-day SMA': sma_50,
        '20-day EMA': ema_20,
        '50-day EMA': ema_50,
        'RSI': rsi,
        'MACD': MACD.iloc[-1],
        'MACD Signal': signal.iloc[-1],
        'MACD Histogram': macd_histogram.iloc[-1]
    }

def create_price_chart(data):
    """
    Create an interactive price chart using Plotly
    """
    fig = go.Figure()
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ))
    
    # Moving Averages
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['Close'].rolling(window=20).mean(), 
        mode='lines', 
        name='20-day MA', 
        line=dict(color='orange', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['Close'].rolling(window=50).mean(), 
        mode='lines', 
        name='50-day MA', 
        line=dict(color='green', width=2)
    ))
    
    fig.update_layout(
        title='Stock Price with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )
    
    return fig

def create_volume_chart(data):
    """
    Create an interactive volume chart
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data.index, 
        y=data['Volume'], 
        name='Volume',
        marker_color='lightblue'
    ))
    fig.update_layout(
        title='Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume'
    )
    return fig

def calculate_performance_metrics(data):
    """
    Calculate comprehensive performance metrics
    """
    # Daily returns
    daily_returns = data['Close'].pct_change()
    
    # Cumulative return
    cumulative_return = (1 + daily_returns).prod() - 1
    
    # Annualized volatility
    volatility = daily_returns.std() * np.sqrt(252)
    
    # Sharpe Ratio (assuming risk-free rate = 0)
    sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252)
    
    # Maximum Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    
    return {
        'Total Return (%)': cumulative_return * 100,
        'Volatility (%)': volatility * 100,
        'Sharpe Ratio': sharpe_ratio,
        'Max Drawdown (%)': max_drawdown * 100
    }

def create_returns_distribution(data):
    """
    Create a distribution of returns
    """
    daily_returns = data['Close'].pct_change().dropna()
    
    fig = px.histogram(
        daily_returns, 
        x=daily_returns, 
        title='Distribution of Daily Returns',
        labels={'x': 'Daily Returns', 'y': 'Frequency'},
        marginal='box'
    )
    
    return fig

def main():
    # Set up the Streamlit page
    st.set_page_config(layout="wide", page_title="Stock Analysis Dashboard")
    
    # Title and description
    st.title('🚀 Comprehensive Stock Analysis Dashboard')
    st.markdown("Analyze stock performance, technical indicators, and key metrics.")
    
    # Sidebar for stock selection
    with st.sidebar:
        st.header('📊 Stock Selection')
        ticker = st.text_input('Enter Stock Ticker:', value='')
        st.markdown("*Supports Indian (NSE/BSE) and International Stocks*")
        
        # Optional additional filters
        st.header('🔍 Analysis Preferences')
        show_advanced = st.checkbox('Show Advanced Metrics', value=False)
    
    # Main analysis section
    if ticker:
        # Fetch stock data
        data, full_ticker = get_stock_data(ticker)
        
        if data is not None:
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(['Price & Indicators', 'Performance', 'Advanced Analysis'])
            
            # First Tab: Price and Indicators
            with tab1:
                col1, col2 = st.columns([2,1])
                
                # Price Chart
                with col1:
                    st.header('📈 Price Chart')
                    price_chart = create_price_chart(data)
                    st.plotly_chart(price_chart, use_container_width=True)
                
                # Technical Indicators
                with col2:
                    st.header('📊 Key Indicators')
                    indicators = calculate_technical_indicators(data)
                    for name, value in indicators.items():
                        st.metric(label=name, value=f"{value:.2f}")
                
                # Volume Chart
                st.header('📊 Trading Volume')
                volume_chart = create_volume_chart(data)
                st.plotly_chart(volume_chart, use_container_width=True)
            
            # Second Tab: Performance Metrics
            with tab2:
                col1, col2 = st.columns(2)
                
                # Performance Metrics
                with col1:
                    st.header('📈 Performance Overview')
                    performance = calculate_performance_metrics(data)
                    for name, value in performance.items():
                        st.metric(label=name, value=f"{value:.2f}")
                
                # Returns Distribution
                with col2:
                    st.header('📊 Returns Distribution')
                    returns_dist = create_returns_distribution(data)
                    st.plotly_chart(returns_dist, use_container_width=True)
            
            # Third Tab: Advanced Analysis (Optional)
            with tab3:
                if show_advanced:
                    st.header('🔬 Advanced Stock Analysis')
                    
                    # Company Information (if available)
                    try:
                        stock_info = yf.Ticker(full_ticker)
                        info = stock_info.info
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader('Company Profile')
                            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                            st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                        
                        with col2:
                            st.subheader('Valuation Metrics')
                            st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")
                            st.write(f"**Forward P/E:** {info.get('forwardPE', 'N/A')}")
                            st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
                    except Exception as e:
                        st.warning("Unable to retrieve advanced company information")
                else:
                    st.info("Enable 'Show Advanced Metrics' in the sidebar to view detailed company analysis")
        else:
            st.error(f"Could not retrieve data for {ticker}")

if __name__ == '__main__':
    main()