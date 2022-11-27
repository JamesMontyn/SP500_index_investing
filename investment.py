

class Investment:
    def __init__(self):
        self._total_invested = 0
        self._number_of_shares = 0

    def invest(self, share_price, quantity):
        self._total_invested += (share_price*quantity)
        self._number_of_shares += quantity

    def average_price(self):
        return self._total_invested / self._number_of_shares

    def total_invested(self):
        return self._total_invested

    def number_of_share(self):
        return self._number_of_shares
