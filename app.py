# Basic outline for app.py
from flask import Flask, redirect, render_template, session, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import find_dotenv, load_dotenv
from server.database import db
import os, json

from authlib.integrations.flask_client import OAuth
from os import environ as env
from urllib.parse import quote_plus, urlencode



# Import Seed Data function from server/__main__.py
from seed_data.main import seedData


# Import Environment Variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# Create Instance of Flask App
ma = Marshmallow()

def create_app():
    app = Flask(__name__, static_folder='public')
    CORS(app)

    oauth = OAuth(app)
    app.oauth = oauth  

    # Set up the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('APP_SECRET_KEY')

    # Configure OAuth
    oauth.register(
        "auth0",
        client_id=os.getenv('AUTH0_CLIENT_ID'),
        client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/openid-configuration",
    )

    # Initialize the database
    db.init_app(app)
    ma.init_app(app)

    # Import Routes
    from server.routes import user, business, auth

    # Routes
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(business, url_prefix='/business')

    with app.app_context():
        db.create_all()
        seedData()

    return app

# Database Setup
app = create_app()



# OAuth Login
@app.route('/login')
def login():
    return app.oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# Callback
@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = app.oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# Home
@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))



# Run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))