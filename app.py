from datetime import datetime, timezone
from flask import Flask, jsonify, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()  # Uses the service account attached to Cloud Run

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    # Validate all required fields
    required_fields = ["date", "weight"]
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Validate and normalize date
    try:
        day = datetime.strptime(data["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD"}), 400

    # Validate weight
    try:
        weight = float(data["weight"])
        if weight <= 0:
            return jsonify({"error": "Weight must be greater than 0"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid weight. Please enter a number"}), 400

    # Use normalized date for document ID
    doc_ref = db.collection("bodyweight").document(day.strftime("%Y-%m-%d"))

    # Prevent duplicate entries
    if doc_ref.get().exists:
        return jsonify({"error": "Entry already exists for this date"}), 409

    # Update database
    doc_ref.create({
    "day": day,
    "weight": weight
    })

    return jsonify({
        "id": doc_ref.id,
        "day": day.strftime("%Y-%m-%d"),
        "weight": weight,
        "message": "Entry added"
    }), 201