from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Your secret key'

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.args.get('token')
    
    if not token:
      return jsonify({"message": "Token is missing!"}), 403
    
    try:
      data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
      return jsonify({"message": "Token is invalid!"}), 403
    
    return f(*args, **kwargs)
  
  return decorated
  

@app.route('/unprotected')
def unprotected():
  return jsonify({"message": "This can view everyone"})

@app.route('/protected')
@token_required
def protected():
  return jsonify({"message": "Only available for the valid token holders"})

@app.route('/login')
def login():
  auth = request.authorization

  if auth and auth.password == 'pass':
    token = jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'], algorithm='HS256')
    
    # Automatically decode the tokens
    return jsonify({'token': token}) #token.decode('utf-8')
  
  return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})


if __name__ == '__main__':
  app.run(debug=True)
