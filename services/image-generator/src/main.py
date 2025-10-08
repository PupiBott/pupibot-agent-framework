from flask import Flask, request, jsonify
import os
import uuid
from providers.google_provider import generate as google_generate

app = Flask(__name__)
BASE_DIR = os.path.abspath("./data/images")

# Ensure BASE_DIR exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Function to validate and sanitize provider
def validate_provider(provider):
    if provider not in ["local", "google"]:
        raise ValueError("Invalid provider. Must be 'local' or 'google'.")
    return provider

# Endpoint to generate images
@app.route("/internal/images/generate", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        provider = data.get("provider")
        idempotency_key = data.get("idempotency_key")

        if not prompt or not provider or not idempotency_key:
            return jsonify({"error": "Missing required fields."}), 400

        # Validate provider
        validate_provider(provider)

        # Generate image based on provider
        if provider == "google":
            image_path = google_generate(prompt)
        else:
            # Placeholder for local provider logic
            image_path = os.path.join(BASE_DIR, f"{uuid.uuid4()}.png")
            with open(image_path, "wb") as f:
                f.write(b"PLACEHOLDER_IMAGE")

        image_id = str(uuid.uuid4())
        return jsonify({"image_id": image_id, "path": image_path}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)