import hashlib
import json
from time import time

class Block:
    def __init__(self, index, transactions, proof, previous_hash, metrc_id=None):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash
        self.metrc_id = metrc_id  # Part of PoP

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash,
            'metrc_id': self.metrc_id
        }

    def hash(self):
        block_string = json.dumps(self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
