from flask import Flask, request, jsonify
import os

app = Flask(__name__)

STORAGE_DIR = "cloud_storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route("/upload_update", methods=["POST"])
def upload_update():
    round_no = request.form.get("round")
    weights = request.files.get("weights")
    bias = request.files.get("bias")

    if not round_no or not weights or not bias:
        return jsonify({"error": "Missing data"}), 400

    weights.save(f"{STORAGE_DIR}/weights_round_{round_no}.bin")
    bias.save(f"{STORAGE_DIR}/bias_round_{round_no}.bin")

    print(f"☁️ Stored FHE update for round {round_no}")
    return jsonify({"status": "stored"}), 200

@app.route("/")
def home():
    return "FHE Cloud Storage Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
