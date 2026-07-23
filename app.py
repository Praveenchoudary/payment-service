from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "payment-service"}), 200

@app.route("/charge", methods=["POST"])
def charge():
    data = request.get_json()
    amount = data.get("amount", 0)

    # Simulate a payment (90% success rate)
    success = random.random() > 0.1

    if success:
        return jsonify({
            "status": "success",
            "transaction_id": f"txn_{random.randint(1000,9999)}",
            "amount": amount
        }), 200
    else:
        return jsonify({"status": "failed", "reason": "card_declined"}), 402

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
