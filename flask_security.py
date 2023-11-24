from flask import Flask
from flask_httpauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = '123fdshfiohdsghdskj4'
auth = HTTPDigestAuth()

users = {
    "Abhay": "abh@123",
    "David": "dav@123"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/verify', methods = ['POST'])
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run(debug=True)