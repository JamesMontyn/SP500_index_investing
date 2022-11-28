class Investment:
    """Investment Class holds the data of an investment by an Investor.

        Private Variables
        -----------------
        _total_invested: int
            the total money deposited/invested for this investment

        _number_of_shares: int
            the total number of shares of SPY held in this investment
    """
    def __init__(self):
        """Constructor Investment"""
        self._total_invested = 0
        self._number_of_shares = 0

    def invest(self, share_price, quantity):
        """Adds to investment

        Parameters
        ----------
        share_price: int
            the share price of the added investment

        quantity: int
            the number of shares of SPY added
        """
        self._total_invested += (share_price*quantity)
        self._number_of_shares += quantity

    def average_price(self):
        """Getter average share price of SPY of investment"""
        return self._total_invested / self._number_of_shares

    def total_invested(self):
        """Getter total invested"""
        return self._total_invested

    def number_of_share(self):
        """Getter number of shares"""
        return self._number_of_shares
