from flask import Flask, request, jsonify
import os
import pickle
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = "SUPERSECRET123"

app.debug = True

DB = 'example.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, secret TEXT)')
    c.execute("INSERT INTO users (username, secret) VALUES ('alice', 'alice-secret')")  # intentional
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return "Vulnerable Flask demo app"

@app.route('/user')
def get_user():
    name = request.args.get('name', '')
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    query = f"SELECT id, username FROM users WHERE username = '{name}'"
    try:
        c.execute(query)
        row = c.fetchone()
        conn.close()
        if row:
            return jsonify({'id': row[0], 'username': row[1]})
        return jsonify({'error': 'not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/eval')
def do_eval():
    code = request.args.get('code', '')
    result = eval(code)
    return jsonify({'result': str(result)})

@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.get_data()
    obj = pickle.loads(data)
    return jsonify({'type': str(type(obj))})

@app.route('/config')
def dump_config():
    return jsonify({k: str(v) for k, v in app.config.items()})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
