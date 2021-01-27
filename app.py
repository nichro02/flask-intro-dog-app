#This is the entry point file

from flask import Flask, jsonify, request, g
from flask_cors import CORS
from resources.dogs import dog
import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(dog, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(dog, url_prefix='/api/v1/dogs')

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'Hello world'

@app.route('/sayhi')
def say_hello():
    #jsonify is a good way to pass responses -> formats as JSON
    return jsonify(msg='Hello', status=200, list=['Bob', 'Rick'])

@app.route('/sayhello/<name>')
def greeting(name):
    return jsonify(
        name='My name is '+ name
    )

#query strings
@app.route('/query')
def query():
    #url = http://localhost:8000/query?test=test_band
    #pass in what's between ? and = into request.args.get()
    band = request.args.get('test')
    return jsonify(
        band_name = band
    )

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)