# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from base64 import b64encode
import io

from model import upscale_image
from cartoonify import cartoonify_image  # <-- new import

app = Flask(__name__)
CORS(app)

@app.route("/upscale", methods=["POST"])
def upscale_route():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    try:
        img = Image.open(request.files["image"].stream).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Invalid image: {e}"}), 400

    try:
        result = upscale_image(img)
    except Exception as e:
        return jsonify({"error": f"Upscaling failed: {e}"}), 500

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    b64 = b64encode(buf.getvalue()).decode("utf-8")
    return jsonify({"image": b64})

@app.route("/cartoonify", methods=["POST"])
def cartoonify_route():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    try:
        img = Image.open(request.files["image"].stream).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Invalid image: {e}"}), 400

    try:
        result = cartoonify_image(img)
    except Exception as e:
        return jsonify({"error": f"Cartoonify failed: {e}"}), 500

    buf = io.BytesIO()
    result.save(buf, format="PNG")
    b64 = b64encode(buf.getvalue()).decode("utf-8")
    return jsonify({"image": b64})

if __name__ == "__main__":
    app.run(debug=True)
