from blockchain.token import DazedCoin

class RewardSystem:
    def __init__(self):
        self.dazed = DazedCoin()  # Singleton global DazedCoin

    def grant_reward(self, address, action="verified_user"):
        reward_amount = 50
        print(f"Granting {reward_amount} $Dazed to {address}")
        self.dazed.mint(address, reward_amount)
        print(f"New balance for {address}: {self.dazed.balance_of(address)} $Dazed")

    def get_rewards(self, address):
        print(f"Fetching balance for {address}: {self.dazed.balance_of(address)} $Dazed")
        return self.dazed.balance_of(address)
