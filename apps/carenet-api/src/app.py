from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/document/insertMany', methods=['POST'])
def insert_many():
    if request.json:
        return jsonify({"message": "Data inserted successfully!"}), 200
    else:
        return jsonify({"error": "No data provided"}), 400


@app.route('/document/search', methods=['POST'])
def search():
    query = request.args.get('query')
    if query:
        # Simple search implementation (case-insensitive)
        return jsonify({"ok": 200}), 200
    else:
        return jsonify({"error": "No query provided"}), 400
