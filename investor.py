import investment as iv
from dateutil.relativedelta import relativedelta


class Investor:
    """The Investor class is a modal calculator of an investing strategy.

        Private Variables
        -----------------
        _investment: Investment
            holds the data of the investment in SPY

        _change_list: list
            list of certain pct. changes per date the strategy is based on

        _budget: int
            normal budget to invest when determine function decides
            or when at the end of frequency (if determine function never decides)

        _determine: def
            holds the determine function, which has as input an integer and gives
            a decision to invest (true) or not (false) based on the determinant.
            All possible determine functions:
                - determine_operator_greater
                - determine_operator_lesser
                - determine_operator_constant

        _determiner: int
            the operator of the determine function, given as a string
            the possible determiners:
                - '>' - greater than
                - '<' - less than
                - '1' - determiner is a constant, decided by determinant

        _determinant: int
            the factor to compare with in the determine function
            this can be any number. If determiner is constant ('1'), then
            determinant will decide if the determine function will always
            give true (1), or false (0).

        _frequency: int
            how many months are allowed to determine when to invest the
            given budget. If the determine function does not find a right
            time to invest, then budget will be invested at the end of interval
            e.g. frequency = 1: invests budget per month (a month being: Jan., Feb., etc...)

        _interval: int
            on what day of the month the next interval will start.
            Options:
                0: first day of the month
                1: last day of the month

        _end_date_interval: def
            function that returns the end date of current interval. Possible functions:
                - first_day_month_interval
                - last_day_month_interval

        _magnitude: int
            how many times the budget should be spent when the determine function
            finds a right time to invest.
            e.g. magnitude = 2: invests 2*budget when determine functions gives true
        """

    def __init__(self, change_list, budget, determiner, determinant,
                 frequency, interval, magnitude):
        """Constructs a new Investor object

        Parameters
        ----------
        change_list: pandas data frame
            see _change_list

        budget: int
            see _budget

        determiner: string
            the type of determine function, given as a string
            the possible determiners:
                - '>' - greater than
                - '<' - less than
                - '1' - determiner is a constant, decided by determinant

        determinant: float
            see _determinant

        frequency: int
            see _frequency

        interval: int
            see _interval

        magnitude: float
            see _magnitude
        """
        self._investment = iv.Investment()
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
            self._determine = self.determine_operator_constant  # default

        if interval == 0:
            self._end_date_interval = self.first_day_month_interval
        elif interval == 1:
            self._end_date_interval = self.last_day_month_interval
        else:
            print('interval {} is not a valid option'.format(self._determine))
            self._end_date_interval = self.first_day_next_interval

        self._determinant = determinant
        self._frequency = frequency
        self._magnitude = magnitude

    def determine_operator_greater(self, input_):
        return input_ > self._determinant

    def determine_operator_lesser(self, input_):
        return input_ < self._determinant

    def determine_operator_constant(self, _):
        return bool(self._determinant)

    def last_day_month_interval(self, current_date):
        """Returns the last day of current_date + _frequency months
            e.g. current_date = (2000, 1, 30), _frequency = 2
            then next end_date = (2000, 3, 31)

        Parameters
        ----------
        current_date: datetime
            the current date
        """
        end_date = (current_date + relativedelta(months=self._frequency)).replace(day=28) + relativedelta(days=4)
        end_date -= relativedelta(days=end_date.day)
        # adjust to the closest existing last day of month in _change_list
        while end_date not in self._change_list.index:
            end_date -= relativedelta(days=1)
        return end_date

    def first_day_month_interval(self, current_date):
        """Returns the first day of current_date + _frequency months
            e.g. current_date = (2000, 1, 30), _frequency = 2
            then next end_date = (2000, 3, 1)

        Parameters
        ----------
        current_date: datetime
            the current date
        """
        end_date = (current_date + relativedelta(months=self._frequency)).replace(day=1)
        # adjust to the closest existing first day of month in _change_list
        while end_date not in self._change_list.index:
            end_date += relativedelta(days=1)
        return end_date

    def print_data_frame(self):
        print(self._change_list)

    def calculate_investments(self):
        interval_end_date = self._end_date_interval((self._change_list.index[1]))
        factor_determine_buy_price = (1 + (self._determinant / 100))

        # Initial buy (always start with a first buy)
        buy_price = self._change_list.iloc[0, 1]
        self._investment.invest(buy_price, (self._budget / buy_price))

        # looping over next dates with a while loop to skip dates that
        # do not have to be looked at (e.g. already invested in interval)
        i = 0
        while i < self._change_list.index[1:].shape[0]:
            print(self._change_list.index[i], interval_end_date)

            # buy if end of current interval is reached
            if self._change_list.index[i] == interval_end_date:
                buy_price = self._change_list.iloc[i][1]
                self._investment.invest(buy_price, (self._budget / buy_price))
                interval_end_date = self._end_date_interval(self._change_list.index[i])
                print(self._change_list.index[i])

            # buy if determine function gives True
            elif self._determine(self._change_list.iloc[i][0]):
                buy_price = self._change_list.iloc[i][2] * factor_determine_buy_price
                self._investment.invest(buy_price, ((self._budget*self._magnitude) / buy_price))

                # skipping the rest of the dates in this interval
                while self._change_list.index[i] < interval_end_date:
                    i += 1

                interval_end_date = self._end_date_interval(self._change_list.index[i])

            i += 1

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
