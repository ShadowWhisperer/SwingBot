#!/usr/bin/python3

#
# Creator: ShadowWhisperer
#  Github: https://github.com/ShadowWhisperer
# Created: 12/10/2024
# Updated: 12/10/2024
#

import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from datetime import datetime, timedelta
import os
import sys

# Parameters
#####################################
rsi_min = 27            # Minimum RSI threshold       27
rsi_max = 70            # Maximum RSI threshold       70
price_min = 2           # Minimum $                    2
price_max = 20          # Max $                       20
ema_days = 14           # Days for EMA to check       14
macd_fast = 12          # MACD Fast period            12
macd_slow = 26          # MACD Slow period            26
macd_signal = 9         # MACD Signal period           9
relative_vol_min = 0.6  # Relative volume min          0.6
avg_vol_min = 500_000   # Average volume min           500,000
#####################################



#Check for tickers.txt
if not os.path.exists('tickers.txt'):
    print("Error: 'tickers.txt' file not found.")
    sys.exit()


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
clear_screen()

# Print Stats
print(f"\n Searching {sum(1 for _ in open('tickers.txt'))} tickers...\n")
print(f"             RSI: {rsi_min}-{rsi_max}")
print(f"          Priced: ${price_min}-${price_max}")
print(f"Relative Vol Min: {relative_vol_min}")
print(f"     Avg Vol Min: {avg_vol_min}")
print(f" Expo Moving Avg: {ema_days} days")


# List of stock to check
nasdaq_symbols = [line.strip() for line in open('tickers.txt')]

# Color Variables
blue = "\033[94m"
green = "\033[92m"
red = "\033[91m"
white = "\033[0m"


# Find the start and end date, for the last 3 months
def get_date_range():
    end_date = datetime.today().strftime('%Y-%m-%d')  # Current date
    start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')  # 3 months ago
    return start_date, end_date

def fetch_and_analyze(symbol):
    start_date, end_date = get_date_range()
    data = yf.download(symbol, start=start_date, end=end_date, interval="1d", progress=False)
    
    if data.empty:
        print(f"{red}No data for {symbol}{white}")
        return None

    # Flatten multi-level columns and ensure proper naming
    if isinstance(data.columns, pd.MultiIndex):
       data.columns = data.columns.droplevel(0)
       data.columns = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

    # Check if the data was downloaded within the expected date range
    if not (start_date <= data.index[0].strftime('%Y-%m-%d') <= end_date):
        print(f"Warning: Data for {symbol} is outside the expected range.")
    
    if "Adj Close" not in data.columns or "Volume" not in data.columns:
        return None

    try:
        close_series = data["Adj Close"] # Ensure the 'Adj Close' column is 1-dimensional
        
        # Check if the close series is 1-dimensional
        if close_series.ndim != 1:
            print(f"{red}{symbol} has an unexpected dimension: {close_series.ndim}{white}")
            return None
        
        # Calculate RSI using ta.momentum
        rsi_indicator = RSIIndicator(close_series)
        
        # Calculate EMA using ta.trend
        ema_indicator = EMAIndicator(close_series, window=ema_days)
        data["EMA"] = ema_indicator.ema_indicator()
        
        # Calculate MACD using ta.trend
        macd_indicator = MACD(close_series, window_slow=macd_slow, window_fast=macd_fast, window_sign=macd_signal)
        data["MACD"] = macd_indicator.macd()
        data["MACD_Signal"] = macd_indicator.macd_signal()
        data["MACD_Diff"] = macd_indicator.macd_diff()  # MACD Histogram (difference between MACD and MACD Signal)

        data["RSI"] = rsi_indicator.rsi()
        data["AvgVolume"] = data["Volume"].rolling(window=10).mean()  # Average Volume
        data["RelVolume"] = data["Volume"] / data["AvgVolume"]       # Relative Volume

        # Get the latest metrics
        latest_data = data.iloc[-1]
        latest_rsi = latest_data["RSI"]
        latest_price = latest_data["Close"]
        latest_rel_volume = latest_data["RelVolume"]
        latest_avg_volume = latest_data["AvgVolume"]
        latest_ema = latest_data["EMA"]
        latest_macd = latest_data["MACD"]
        latest_macd_signal = latest_data["MACD_Signal"]
        latest_macd_diff = latest_data["MACD_Diff"]

        # Apply filters, including updated MACD conditions
        if (
            rsi_min < latest_rsi < rsi_max and  # RSI between 30 and 70
            price_min < latest_price < price_max and
            latest_avg_volume > avg_vol_min and
            latest_rel_volume > relative_vol_min and
            latest_macd_diff > 0  # MACD Histogram positive (indicating bullish momentum)
        ):
            return {
                "symbol": symbol,
                "rsi": latest_rsi,
                "price": latest_price,
                "rel_volume": latest_rel_volume,
                "avg_volume": latest_avg_volume,
                "ema": latest_ema,
                "macd": latest_macd,
                "macd_signal": latest_macd_signal,
                "macd_diff": latest_macd_diff
            }
    except Exception as e:
        print(f"{red}Error - {symbol}: {e}{white}")
        return None

# Analyze each symbol & filter
results = [fetch_and_analyze(symbol) for symbol in nasdaq_symbols]
swing_candidates = [r for r in results if r]


# Final output
print("\n\n\n------------------------------------------")
print("         [Potential Candidates]")
print("------------------------------------------\n")
if swing_candidates:
    for candidate in swing_candidates:
        print(f"               {green}{candidate['symbol']}{white}\n"
              f"        Price: ${candidate['price']:.2f}\n"
              f"          RSI: {candidate['rsi']:.2f}\n"
              f" Relative Vol: {candidate['rel_volume']:.2f}\n"
              f"      Avg Vol: {candidate['avg_volume']:.2f}\n"
              f"          EMA: ${candidate['ema']:.2f}\n"
              f"         MACD: {candidate['macd']:.2f}\n"
              f"  MACD Signal: {candidate['macd_signal']:.2f}\n"
              f"    MACD Diff: {candidate['macd_diff']:.2f}\n")
else:
    print("No good candidates found.")
