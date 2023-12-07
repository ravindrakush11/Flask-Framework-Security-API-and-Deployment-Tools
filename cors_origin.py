from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": 'http://localhost:3000'}})  #


@app.route('/hii', methods = ['GET'])
def data():
    return jsonify(message = 'data is not allowed')

@app.route('/api/data/', methods = ['GET'])
# @cross_origin(origin=['http://localhost:8000'], headers=['Content-Type'])
def get_data():
    return jsonify(message='Data from the API')

if __name__ == '__main__':
    app.run(debug = True, host = '192.168.11.89')