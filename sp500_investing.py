import datetime as dt
from datetime import datetime
from lib2to3.pgen2.token import NEWLINE
from telnetlib import BM
import pandas as pd
from pandas.tseries.offsets import BMonthEnd
import yfinance as yf
from yahoofinancials import YahooFinancials

spy_df = yf.download('SPY', 
                      period='max',
                      interval='1d',
                      rounding=False, 
                      progress=False)


print(spy_df)

#Percentages changes per day
change_open_to_close = []           #Pct change between Open and Close
change_open_to_low  = []            #Pct change between Open and Low
change_prevclose_to_close  = []     #Pct change between Close of previous day and Close
change_prevclose_to_low  = []       #Pct change between Close of previous day and Low
PrevClose = spy_df['Close'][0]

for date in spy_df.index:
    change_open_to_close.append(((spy_df['Close'][date] - spy_df['Open'][date]) / spy_df['Open'][date]) * 100)
    change_open_to_low.append(((spy_df['Low'][date] - spy_df['Open'][date]) / spy_df['Open'][date]) * 100)
    change_prevclose_to_close.append(((spy_df['Close'][date] - PrevClose) / PrevClose) * 100)
    change_prevclose_to_low.append(((spy_df['Low'][date] - PrevClose) / PrevClose) * 100)
    PrevClose = spy_df['Close'][date]

#Results dataframe
results_df = pd.DataFrame(index=spy_df.index)
lastBuyMonth = 1
prevDate = datetime(1993, 1, 29)                       #starting with 1993-02-01, previous date was 1993-01-29
budgetPerMonth = 100
totalDeposit = 0
avgBuyPrice = 0

#Buy monthly at a drop of 2 pct. between open to close, or last day of month
avgprice_monthly_drop_2pct = [0]              #Average share price of investment
shares_monthly_drop_2pct = [0]                #Number of shares

results_df['Pct. Open to Low'] = change_open_to_close
results_df['Pct. Open to Close'] = change_open_to_low
results_df['Pct. Prev. Close to Close'] = change_prevclose_to_close
results_df['Pct. Prev. Close to Low'] = change_prevclose_to_low

for date in results_df.index:
    if lastBuyMonth is not date.month:
        if (date.month - lastBuyMonth) == 2 or (date.month - lastBuyMonth) == -10:
            #buy close of last day of previous month
            noSharesBuying = budgetPerMonth / spy_df['Close'][prevDate]
            newNoShares = shares_monthly_drop_2pct[-1] + noSharesBuying
            avgprice_monthly_drop_2pct[-1] = ((avgprice_monthly_drop_2pct[-1] * shares_monthly_drop_2pct[-1] 
                                               + spy_df['Close'][prevDate] * noSharesBuying) / newNoShares)
            shares_monthly_drop_2pct[-1] = (newNoShares)
            lastBuyMonth = prevDate.month
            totalDeposit += budgetPerMonth

        if results_df['Pct. Open to Close'][date] <= -2:
            print(date, spy_df['Close'][date], results_df['Pct. Open to Close'][date])
            #buy close of current date
            noSharesBuying = (budgetPerMonth * 5) / spy_df['Close'][date]
            newNoShares = shares_monthly_drop_2pct[-1] + noSharesBuying
            avgprice_monthly_drop_2pct.append((avgprice_monthly_drop_2pct[-1] * shares_monthly_drop_2pct[-1] 
                                               + spy_df['Close'][date] * noSharesBuying) / newNoShares)
            shares_monthly_drop_2pct.append(newNoShares)
            lastBuyMonth = date.month
            totalDeposit += budgetPerMonth * 5
            continue

    avgprice_monthly_drop_2pct.append(avgprice_monthly_drop_2pct[-1])
    shares_monthly_drop_2pct.append(shares_monthly_drop_2pct[-1])
    prevDate = date

#Remove the initial 0's from the lists
avgprice_monthly_drop_2pct.remove(0)
shares_monthly_drop_2pct.remove(0)

results_df['Avg. price (monthly & 2pct.)'] = avgprice_monthly_drop_2pct
results_df['Shares (monthly & 2pct.)'] = shares_monthly_drop_2pct

print(results_df)
print("total deposit:", totalDeposit)
print("total value:", spy_df['Close'][-1] *  results_df['Shares (monthly & 2pct.)'][-1])
print("pct. profit:", ((spy_df['Close'][-1] *  results_df['Shares (monthly & 2pct.)'][-1] - totalDeposit) / totalDeposit) * 100)


