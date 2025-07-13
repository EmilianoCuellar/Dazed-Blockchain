from uuid import uuid4
from time import time

class Transaction:
    def __init__(self, sender, recipient, amount, product_id=None):
        self.id = str(uuid4()).replace('-', '')
        self.timestamp = time()
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.product_id = product_id  # Optional link to METRC

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'product_id': self.product_id
        }
