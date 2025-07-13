from flask import Flask, request, jsonify
from flask_cors import CORS
from blockchain_core import DazedChain

app = Flask(__name__)
CORS(app)

chain = DazedChain()

@app.route('/buy', methods=['POST'])
def buy_tokens():
    data = request.get_json()
    wallet = data.get('wallet')
    amount = data.get('amount')

    if not wallet or not amount:
        return jsonify({"error": "Missing wallet or amount"}), 400

    tx = {
        "to": wallet,
        "amount": amount,
        "type": "mint",
        "note": "User purchased tokens"
    }

    block = chain.add_block([tx])
    return jsonify({
        "message": f"Purchased {amount} $Dazed",
        "block": block,
        "wallet": wallet,
        "amount": amount
    }), 200

@app.route('/sell', methods=['POST'])
def sell_tokens():
    data = request.get_json()
    wallet = data.get('wallet')
    amount = data.get('amount')
    recipient = data.get('recipient', 'Dazed Treasury')

    if not wallet or not amount:
        return jsonify({"error": "Missing wallet or amount"}), 400

    tx = {
        "from": wallet,
        "to": recipient,
        "amount": amount,
        "type": "transfer",
        "note": "User sold tokens"
    }

    block = chain.add_block([tx])
    return jsonify({
        "message": f"Sold {amount} $Dazed",
        "block": block,
        "wallet": wallet,
        "amount": amount
    }), 200

if __name__ == '__main__':
    app.run(port=5004)
