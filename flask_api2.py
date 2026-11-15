from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Second Flask API endpoint!"})

@app.route('/health')
def health():
    return jsonify({"status": "Second Flask API is running healthy inside Kubernetes. 15 Nov 10:46 AM"}), 200

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5001)