from flask import Flask, jsonify
import os

app = Flask(__name__)

# Load secrets from environment (no hardcoded secret)
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-placeholder")
API_KEY = os.environ.get("API_KEY", None)

app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/")
def hello():
    return jsonify({
        "message": "hello from demo app",
        "api_key_present": bool(API_KEY)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
