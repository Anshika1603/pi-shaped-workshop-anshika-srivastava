from flask import Flask, jsonify
import os

app = Flask(__name__)

# Demo insecure hardcoded secret (intentional for scanning)
API_KEY = "SUPER_SECRET_HARDCODED_KEY_12345"

@app.route("/")
def hello():
    return jsonify({"message": "hello from vulnerable demo app", "api_key_preview": API_KEY[:8]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
