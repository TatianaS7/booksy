# Import Libraries
import json
from os import environ as env
from urllib.parse import urlencode, quote_plus

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for


# Load Configuration
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


# Create Instance of Flask App
app = Flask(__name__)
app.secret_key = env.get('SECRET_KEY')


# Configure Authlib to handle authentication with Auth0
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get('AUTH0_CLIENT_ID'),
    client_secret=env.get('AUTH0_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid profile email',
    },  
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)