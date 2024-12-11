# SwingBot

SwingBot is a Python script designed to help identify potential swing trade opportunities, by analyzing historical stock data.  
It processes a predefined list of tickers, evaluates technical indicators, and displays promising candidates based on predefined criteria.  

Required dependencies:  
```pip install yfinance pandas numpy ta```  
<br>  

🔍 ***What This Does***  
1. Data Fetching: Pulls historical stock data for a list of tickers from Yahoo Finance.
2. Technical Analysis: Evaluates the stock data against a set of technical indicators (RSI, EMA, MACD, etc.).
3. Results Display: Filters stocks based on defined criteria and displays promising swing trade candidates.
<br>

❌ ***What This Does NOT Do***  
1. Live Stock Watching
2. Buy/Sell Stocks
3. Use AI
<br>

📝 ***Example Output***  
![Swing](https://github.com/user-attachments/assets/a13b87e6-1489-4dff-871a-d8d51e7c32b0)  
<br>

🛠️ ***How to Use***  
1. Create a tickers.txt file, and add your stock tickers. One ticker per line.  
2. Adjust the configuration parameters in the script (RSI, price range, volume, etc.).  
3. Run the script:  
```diff
python3 swingbot.py  
```
<br>

⚠️ ***Disclaimers***  
1. This is not financial advice. This tool was created for educational and testing purposes only.
2. I will not be held responsible for any gains/losses incurred as a result of using this tool.
3. Always do your own research and consult with a financial advisor before making any investment decisions.  
