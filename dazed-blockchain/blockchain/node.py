import json
import hashlib
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from .block import Block

class DazedBlockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], 100, '1', metrc_id='000000000000000000000000')
        self.chain.append(genesis_block)

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_transaction(self, sender, recipient, amount, product_id=None):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'product_id': product_id
        })
        return self.last_block.index + 1

    def mine_block(self, metrc_id):
        last_block = self.last_block
        proof = self.proof_of_product(last_block.proof, metrc_id)
        block = Block(len(self.chain), self.current_transactions, proof, last_block.hash(), metrc_id)
        self.current_transactions = []
        self.chain.append(block)
        return block

    def proof_of_product(self, last_proof, metrc_id):
        """
        PoP = Proof of Product
        Simple PoW-style algo, but tied to a 24-digit METRC ID.
        """
        proof = 0
        while self.valid_proof(last_proof, proof, metrc_id) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof, metrc_id):
        guess = f'{last_proof}{proof}{metrc_id}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "4200"  # PoP difficulty (can be adjusted)

    @property
    def last_block(self):
        return self.chain[-1]

    def to_dict(self):
        return [block.to_dict() for block in self.chain]
