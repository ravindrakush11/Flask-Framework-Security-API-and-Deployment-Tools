from flask import Flask
from waitress import serve

# https://nagasudhir.blogspot.com/2022/10/waitress-as-flask-server-wsgi.html
app = Flask(__name__)

@app.route('/')
def index():
    return 'This is a deployment server!!!'

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000, threads=2, url_prefix="/my-app")