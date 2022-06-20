import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials

spy_df = yf.download('SPY', 
                      period='max',
                      interval='1d',
                      rounding=False, 
                      progress=False)

print(spy_df)


#Calculating percentages change per day
change_open_to_close = []           #Pct change between Open and Close
change_open_to_low  = []            #Pct change between Open and Low
change_prevclose_to_close  = []     #Pct change between Close of previous day and Close
change_prevclose_to_low  = []       #Pct change between Close of previous day and Low
PrevClose = spy_df['Close'][0]

for ind in spy_df.index:
    change_open_to_close.append(((spy_df['Close'][ind] - spy_df['Open'][ind]) / spy_df['Open'][ind]) * 100)
    change_open_to_low.append(((spy_df['Low'][ind] - spy_df['Open'][ind]) / spy_df['Open'][ind]) * 100)
    change_prevclose_to_close.append(((spy_df['Close'][ind] - PrevClose) / PrevClose) * 100)
    change_prevclose_to_low.append(((spy_df['Low'][ind] - PrevClose) / PrevClose) * 100)
    PrevClose = spy_df['Close'][ind]

spy_df['Pct. Open to Low'] = change_open_to_close
spy_df['Pct. Open to Close'] = change_open_to_low
spy_df['Pct. Prev. Close to Close'] = change_prevclose_to_close
spy_df['Pct. Prev. Close to Low'] = change_prevclose_to_low

print(spy_df)