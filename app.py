# Basic outline for app.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from dotenv import find_dotenv, load_dotenv
from server.database import db
import os


# Import Seed Data function from server/__main__.py
from seed_data.main import seedData


# Import Environment Variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# Create Instance of Flask App
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')

    jwt = JWTManager(app)

    db.init_app(app)
    ma.init_app(app)

    # Import Routes
    from server.routes import user, business, auth

    # Routes
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, url_prefix='/user')
    # app.register_blueprint(business, url_prefix='/business')

    with app.app_context():
        db.create_all()
        seedData()

    return app

# Database Setup
app = create_app()



# Run the application
if __name__ == '__main__':
    app.run(debug=True)