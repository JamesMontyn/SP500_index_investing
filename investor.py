import investment as iv


class Investor:
    def __init__(self, change_list, budget, determiner, determinant, frequency, magnitude):
        self._investment = iv.Investment
        self._change_list = change_list
        self._budget = budget

        if determiner == '>':
            self._determine = self.determine_operator_greater
        elif determiner == '<':
            self._determine = self.determine_operator_lesser
        elif determiner == '1':
            self._determine = self.determine_operator_constant
        else:
            print('Determiner {} is not a valid option'.format(self._determine))

        self._determinant = determinant
        self._frequency = frequency
        self._magnitude = magnitude

    def determine_operator_greater(self, input_):
        return input_ > self._determinant

    def determine_operator_lesser(self, input_):
        return input_ < self._determinant

    def determine_operator_constant(self, _):
        return self._determinant

    def calculate_investments(self):
        #TODO: calculation

"""
import datetime as dt
from datetime import datetime

prevDate = datetime(1993, 1, 29)  # starting with 1993-02-01, previous date was 1993-01-29

# first day strategy
for date in results_df.index:
    if date.month is not lastBuyMonth_fd:
        # buy close of current date
        noSharesBuying = budgetPerMonth / spy_df['Close'][date]
        newNoShares = shares_fd[-1] + noSharesBuying
        avgprice_fd.append((avgprice_fd[-1] * shares_fd[-1]
                            + spy_df['Close'][date] * noSharesBuying) / newNoShares)
        shares_fd.append(newNoShares)
        lastBuyMonth_fd = date.month
        continue

    avgprice_fd.append(avgprice_fd[-1])
    shares_fd.append(shares_fd[-1])

# last day strategy
for date in results_df.index:
    if (date.month - lastBuyMonth_ld) == 2 or (date.month - lastBuyMonth_ld) == -10:
        # buy close of last day of previous month
        noSharesBuying = budgetPerMonth / spy_df['Close'][prevDate]
        newNoShares = shares_ld[-1] + noSharesBuying
        avgprice_ld[-1] = ((avgprice_ld[-1] * shares_ld[-1]
                            + spy_df['Close'][prevDate] * noSharesBuying) / newNoShares)
        shares_ld[-1] = (newNoShares)
        lastBuyMonth_ld = prevDate.month

    avgprice_ld.append(avgprice_ld[-1])
    shares_ld.append(shares_ld[-1])
    prevDate = date

# open to close strategy
for date in results_df.index:
    if lastBuyMonth_oc is not date.month:
        if (date.month - lastBuyMonth_oc) == 2 or (date.month - lastBuyMonth_oc) == -10:
            # buy close of last day of previous month
            noSharesBuying = budgetPerMonth / spy_df['Close'][prevDate]
            newNoShares = shares_oc[-1] + noSharesBuying
            avgprice_oc[-1] = ((avgprice_oc[-1] * shares_oc[-1]
                                + spy_df['Close'][prevDate] * noSharesBuying) / newNoShares)
            shares_oc[-1] = (newNoShares)
            lastBuyMonth_oc = prevDate.month

        if results_df['Pct. Open to Close'][date] <= -2:
            # buy close of current date
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

# Remove the initial 0's from the lists
avgprice_fd.remove(0)
shares_fd.remove(0)
avgprice_ld.remove(0)
shares_ld.remove(0)
avgprice_oc.remove(0)
shares_oc.remove(0)
"""


