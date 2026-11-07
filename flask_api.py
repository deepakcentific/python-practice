from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Sample Flask API endpoint!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy. 5:55 PM"}), 200

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)