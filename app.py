from datetime import datetime, timezone
from flask import Flask, jsonify, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()  # uses the service account attached to Cloud Run

# Health check
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# Fetch all documents from 'entries' collection
@app.route("/entries", methods=["GET"])
def fetch_all_entries():
    entries_ref = db.collection("entries")
    docs = entries_ref.stream()
    
    entries = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return jsonify(entries)

# Add a new entry, using current UTC date
@app.route("/add_entry", methods=["POST"])
def add_entry():
    data = request.get_json()

    weight = data.get("weight")
    if weight is None:
        return jsonify({"error": "weight is required"}), 400

    # Get current UTC date
    created_on = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Add document to Firestore
    doc_ref = db.collection("entries").add({
        "created_on": created_on,
        "weight": weight
    })

    return jsonify({"id": doc_ref[1].id, "created_on": created_on, "message": "Entry added"}), 201