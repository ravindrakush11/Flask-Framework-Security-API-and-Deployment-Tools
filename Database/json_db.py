from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@localhost/flask_database"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class DataItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    
    uc_list = db.Column(MutableDict.as_mutable(JSON), nullable = True)
    sub_uc_list = db.Column(MutableDict.as_mutable(JSON), nullable = True)
    use_case = db.Column(MutableDict.as_mutable(JSON), nullable = True)   
    
class JSON_Model(db.Model):
    id = db.Column(db.String(50), primary_key = True)
    json_data = db.Column(MutableDict.as_mutable(JSON), nullable = True)

with app.app_context():
    db.create_all()
    
    
@app.route('/api/save_data', methods=['POST'])
def save_data():
    try:
        data = request.get_json()
        
        application = data.get('application')
        industry = data.get('industry')
        region = data.get('region')

        if application and industry and region:
            new_data_item = DataItem(application=application, industry=industry, region=region #)
                                                ,uc_list=data.get('uc_list'),
                                                sub_uc_list = data.get('sub_uc_list'),
                                                use_case = data.get('use_case'))
            db.session.add(new_data_item)
            db.session.commit()       
            
            return jsonify({"status":200,"message": "Data saved successfully", "data": {"id": new_data_item.id}}), 400
        else:
            return jsonify({"status":200,"error": "Incomplete data provided"}), 400

    except Exception as e:
        return jsonify({"status":200,"error": str(e)}), 500   



@app.route('/json_data', methods = ['POST'])
def save_json_data():
    try:
        data = request.get_json()
        id_value = data.get('id')
        json_data = data.get('json_data')
        
        if id_value and json_data:
            new_data_item = JSON_Model(id=id_value, json_data=json_data)
            db.session.add(new_data_item)
            db.session.commit()

            return jsonify({"status":200,"message": "JSON data saved successfully", "data": {"id": new_data_item.id}}), 400
        else:
            return jsonify({"status":200,"error": "Incomplete or invalid data provided"}), 400

    except Exception as e:
        return jsonify({"status":200,"error": str(e)}), 500
  
  
  
# Endpoint to retrieve JSON data by ID
@app.route('/api/get_json_data/<string:id>', methods=['GET'])
def get_json_data_by_id(id):
    try:
        data_item = JSON_Model.query.get(id)

        if data_item:
            return jsonify({"status":200,"data": {"id": data_item.id, "json_data": data_item.json_data}}), 400
        else:
            return jsonify({"status":200,"error": "Data not found"}), 400

    except Exception as e:
        return jsonify({"status":200,"error": str(e)}), 500
    
# Endpoint to retrieve all JSON data
@app.route('/api/get_all_json_data', methods=['GET'])
def get_all_json_data():
    try:
        all_data_items = JSON_Model.query.all()
        data_list = [{"status":200,"id": item.id, "json_data": item.json_data} for item in all_data_items], 400

        return jsonify({"status":200,"data": data_list}), 400

    except Exception as e:
        return jsonify({"status":200,"error": str(e)}), 500
    

# Endpoint to retrieve values based on id, name, age, address, tags
@app.route('/api/get_data', methods=['GET'])
def get_data():
    try:
        # Get query parameters from the request
        id_value = request.args.get('id')
        name = request.args.get('name')
        age = request.args.get('age')
        address = request.args.get('address')
        tags = request.args.getlist('tags')
        title = request.args.getlist('title')
        description = request.args.getlist('description')

        # Build the query
        query = JSON_Model.query

        if id_value:
            query = query.filter_by(id=id_value)
        if name:
            query = query.filter(JSON_Model.json_data['name'].astext.ilike(f'%{name}%'))
        if age:
            query = query.filter(JSON_Model.json_data['age'].astext.ilike(f'%{age}%'))
        if address:
            query = query.filter(JSON_Model.json_data['address'].astext.ilike(f'%{address}%'))
        if tags:
            query = query.filter(JSON_Model.json_data['tags'].astext.ilike(f'%{"%".join(tags)}%'))

        if title:
            query = query.filter(JSON_Model.json_data['title'].astext.ilike(f'%{title}%'))
        if description:
            query = query.filter(JSON_Model.json_data['description'].astext.ilike(f'%{description}%'))
            
        
        # Execute the query
        result = query.all()

        # Format the result
        data_list = [{"id": item.id, "json_data": item.json_data} for item in result]

        return jsonify({"data": data_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

"""In the "Params" section, add the following key-value pairs based on your criteria:

Key: id, Value: 12345 (or any specific id you want to query)
Key: name, Value: John (or any specific name you want to query)
Key: age, Value: 30 (or any specific age you want to query)
Key: address, Value: Example City (or any specific address you want to query)
Key: tags, Value: tag1 (or any specific tag you want to query)"""

if __name__ == '__main__':
    # db.create_all()
    app.run(host='127.0.0.1', port=5010, debug=True)
