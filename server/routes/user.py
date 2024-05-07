# Import dependencies
from flask import Blueprint, request, jsonify
from bcrypt import hashpw, gensalt, checkpw
import json, bcrypt, os


# Import database
from server import db


# Import models


# Define blueprint
user = Blueprint('user', __name__)


# Define routes

# GET// User can get their own appointment details


# POST// User can create an appointment


# PUT// User can update their appointment


# DELETE// User can cancel/delete their appointment