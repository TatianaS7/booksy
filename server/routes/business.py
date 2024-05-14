# Import Dependencies
from flask import Blueprint, request, jsonify
import json, os, bcrypt
from server.database import db
from datetime import datetime, time
from flask_jwt_extended import jwt_required, get_jwt_identity

# Import Models
from server.models import Business, Appointment, Service

# Import Environment Variables
JWT_SECRET = os.getenv('JWT_SECRET')    

# Define Blueprint
business = Blueprint('business', __name__)


# Define Routes

# GET
# Get All Businesses
@business.route('/all', methods=['GET'])
def get_businesses():
    try:
        # Get all businesses
        businesses = Business.query.all()

        # Return serialized businesses as JSON
        return jsonify([business.serialize() for business in businesses])
    except Exception as e:
        return jsonify({'error': str(e)}), 500