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

        _magnitude: int
            how many times the budget should be spent when the determine function
            finds a right time to invest.
            e.g. magnitude = 2: invests 2*budget when determine functions gives true
        """

    def __init__(self, change_list, budget, determiner, determinant, frequency, magnitude):
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

        self._determinant = determinant
        self._frequency = frequency
        self._magnitude = magnitude

    def determine_operator_greater(self, input_):
        return input_ > self._determinant

    def determine_operator_lesser(self, input_):
        return input_ < self._determinant

    def determine_operator_constant(self, _):
        return self._determinant

    def next_end_date_interval(self, current_date):
        """Returns the last day of current_date + _frequency months
            e.g. current_date = (2000, 1, 30), _frequency = 2
            then next end_date = (2000, 3, 31)

        Parameters
        ----------
        current_date: datetime
            the current date
        """
        end_date = (current_date + relativedelta(months=self._frequency)).replace(day=28) + relativedelta(days=4)
        return end_date - relativedelta(days=end_date.day)

    def calculate_investments(self):
        print(self._change_list.index[0])
        date_end_interval = self.next_end_date_interval((self._change_list.index[0]))
        print(date_end_interval)

        # Initial buy (always start with a first buy)
        buy_price = self._change_list.iloc[0, 1]
        print(buy_price)
        self._investment.invest(buy_price, (self._budget / buy_price))

        print(self._investment.average_price(), self._investment.total_invested(), self._investment.number_of_share())

        # for date in self._change_list:


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
