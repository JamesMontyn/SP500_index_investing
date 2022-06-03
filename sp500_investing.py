import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials

spy_df = yf.download('SPY', 
                      start='2019-01-01', 
                      end='2022-06-03', 
                      progress=False)
spy_df.head()

print(spy_df)