class DazedCoin:
    _instance = None  # Global instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DazedCoin, cls).__new__(cls)
            cls._instance.total_supply = 420_000_000
            cls._instance.balances = {}
        return cls._instance

    def mint(self, address, amount):
        if address not in self.balances:
            self.balances[address] = 0
        self.balances[address] += amount

    def balance_of(self, address):
        return self.balances.get(address, 0)

    def burn(self, address, amount):
        if self.balances.get(address, 0) < amount:
            raise Exception("Insufficient balance to burn.")
        self.balances[address] -= amount
        self.burned += amount
        self.circulating_supply -= amount
        return amount

    def transfer(self, sender, recipient, amount):
        if self.balances.get(sender, 0) < amount:
            raise Exception("Insufficient balance to transfer.")
        self.balances[sender] -= amount
        self._add_balance(recipient, amount)
        return amount

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def _add_balance(self, address, amount):
        if address not in self.balances:
            self.balances[address] = 0
        self.balances[address] += amount
