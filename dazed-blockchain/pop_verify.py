from flask import Flask, request, jsonify
from blockchain_core import DazedChain
from zk.id_verifier import SimpleZkID

app = Flask(__name__)
chain = DazedChain()
zk = SimpleZkID()

@app.route("/pop-verify", methods=["POST"])
def verify_product():
    data = request.get_json()
    wallet = data.get("wallet")
    metrc_id = data.get("metrc_id")
    commitment = data.get("commitment")

    if not wallet or not metrc_id or not commitment:
        return jsonify({"error": "Missing wallet, METRC ID, or zk commitment"}), 400

    if len(metrc_id) != 24 or not metrc_id.isdigit():
        return jsonify({"error": "Invalid METRC ID format"}), 400

    # zk-ID validation
    if not zk.verify_commitment(commitment, "verified-age-21"):
        return jsonify({
            "verified": False,
            "message": "User is not zk-verified to be 21+",
            "rewarded": False
        }), 403

    reward_amount = 420
    tx = {
        "type": "mint",
        "to": wallet,
        "amount": reward_amount,
        "note": f"Verified product METRC {metrc_id}"
    }

    block = chain.add_block([tx])

    return jsonify({
        "message": "Product verified and reward minted",
        "metrc_id": metrc_id,
        "reward": reward_amount,
        "wallet": wallet,
        "verified": True,
        "block": block
    }), 201

if __name__ == "__main__":
    app.run(port=5003)
