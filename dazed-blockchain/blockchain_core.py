import time
import json
import hashlib
import os
from ledger import Ledger

CHAIN_FILE = "blockchain_data/chain.json"

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # list of {from, to, amount, type}
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.to_dict(include_hash=False), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self, include_hash=True):
        data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        if include_hash:
            data["hash"] = self.hash
        return data

    @classmethod
    def from_dict(cls, data):
        block = cls(data["index"], data["transactions"], data["previous_hash"])
        block.timestamp = data["timestamp"]
        block.nonce = data["nonce"]
        block.hash = data["hash"]
        return block

class DazedChain:
    def __init__(self):
        self.ledger = Ledger()
        os.makedirs(os.path.dirname(CHAIN_FILE), exist_ok=True)

        if os.path.exists(CHAIN_FILE):
            with open(CHAIN_FILE, 'r') as f:
                self.chain = json.load(f)
        else:
            from genesis_block_setup import GenesisBlock
            genesis = GenesisBlock()
            genesis.save_to_disk()
            self.chain = [genesis.to_dict()]
            self._save_chain()

    def _save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        last_hash = self.last_block()['hash']
        new_block = Block(len(self.chain), transactions, last_hash)

        for tx in transactions:
            if tx['type'] == 'mint':
                self.ledger.mint(tx['to'], tx['amount'])
            elif tx['type'] == 'transfer':
                self.ledger.transfer(tx['from'], tx['to'], tx['amount'])

        self.chain.append(new_block.to_dict())
        self._save_chain()
        return new_block.to_dict()

    def all_blocks(self):
        return self.chain
