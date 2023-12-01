from flask import Flask, jsonify, request, make_response
from functools import wraps

# https://www.youtube.com/watch?v=VW8qJxy4XcQ&ab_channel=PrettyPrinted

app = Flask(__name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and  auth.username == 'username' and auth.password == 'password':
            return f(*args, **kwargs)
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm = "Login Required"'})
    return decorated

@app.route('/page')
@auth_required
def page():
    return '<h1> You are on the page!</h1>'

@app.route('/other page')
def other_page():
    return 'You are on the other page'


if __name__ == '__main__':
    app.run(debug=True, port='5003')