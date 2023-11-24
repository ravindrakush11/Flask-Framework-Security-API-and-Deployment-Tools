from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    print("Received token:", token)
    return tokens.get(token, None)

@app.route('/token', methods=['POST'])
@auth.login_required
def index():
    print("hello world")
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug= True, port=5001)
