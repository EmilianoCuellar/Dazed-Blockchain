import requests
import time

API = "http://localhost:5002"

# Auto-mine PoP and zk-ID reward blocks for testing
TEST_TRANSACTIONS = [
    {"type": "mint", "to": "0xDispensary1", "amount": 420},
    {"type": "mint", "to": "0xUserZK1", "amount": 50},
    {"type": "transfer", "from": "0xUserZK1", "to": "0xUser2", "amount": 25},
    {"type": "mint", "to": "0xDispensary2", "amount": 420},
    {"type": "transfer", "from": "0xUser2", "to": "0xDispensary1", "amount": 10}
]

print("🚀 Starting auto-miner...\n")
for tx in TEST_TRANSACTIONS:
    res = requests.post(f"{API}/mine", json=tx)
    if res.status_code == 201:
        print(f"✅ Block mined for: {tx}")
    else:
        print(f"❌ Failed to mine: {tx} | Reason: {res.json()}")
    time.sleep(1)

print("\n🏁 Test mining complete.")
