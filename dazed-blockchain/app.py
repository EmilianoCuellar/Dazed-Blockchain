from blockchain.token import DazedCoin
from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4

from blockchain.node import DazedBlockchain
from blockchain.transaction import Transaction
from blockchain.reward import RewardSystem
from zk.id_verifier import SimpleZkID
zk = SimpleZkID()

# Initialize core objects
app = Flask(__name__)
CORS(app)
blockchain = DazedBlockchain()
rewards = RewardSystem()
token = DazedCoin()

# Unique node ID for simulation
node_identifier = str(uuid4()).replace('-', '')

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Dazed Blockchain API is running'}), 200


@app.route('/zk-id/verify', methods=['POST'])
def verify_zk_id():
    data = request.get_json()
    commitment = data.get('commitment', '').strip()
    address = data.get('wallet', '').strip()

    expected_value = "verified-age-21"

    if commitment == expected_value:
        rewards.grant_reward(address, action="verified_user")
        print(f"Reward granted. Current balance for {address}: {rewards.get_rewards(address)} $Dazed")
        return jsonify({
            'verified': True,
            'message': 'ZK ID proof accepted. Reward granted!',
            'rewarded': True
        }), 200
    else:
        return jsonify({
            'verified': False,
            'message': 'Invalid zk-proof. No rewards granted.',
            'rewarded': False
        }), 403



@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.get_json()
    metrc_id = data.get('metrc_id')
    if not metrc_id:
        return jsonify({'error': 'METRC ID is required'}), 400

    block = blockchain.mine_block(metrc_id)
    return jsonify({
        'message': 'New block mined!',
        'block': block.to_dict()
    }), 201

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing values'}), 400

    txn = Transaction(
        sender=data['sender'],
        recipient=data['recipient'],
        amount=data['amount'],
        product_id=data.get('product_id')
    )
    blockchain.current_transactions.append(txn.to_dict())
    return jsonify({'message': f'Transaction will be added to Block {blockchain.last_block.index + 1}'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.to_dict(),
        'length': len(blockchain.chain)
    }), 200

@app.route('/reward', methods=['POST'])
def reward_user():
    data = request.get_json()
    address = data.get('address')
    action = data.get('action', 'product_verified')

    if not address:
        return jsonify({'error': 'Address is required'}), 400

    amount = rewards.grant_reward(address, action)
    return jsonify({
        'message': f'{amount} tokens rewarded for action: {action}',
        'total_rewards': rewards.get_rewards(address)
    }), 200

@app.route('/token/mint', methods=['POST'])
def mint_token():
    data = request.get_json()
    address = data.get('address')
    amount = data.get('amount')
    try:
        minted = token.mint(address, amount)
        return jsonify({'message': f'{minted} $Dazed tokens minted to {address}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/token/transfer', methods=['POST'])
def transfer_token():
    data = request.get_json()
    sender = data.get('sender')
    recipient = data.get('recipient')
    amount = data.get('amount')
    try:
        token.transfer(sender, recipient, amount)
        return jsonify({'message': f'{amount} $Dazed transferred from {sender} to {recipient}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/token/burn', methods=['POST'])
def burn_token():
    data = request.get_json()
    address = data.get('address')
    amount = data.get('amount')
    try:
        burned = token.burn(address, amount)
        return jsonify({'message': f'{burned} $Dazed tokens burned from {address}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/token/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = token.get_balance(address)
    return jsonify({'address': address, 'balance': balance}), 200


@app.route('/rewards/<address>', methods=['GET'])
def get_rewards(address):
    return jsonify({
        'address': address,
        'rewards': rewards.get_rewards(address)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    
