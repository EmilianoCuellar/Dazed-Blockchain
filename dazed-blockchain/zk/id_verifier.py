import hashlib

class SimpleZkID:
    def __init__(self):
        self.salt = "dazed"
        print(" SimpleZkID initialized with salt:", self.salt)

    def generate_commitment(self, secret_value):
        to_hash = f"{self.salt}-{secret_value}".encode()
        print("Hashing:", to_hash)
        return hashlib.sha256(to_hash).hexdigest()

    def verify_commitment(self, commitment, expected_value):
        print("DEBUG: Starting zk-ID verification")
        expected_hash = self.generate_commitment(expected_value)
        print("Expected Hash:", expected_hash)
        print("Received Commitment:", commitment)
        return commitment == expected_hash
