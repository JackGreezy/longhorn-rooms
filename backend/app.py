from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/test')
def test_route():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(port=5000)

