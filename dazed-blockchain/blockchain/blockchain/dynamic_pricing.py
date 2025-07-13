import math

class DazedCoin:
    _instance = None  # Global instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DazedCoin, cls).__new__(cls)
            cls._instance.total_supply = 420_000_000
            cls._instance.balances = {}
            cls._instance.base_price = 0.05  # Initial base price
            cls._instance.current_price = cls._instance.base_price
        return cls._instance

    def mint(self, address, amount):
        if address not in self.balances:
            self.balances[address] = 0
        self.balances[address] += amount

    def transfer(self, sender, recipient, amount):
        if sender not in self.balances or self.balances[sender] < amount:
            raise ValueError("Insufficient balance.")
        self.balances[sender] -= amount
        if recipient not in self.balances:
            self.balances[recipient] = 0
        self.balances[recipient] += amount

    def balance_of(self, address):
        return self.balances.get(address, 0)

    def buy(self, address, usd_amount):
        dazed_purchased = usd_amount / self.current_price
        self.mint(address, dazed_purchased)
        self.adjust_price(dazed_purchased, increase=True)

    def sell(self, address, dazed_amount):
        if self.balance_of(address) < dazed_amount:
            raise ValueError("Insufficient balance.")
        usd_received = dazed_amount * self.current_price
        self.transfer(address, "Dazed Treasury", dazed_amount)
        self.adjust_price(dazed_amount, increase=False)
        return usd_received

    def adjust_price(self, volume, increase=True):
        impact = (volume / self.total_supply) * 0.05  # 0.05% price impact per 1% volume
        if increase:
            self.current_price += impact
        else:
            self.current_price -= impact

    def get_price(self):
        return round(self.current_price, 6)

    def market_cap(self):
        circulating_supply = sum(self.balances.values())
        return round(circulating_supply * self.current_price, 2)
