from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import os
app = Flask(__name__)
# Generate a secure random secret key
app.config['SECRET_KEY'] = os.urandom(24)

secret_key = app.config.get('SECRET_KEY')
print(f"Secret Key: {secret_key}")
# Setup the Flask-JWT-Extended extension
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200  


if __name__ == "__main__":
    app.run(debug=True)
    

# Arbitrary token generation by the secret key
import jwt
import datetime

# Replace 'your_secret_key_here' with your actual secret key
secret_key = 'your_secret_key_here'

# Replace 'your_username' with the actual identity you want to include in the token
token_data = {
    'identity': 'username',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
}

token = jwt.encode(token_data, secret_key, algorithm='HS256')
print(token)
