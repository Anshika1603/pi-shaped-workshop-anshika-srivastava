from flask import Flask, request, jsonify
import sqlite3, os

app = Flask(__name__)
app.config['SECRET_KEY'] = "dev-default-key"
app.debug = True

DB = 'example.db'
def init_db():
    c = sqlite3.connect(DB).cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT)')
    c.execute("INSERT INTO users (username) VALUES ('alice')")
    sqlite3.connect(DB).commit()

@app.route('/')
def i(): return "Vulnerable Flask demo app"

@app.route('/user')
def user():
    n = request.args.get('name','')
    cur = sqlite3.connect(DB).cursor()
    cur.execute(f"SELECT id, username FROM users WHERE username = '{n}'")
    r = cur.fetchone()
    return jsonify({'id': r[0], 'user': r[1]}) if r else ('not found', 404)

@app.route('/eval')
def do_eval():
    return jsonify(result=str(eval(request.args.get('code',''))))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
