from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=False)
