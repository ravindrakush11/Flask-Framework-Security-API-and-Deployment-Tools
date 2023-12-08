from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/flask_database"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Dummy_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(128))
    phone_no = db.Column(db.String(25))
    email = db.Column(db.String(20))
    
with app.app_context():
    db.create_all()
    
@app.route('/', methods = ['POST'])
def save_data():
    
    data = request.get_json()
    id  = data.get('id')
    name = data.get('name')
    address = data.get('address')
    phone_no = data.get('phone_no')
    email = data.get('email')
    
    item = Dummy_User(name=name, id=id, address = address, phone_no = phone_no, email=email)
    db.session.add(item)
    db.session.commit()
    
    return jsonify("data added succesfully")

if __name__ == '__main__':
    app.run(debug=True,port = '5007')
    
# Migration Commands 
# flask --app file_name db init 
# flask --app file_name db migrate
# flask --app file_name db upgrade

# Add a new column in existing table
# flask --app file_name db migrate -m "Add column_name to table_name" 
# flask --app file_name db revision   #When migration files are missing

