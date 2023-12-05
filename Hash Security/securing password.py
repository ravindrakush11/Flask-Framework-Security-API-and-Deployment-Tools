import os
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_bcrypt import Bcrypt

# Generate a secure key
secure_key = secrets.token_urlsafe(32)  # 32 bytes for a reasonably long key

# Generate a random 128-bit (16-byte) salt
# salt = secrets.token_bytes(16)

salt = secrets.SystemRandom()  #secure random number generator

# Never Print the secure key
# print("Generated Secure Key:", secure_key,'\n',"Generated Salt:", salt)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'secure_key')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", 'salt')

# mitigate certain types of cross-site request forgery (CSRF) and cross-site script inclusion (XSSI) attacks
app.config["REMEMBER_COOKIE_SAMESITE"] = "strict"
app.config["SESSION_COOKIE_SAMESITE"] = "strict"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/flask_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}

db = SQLAlchemy(app)   
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    


# Creating Tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Login successful
            return redirect(url_for('dashboard'))

        # Login unsuccessful
        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Retrieve the username from the session or however you store user information after login
    username = "username"  
    return render_template('dashboard.html', username=username)


if __name__ == "__main__":
    app.run(debug=True, port='5005')
