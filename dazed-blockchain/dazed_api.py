from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from blockchain_core import DazedChain

app = Flask(__name__)
CORS(app)  # still include this

chain = DazedChain()

@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS"
    return response

@app.route("/chain", methods=["GET"])
def full_chain():
    try:
        chain_data = []

        print("🧱 Raw chain data:")
        for block in chain.all_blocks():
            print("🔎 Block:", block)  # <-- fixed debug line
            chain_data.append(block)

            block_info = {
                "index": getattr(block, "index", 0),
                "timestamp": getattr(block, "timestamp", 0),
                "transactions": getattr(block, "transactions", []),
                "nonce": getattr(block, "nonce", 0),
                "previous_hash": getattr(block, "previous_hash", ""),
                "hash": getattr(block, "hash", "")
            }
            chain_data.append(block_info)

        return jsonify({
            "chain": chain_data,
            "length": len(chain_data)
        })

    except Exception as e:
        print("❌ Error in /chain route:", e)
        return jsonify({"error": "Server error", "details": str(e)}), 500




@app.route("/balance/<address>", methods=["GET"])
def get_balance(address):
    balance = chain.ledger.get_balance(address)
    return jsonify({"address": address, "balance": balance}), 200

@app.route("/mine", methods=["POST"])
def mine_block():
    data = request.get_json()
    tx_type = data.get("type")  # 'mint' or 'transfer'
    from_addr = data.get("from")
    to_addr = data.get("to")
    amount = data.get("amount")

    if tx_type not in ["mint", "transfer"]:
        return jsonify({"error": "Invalid transaction type."}), 400

    tx = {"type": tx_type, "from": from_addr, "to": to_addr, "amount": amount}
    if tx_type == "mint":
        del tx["from"]  # Not needed for mint

    block = chain.add_block([tx])
    return jsonify({"message": "Block mined", "block": block}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
