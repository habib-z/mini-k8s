from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Read from a file and simulate persistence
DATA_FILE = '/data/storage.txt'

# Initialize data file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        f.write("Initial Data")

@app.route('/data', methods=['GET'])
def get_data():
    with open(DATA_FILE, 'r') as f:
        data = f.read()
    return jsonify({"data": data})

@app.route('/data', methods=['POST'])
def update_data():
    new_data = request.json.get('data', '')
    with open(DATA_FILE, 'w') as f:
        f.write(new_data)
    return jsonify({"message": "Data updated"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
