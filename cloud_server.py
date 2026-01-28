from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ==============================
# Cloud storage directory
# ==============================
CLOUD_DIR = "cloud_storage"
os.makedirs(CLOUD_DIR, exist_ok=True)

# ==============================
# Health check
# ==============================
@app.route("/")
def home():
    return "FHE Cloud Storage Running"

# ==============================
# Upload encrypted FHE updates
# ==============================
@app.route("/upload", methods=["POST"])
def upload_encrypted_update():
    round_no = request.form.get("round")
    weights_file = request.files.get("weights")
    bias_file = request.files.get("bias")

    if not round_no or not weights_file or not bias_file:
        return jsonify({"error": "Missing data"}), 400

    weights_path = os.path.join(CLOUD_DIR, f"weights_round_{round_no}.bin")
    bias_path = os.path.join(CLOUD_DIR, f"bias_round_{round_no}.bin")

    weights_file.save(weights_path)
    bias_file.save(bias_path)

    print(f"☁️ Encrypted FHE update stored for round {round_no}")

    return jsonify({
        "status": "stored",
        "round": round_no
    }), 200

# ==============================
# LIST FILES IN NEAT JSON FORMAT
# ==============================
@app.route("/files", methods=["GET"])
def list_files():
    files = os.listdir(CLOUD_DIR)
    result = {}

    for file in files:
        if "_round_" in file:
            file_type = file.split("_round_")[0]     # weights / bias
            round_no = file.split("_round_")[1].split(".")[0]
            round_key = f"round_{round_no}"

            if round_key not in result:
                result[round_key] = {}

            result[round_key][file_type] = file

    return jsonify(result), 200

# ==============================
# Run server (Render handles port)
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
