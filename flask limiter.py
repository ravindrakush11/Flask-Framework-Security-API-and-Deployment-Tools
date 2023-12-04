from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# https://flask-limiter.readthedocs.io/en/stable/index.html
# https://www.youtube.com/watch?v=vQleDvTM5xA&list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX&index=52&ab_channel=PrettyPrinted

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day"],
    application_limits_cost=lambda: 2,
    fail_on_first_breach=True,
    on_breach=lambda _: jsonify({'message': 'Rate limit breached!'}),
    request_identifier=lambda: get_remote_address(),   #  create a custom identifier for a request
    default_limits_cost=1
)

@app.route('/api')
@limiter.limit('5 per minute')
def api():
    return 'This is the response from API'

if __name__ == '__main__':
    app.run(debug=True, port=5005)