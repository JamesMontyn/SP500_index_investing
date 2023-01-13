import datetime
import pandas as pd
import investment as iv
import random
from dateutil.relativedelta import relativedelta

# TODO: implement random strategy (random day of month)


class Investor:
    """The Investor class is a modal calculator of an investing strategy.

        Private Variables
        -----------------
        _investment: Investment
            holds the data of the investment in SPY

        _change_df: pandas date frame
            dataframe of certain pct. changes per date the strategy is based on

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
                - '>': greater than
                - '<': less than
                - '1': determiner is a constant, decided by determinant

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
                - 0: first day of the month
                - 1: last day of the month

        _end_date_interval: def
            function that returns the end date of current interval. Possible functions:
                - first_day_month_interval
                - last_day_month_interval
                - random_day_month_interval

        _magnitude: int
            how many times the budget should be spent when the determine function
            finds a right time to invest.
            e.g. magnitude = 2: invests 2*budget when determine functions gives true
        """

    def __init__(self, change_df, budget, determiner, determinant,
                 frequency, interval, magnitude):
        """Constructs a new Investor object

        Parameters
        ----------
        change_df: pandas data frame
            see _change_df

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
            the type of determine function, given as a string
            the possible determiners:
                - 0: first_day_month_interval
                - 1: last_day_month_interval
                - 2: random_day_month_interval

        magnitude: float
            see _magnitude
        """
        self._investment = iv.Investment()
        self._data_frame = change_df.copy()
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
        elif interval == 2:
            self._end_date_interval = self.random_day_month_interval
        else:
            print('interval {} is not a valid option'.format(self._determine))
            self._end_date_interval = self.first_day_month_interval

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
        # adjust to the closest existing last day of month in _change_df
        while end_date not in self._data_frame.index:
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
        # adjust to the closest existing first day of month in _change_df
        while end_date not in self._data_frame.index:
            if end_date > self._data_frame.index[-1]:
                return end_date
            end_date += relativedelta(days=1)
        return end_date

    def random_day_month_interval(self, current_date):
        first_date_of_month = current_date + relativedelta(months=self._frequency)
        candidates = [date for date in self._data_frame.index
                      if first_date_of_month.year == date.year and first_date_of_month.month == date.month]

        # if no candidates found, we are looking at 'future' data, so return the last date in the dataframe
        if not candidates:
            return self._data_frame.index[-1]
        return random.choice(candidates)

    def print_data_frame(self, full):
        """Prints the data frame

        Parameters
        ----------
        full: bool
            print full data frame or not
        """
        if full:
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(self._data_frame)
        else:
            print(self._data_frame)

    def print_investment_stats(self, share_price):
        """Prints the summary results of investment strategy

        Parameters
        ----------
        share_price: float
            current share price value
        """
        value_investment = self._investment.number_of_shares() * share_price

        print("-------=== Summary ===--------")
        print("Total invested:", self._investment.total_invested())
        print("Total shares:", self._investment.number_of_shares())
        print("Avg. P/S investment:", self._investment.average_price())
        print("Value of investment:", value_investment)
        print("Total profit:", value_investment - self._investment.total_invested())
        print("Total pct. gain:",
              ((value_investment
               - self._investment.total_invested())
               / self._investment.total_invested()) * 100)
        print("-------===============--------\n")

    def data_frame_to_csv(self, file_name):
        """Creates a new csv file containing the dataframe

        Parameters
        ----------
        file_name: string
            the filename of the csv file
        """
        self._data_frame.to_csv(file_name)

    def calculate_investments(self):
        """Performs the investment strategy, as such:
            1. Initial buy, buy at first date in the data frame
            Loop:
                2.1. Buy if at end of current interval
                2.2. Buy if determine function gives True (and haven't bought in interval yet)
        """
        # Initial buy (always start with a first buy)
        buy_price = self._data_frame.iloc[0, 1]
        date = self._data_frame.index[0]
        self._investment.invest(buy_price, (self._budget / buy_price))
        self._data_frame.at[date, 'Invested'] = self._investment.total_invested()
        self._data_frame.at[date, 'Shares'] = self._investment.number_of_shares()
        self._data_frame.at[date, 'Avg. p/s'] = self._investment.average_price()

        # looping over next dates with a while loop to skip dates that
        # do not have to be looked at (e.g. already invested in interval)
        interval_end_date = self._end_date_interval((self._data_frame.index[0]))
        factor_determine_buy_price = (1 + (self._determinant / 100))
        i = 1
        while i < self._data_frame.index.shape[0]:
            date = self._data_frame.index[i]

            # buy if end of current interval is reached
            if date == interval_end_date:
                buy_price = self._data_frame.iloc[i][1]
                self._investment.invest(buy_price, (self._budget / buy_price))
                interval_end_date = self._end_date_interval(date)
                self._data_frame.at[date, 'Invested'] = self._investment.total_invested()
                self._data_frame.at[date, 'Shares'] = self._investment.number_of_shares()
                self._data_frame.at[date, 'Avg. p/s'] = self._investment.average_price()

            # buy if determine function gives True
            elif self._determine(self._data_frame.iloc[i][0]):
                buy_price = self._data_frame.iloc[i][1] * factor_determine_buy_price
                self._investment.invest(buy_price, ((self._budget*self._magnitude) / buy_price))
                self._data_frame.at[date, 'Invested'] = self._investment.total_invested()
                self._data_frame.at[date, 'Shares'] = self._investment.number_of_shares()
                self._data_frame.at[date, 'Avg. p/s'] = self._investment.average_price()

                # skipping the rest of the dates in this interval
                while date < interval_end_date:
                    i += 1
                    date = self._data_frame.index[i]

                interval_end_date = self._end_date_interval(date)

            i += 1
