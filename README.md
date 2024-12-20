# Stock Analysis Dashboard


## Overview
A comprehensive stock analysis dashboard built with Streamlit that provides real-time analysis of stocks from both Indian (NSE/BSE) and international markets. The dashboard offers technical indicators, performance metrics, and advanced company analysis in an interactive interface.

## Features

### 📈 Price & Indicators Tab
- Real-time stock price charts with candlestick patterns
- 20-day and 50-day moving averages
- Interactive volume analysis
- Key technical indicators:
  - Simple Moving Averages (20 & 50 day)
  - Exponential Moving Averages (20 & 50 day)
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)

### 📊 Performance Tab
- Comprehensive performance metrics:
  - Total Return percentage
  - Volatility analysis
  - Sharpe Ratio
  - Maximum Drawdown
- Returns distribution visualization with box plot

### 🔬 Advanced Analysis Tab
- Company profile information
- Sector and industry classification
- Market capitalization
- Valuation metrics:
  - P/E Ratio
  - Forward P/E
  - Dividend Yield

## Dependencies
```bash
streamlit
yfinance
pandas
numpy
plotly
```

## Installation
1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Launch the dashboard using the command above
2. Enter a stock ticker in the sidebar:
   - For NSE stocks: Use symbol (e.g., 'TATAMOTORS')
   - For BSE stocks: Use symbol (e.g., 'TATAMOTORS.BO')
   - For international stocks: Use symbol (e.g., 'AAPL')
3. Toggle 'Show Advanced Metrics' for additional analysis
4. Navigate through tabs to view different aspects of analysis

## Error Handling
- The dashboard attempts to fetch data with multiple exchange suffixes (.NS, .BO)
- Clear error messages for invalid tickers or data fetch issues
- Graceful handling of missing company information

## Data Sources
- Stock data: Yahoo Finance API via `yfinance`
- Technical indicators: Calculated in real-time
- Company information: Yahoo Finance API

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
- Built with Streamlit
- Data provided by Yahoo Finance
- Technical analysis calculations based on standard financial formulas

## Support
For support, please open an issue in the repository or contact [saralaufeysonlaya08@gmail.com]
