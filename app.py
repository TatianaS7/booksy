# Basic outline for app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import find_dotenv, load_dotenv


# Import Environment Variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# Create Instance of Flask App
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
    return app

# Database Setup
app = create_app()

# Import Routes
from server.routes import user, business

# Routes
app.register_blueprint(user, url_prefix='/user')
# app.register_blueprint(business, url_prefix='/business')



if __name__ == '__main__':
    app.run(debug=True)