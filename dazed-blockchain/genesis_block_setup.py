import json
import time
import hashlib
import os

GENESIS_FILE = "blockchain_data/genesis_block.json"

class GenesisBlock:
    def __init__(self):
        self.index = 0
        self.timestamp = time.time()
        self.transactions = [
            {"to": "0xFounder", "amount": 84000000},  # Founder allocation (20%)
            {"to": "Dazed Treasury", "amount": 336000000}  # Treasury, rewards, public
        ]
        self.previous_hash = "0" * 64
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def save_to_disk(self):
        os.makedirs(os.path.dirname(GENESIS_FILE), exist_ok=True)
        with open(GENESIS_FILE, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        print("✅ Genesis block created and saved.")

if __name__ == "__main__":
    genesis = GenesisBlock()
    genesis.save_to_disk()
