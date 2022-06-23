import datetime as dt
from datetime import datetime
from lib2to3.pgen2.token import NEWLINE
from telnetlib import BM
import pandas as pd
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
prevDate = datetime(1993, 1, 29)                       #starting with 1993-02-01, previous date was 1993-01-29
budgetPerMonth = 100
magnitudedropbuy = 1                                   #how much budgetPerMonth times should be invested at a "drop buy"

#Buy every first open stock market day of the month (fd = first day)
avgprice_fd = [0]                        #Average share price of investment
shares_fd = [0]                          #Number of shares
lastBuyMonth_fd = 1

#Buy every last open stock market day of the month (ld = last day)
avgprice_ld = [0]                        #Average share price of investment
shares_ld = [0]                          #Number of shares
lastBuyMonth_ld = 1

#Buy monthly at a drop of 2 pct. between open to close, or last day of month (oc = open to close)
lastBuyMonth_oc = 1
avgprice_oc = [0]                        #Average share price of investment
shares_oc = [0]                          #Number of sharesavgprice_oc

results_df['Pct. Open to Close'] = change_open_to_close
results_df['Pct. Open to Low'] = change_open_to_low
results_df['Pct. Prev. Close to Close'] = change_prevclose_to_close
results_df['Pct. Prev. Close to Low'] = change_prevclose_to_low

#first day strategy
for date in results_df.index:
    if date.month is not lastBuyMonth_fd:
        #buy close of current date
            noSharesBuying = budgetPerMonth / spy_df['Close'][date]
            newNoShares = shares_fd[-1] + noSharesBuying
            avgprice_fd.append((avgprice_fd[-1] * shares_fd[-1] 
                                               + spy_df['Close'][date] * noSharesBuying) / newNoShares)
            shares_fd.append(newNoShares)
            lastBuyMonth_fd = date.month
            continue

    avgprice_fd.append(avgprice_fd[-1])
    shares_fd.append(shares_fd[-1])

#last day strategy
for date in results_df.index:
    if (date.month - lastBuyMonth_ld) == 2 or (date.month - lastBuyMonth_ld) == -10:
        #buy close of last day of previous month
            noSharesBuying = budgetPerMonth / spy_df['Close'][prevDate]
            newNoShares = shares_ld[-1] + noSharesBuying
            avgprice_ld[-1] = ((avgprice_ld[-1] * shares_ld[-1] 
                                               + spy_df['Close'][prevDate] * noSharesBuying) / newNoShares)
            shares_ld[-1] = (newNoShares)
            lastBuyMonth_ld = prevDate.month

    avgprice_ld.append(avgprice_ld[-1])
    shares_ld.append(shares_ld[-1])
    prevDate = date

#open to close strategy
for date in results_df.index:
    if lastBuyMonth_oc is not date.month:
        if (date.month - lastBuyMonth_oc) == 2 or (date.month - lastBuyMonth_oc) == -10:
            #buy close of last day of previous month
            noSharesBuying = budgetPerMonth / spy_df['Close'][prevDate]
            newNoShares = shares_oc[-1] + noSharesBuying
            avgprice_oc[-1] = ((avgprice_oc[-1] * shares_oc[-1] 
                                               + spy_df['Close'][prevDate] * noSharesBuying) / newNoShares)
            shares_oc[-1] = (newNoShares)
            lastBuyMonth_oc = prevDate.month

        if results_df['Pct. Open to Close'][date] <= -2:
            #buy close of current date
            noSharesBuying = (budgetPerMonth * magnitudedropbuy) / spy_df['Close'][date]
            newNoShares = shares_oc[-1] + noSharesBuying
            avgprice_oc.append((avgprice_oc[-1] * shares_oc[-1] 
                                               + spy_df['Close'][date] * noSharesBuying) / newNoShares)
            shares_oc.append(newNoShares)
            lastBuyMonth_oc = date.month
            continue

    avgprice_oc.append(avgprice_oc[-1])
    shares_oc.append(shares_oc[-1])
    prevDate = date

#Remove the initial 0's from the lists
avgprice_fd.remove(0)
shares_fd.remove(0)
avgprice_ld.remove(0)
shares_ld.remove(0)
avgprice_oc.remove(0)
shares_oc.remove(0)

results_df['Avg. price (monthly & first day)'] = avgprice_fd
results_df['Shares (monthly & first day)'] = shares_fd

results_df['Avg. price (monthly & last day)'] = avgprice_ld
results_df['Shares (monthly & last day)'] = shares_ld

results_df['Avg. price (monthly & 2pct.)'] = avgprice_oc
results_df['Shares (monthly & 2pct.)'] = shares_oc

print(results_df)

totalDeposit = results_df['Shares (monthly & first day)'][-1] * results_df['Avg. price (monthly & first day)'][-1]
print("-== first day ==-")
print("total deposit:", totalDeposit)
print("total value:", spy_df['Close'][-1] *  results_df['Shares (monthly & first day)'][-1])
print("pct. profit:", ((spy_df['Close'][-1] *  results_df['Shares (monthly & first day)'][-1] - totalDeposit) / totalDeposit) * 100)

totalDeposit = results_df['Shares (monthly & last day)'][-1] * results_df['Avg. price (monthly & last day)'][-1]
print("-== last day ==-")
print("total deposit:", totalDeposit)
print("total value:", spy_df['Close'][-1] *  results_df['Shares (monthly & last day)'][-1])
print("pct. profit:", ((spy_df['Close'][-1] *  results_df['Shares (monthly & last day)'][-1] - totalDeposit) / totalDeposit) * 100)

totalDeposit = results_df['Shares (monthly & 2pct.)'][-1] * results_df['Avg. price (monthly & 2pct.)'][-1]
print("-== 2pct. drop ==-")
print("total deposit:", totalDeposit)
print("total value:", spy_df['Close'][-1] *  results_df['Shares (monthly & 2pct.)'][-1])
print("pct. profit:", ((spy_df['Close'][-1] *  results_df['Shares (monthly & 2pct.)'][-1] - totalDeposit) / totalDeposit) * 100)