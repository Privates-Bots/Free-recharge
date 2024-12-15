from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({'message': 'Hello, Vercel! This is the /test endpoint.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
