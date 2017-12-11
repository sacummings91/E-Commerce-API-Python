from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'JWT_KEY'
api = Api(app)


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
