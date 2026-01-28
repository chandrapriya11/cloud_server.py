from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Folder to store encrypted updates
CLOUD_DIR = "cloud_storage"
os.makedirs(CLOUD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "FHE Cloud Storage Running"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()

    round_no = data["round"]
    weights = bytes(data["weights"])
    bias = bytes(data["bias"])

    with open(f"{CLOUD_DIR}/weights_round_{round_no}.bin", "wb") as f:
        f.write(weights)

    with open(f"{CLOUD_DIR}/bias_round_{round_no}.bin", "wb") as f:
        f.write(bias)

    print(f"☁️ Encrypted update stored for round {round_no}")
    return jsonify({"status": "stored"})
