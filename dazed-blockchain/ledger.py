import os
import json

LEDGER_FILE = "blockchain_data/ledger.json"

class Ledger:
    def __init__(self):
        os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)
        if not os.path.exists(LEDGER_FILE):
            self.balances = {
                "0xFounder": 84000000,
                "Dazed Treasury": 336000000
            }
            self._save()
        else:
            with open(LEDGER_FILE, 'r') as f:
                self.balances = json.load(f)

    def _save(self):
        with open(LEDGER_FILE, 'w') as f:
            json.dump(self.balances, f, indent=4)

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def transfer(self, sender, recipient, amount):
        if self.get_balance(sender) < amount:
            raise ValueError("Insufficient balance")

        self.balances[sender] -= amount
        self.balances[recipient] = self.get_balance(recipient) + amount
        self._save()

    def mint(self, address, amount):
        self.balances[address] = self.get_balance(address) + amount
        self._save()

    def all_balances(self):
        return self.balances
