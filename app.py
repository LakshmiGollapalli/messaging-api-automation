from flask import Flask, request, jsonify
from services.message_service import MessageService
from error_handlers import register_error_handlers
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


app = Flask(
    __name__,
    instance_path=INSTANCE_DIR,
    instance_relative_config=True
    )
# old logic tag v1.0
# Inject FakeProvider into service (Dependency Injection)
# provider = FakeProvider()
# service = MessageService(provider)


# Initialize MessageService; it will read providers from config
service = MessageService()
register_error_handlers(app)


@app.route("/")
def root():
    return {
        "service": "message-service",
        "version": "1.0",
        "status": "running"
    }, 200


@app.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "service": "message system",
        "providers": [
            "FastMessageProvider",
            "ReliableMessageProvider"]
    }, 200


@app.route("/messages", methods=["POST"])
def send_message():
    """
    POST /messages

    201 -> Message created
    400 -> Invalid input
    503 -> Provider failure
    """

    data = request.json
    response, status = service.create_message(
        data.get("receiver"),
        data.get("content")
    )
    return jsonify(response), status


@app.route("/messages/<int:message_id>", methods=["GET"])
def get_message(message_id):
    """
    GET /messages/<id>

    200 -> Success
    404 -> Not found
    """
    response, status = service.get_message(message_id)
    return jsonify(response), status


@app.route("/delivery-update", methods=["POST"])
def webhook_update():
    """
    Simulated Webhook Endpoint.

    External provider calls this endpoint.

    200 -> Status updated
    404 -> Provider ID not found
    400 -> Invalid state transition
    """
    data = request.json
    response, status = service.update_status(
        data.get("provider_id"),
        data.get("status"),
        data.get("timestamp")
    )
    return jsonify(response), status


if __name__ == "__main__":
    # 127.0.0.1 means only accessible locally
    # Port 5000 is default Flask development port
    app.run(host="0.0.0.0", port=5000, debug=True)
