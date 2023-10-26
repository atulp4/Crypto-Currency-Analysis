# Crypto-Currency-Analysis

**Bitcoin Technical Analysis
This project performs basic technical analysis on Bitcoin price data to identify potential long or short trade opportunities.

**Data
The data used is 1-minute candlestick data for Bitcoin (BTC/USDT) from Binance exchange. The raw CSV data is preprocessed to convert columns to appropriate datatypes and set the 'date' column as the index.

**Analysis
The run_btc_analysis function takes in the following parameters:

analysis - Either "LONG" or "SHORT" to indicate the type of analysis
x - Success threshold percentage for profit target
y - Stop loss threshold percentage if trade moves against entry price
from_date - Start date for analysis period
to_date - End date for analysis period
It iterates through the DataFrame and identifies potential long or short trades based on the entry price, stop loss and profit targets.

For LONG analysis, it marks a 'Success' if price increases by x% from entry and 'Failure' if price drops by y% from entry.

For SHORT analysis, it is reversed - 'Success' if price drops by x% and 'Failure' if price increases by y%.

The average time taken for success and failure trades are also calculated.

Output
The results are displayed in two charts:

Pie chart showing the count of successful and failed trades
Bar chart showing the average time taken for successful and failed trades
This provides a quick visual analysis of the profitability and duration of the trading strategy over the specified period.

Usage
The analysis can be run by passing the desired parameters:

Copy code

run_btc_analysis(analysis="LONG", x=2, y=1, from_date="2021-01-01", to_date="2021-01-07")
This will backtest a LONG strategy with 2% profit target and 1% stop loss over the first week of 2021.

The code can be easily extended to optimize the input parameters or incorporate other trading signals.

        - btc.py
