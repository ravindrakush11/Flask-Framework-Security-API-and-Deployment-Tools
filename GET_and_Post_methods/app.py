from flask import Flask, request, jsonify

app = Flask(__name__)

# GET endpoint: read-only:      http://localhost:5000/greet?name=Alice
@app.route('/greet_get', methods=['GET'])
def greet_get():
    name = request.args.get('name', 'Guest')  # query param
    return jsonify({
        'method': 'GET',
        'message': f'Hello, {name}!'
    })

# POST endpoint: data submission through Postman
@app.route('/greet_post', methods=['POST'])
def greet_postman():
    data = request.get_json()
    name = data.get('name', 'Guest')  # JSON body
    return jsonify({
        'method': 'POST',
        'message': f'Hello, {name}!'
    })


# POST endpoint: data submission throught html form
@app.route('/greet_form', methods=['POST'])
def greet_html_form():
    # data = request.get_json()
    # name = data.get('name', 'Guest')  # JSON body
    name = request.form.get('name', 'Guest')
    return jsonify({
        'method': 'POST',
        'message': f'Hello, {name}!'
    })


if __name__ == '__main__':
    app.run(debug=True)
