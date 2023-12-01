from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# https://flask-limiter.readthedocs.io/en/stable/index.html

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address,app=app,  default_limits=["10 per day", "1 per hour"], )

@app.route('/api')
@limiter.limit('3 per day', override_defaults=False, error_message = "You have consumed all the tokens pls wait for some time", )
def api():
    return 'This is the response from API'

if __name__ == '__main__':
    app.run(debug=True, port=5005)