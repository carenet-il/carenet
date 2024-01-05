from flask import Flask

app = Flask(__name__)


@app.route('/document/insertMany', methods=['POST'])
def insert_many():
    return {"ok": 200}


@app.route('/document/search', methods=['POST'])
def search():
    return {"ok": 200}
