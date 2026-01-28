from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Directory to store encrypted updates
CLOUD_DIR = "cloud_storage"
os.makedirs(CLOUD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "FHE Cloud Storage Running"

@app.route("/upload", methods=["POST"])
def upload_encrypted_update():
    round_no = request.form.get("round")

    weights_file = request.files.get("weights")
    bias_file = request.files.get("bias")

    if not round_no or not weights_file or not bias_file:
        return jsonify({"error": "Missing data"}), 400

    weights_path = f"{CLOUD_DIR}/weights_round_{round_no}.bin"
    bias_path = f"{CLOUD_DIR}/bias_round_{round_no}.bin"

    weights_file.save(weights_path)
    bias_file.save(bias_path)

    print(f"☁️ Encrypted FHE update stored for round {round_no}")

    return jsonify({
        "status": "stored",
        "round": round_no
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
