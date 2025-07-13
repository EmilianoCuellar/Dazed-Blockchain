from flask import Flask, jsonify, request
from blockchain.dynamic_pricing import DazedCoin

app = Flask(__name__)

# Initialize the DazedCoin Dynamic Pricing System
dazed = DazedCoin()

@app.route('/token/price', methods=['GET'])
def get_price():
    return jsonify({
        'current_price': dazed.get_price()
    }), 200

@app.route('/token/marketcap', methods=['GET'])
def get_market_cap():
    return jsonify({
        'market_cap': dazed.market_cap()
    }), 200

@app.route('/token/buy', methods=['POST'])
def buy_dazed():
    data = request.get_json()
    address = data.get('wallet', '').strip()
    usd_amount = float(data.get('usd', 0))

    dazed.buy(address, usd_amount)

    return jsonify({
        'message': f'{usd_amount / dazed.get_price()} $Dazed purchased successfully!',
        'balance': dazed.balance_of(address),
        'current_price': dazed.get_price(),
        'market_cap': dazed.market_cap()
    }), 200

@app.route('/token/sell', methods=['POST'])
def sell_dazed():
    data = request.get_json()
    address = data.get('wallet', '').strip()
    dazed_amount = float(data.get('amount', 0))

    usd_received = dazed.sell(address, dazed_amount)

    return jsonify({
        'message': f'Sold {dazed_amount} $Dazed for ${usd_received} USD',
        'balance': dazed.balance_of(address),
        'current_price': dazed.get_price(),
        'market_cap': dazed.market_cap()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
