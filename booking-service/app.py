from flask import Flask, request, jsonify
import requests
import os
import random

app = Flask(__name__)

PAYMENT_SERVICE_URL = os.environ.get("PAYMENT_SERVICE_URL", "http://localhost:8081")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "booking-service"}), 200

@app.route("/book", methods=["POST"])
def book():
    data = request.get_json()
    hotel_name = data.get("hotel_name", "Unknown Hotel")
    amount = data.get("amount", 100)

    booking_id = f"booking_{random.randint(1000,9999)}"

    # Call payment-service to charge the customer
    try:
        response = requests.post(
            f"{PAYMENT_SERVICE_URL}/charge",
            json={"amount": amount},
            timeout=5
        )
        payment_result = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({
            "booking_id": booking_id,
            "status": "failed",
            "reason": f"payment-service unreachable: {str(e)}"
        }), 503

    if response.status_code == 200 and payment_result.get("status") == "success":
        return jsonify({
            "booking_id": booking_id,
            "hotel_name": hotel_name,
            "status": "confirmed",
            "payment": payment_result
        }), 200
    else:
        return jsonify({
            "booking_id": booking_id,
            "status": "payment_failed",
            "payment": payment_result
        }), 402

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
