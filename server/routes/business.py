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
    
# Get a Business (by ID)
@business.route('/<int:business_id>', methods=['GET'])
def get_business(business_id):
    try:
        # Get business by ID
        business = Business.query.get(business_id)

        # If business is found, return serialized business as JSON
        if business:
            return jsonify(business.serialize())
        # If business is not found, return error
        return jsonify({'error': 'Business not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Search Businesses (by Name, City, State, or Service)
@business.route('/search', methods=['GET'])
def search_businesses():
    try:
        # Get search query from request args
        query = request.args.get('query')

        # Search businesses
        businesses = Business.query.filter(
            (Business.name.ilike(f'%{query}%')) |
            (Business.city.ilike(f'%{query}%')) |
            (Business.state.ilike(f'%{query}%')) |
            (Business.services.any(Service.name.ilike(f'%{query}%')))
        ).all()

        # Return serialized businesses as JSON
        return jsonify([business.serialize() for business in businesses])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Get All Services for a Business
@business.route('/<int:business_id>/services', methods=['GET'])
def get_services(business_id):
    try:
        # Get business by ID
        business = Business.query.get(business_id)

        # If business is not found, return error
        if not business:
            return jsonify({'error': 'Business not found'}), 404

        # Return serialized services as JSON
        return jsonify([service.serialize() for service in business.services])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a Service for a Business (by ID)
@business.route('/<int:business_id>/service/<int:service_id>', methods=['GET'])
def get_service(business_id, service_id):
    try:
        # Get business by ID
        business = Business.query.get(business_id)

        # If business is not found, return error
        if not business:
            return jsonify({'error': 'Business not found'}), 404

        # Get business service by ID
        service = Service.query.filter_by(id=service_id, business_id=business_id).first()

        # If service is not found, return error
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        # Return serialized service as JSON
        return jsonify(service.serialize())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# POST
# Create a Business
@business.route('/new', methods=['POST'])
def create_business():
    try:
        # Get data from request
        data = request.json

        # Create a new Business object
        business = Business(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            phone_number=data['phone_number'],
            email=data['email'],
            password=data['password']
        )

        # Add Business to database
        db.session.add(business)
        db.session.commit()

        # Return serialized business as JSON
        return jsonify(business.serialize())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a Service for a Business
@business.route('/<int:business_id>/service/new', methods=['POST'])  
def create_service(business_id):
    try:
        # Get data from request
        data = request.json

        # Get business by ID
        business = Business.query.get(business_id)

        # If business is not found, return error
        if not business:
            return jsonify({'error': 'Business not found'}), 404

        # Create a new Service object
        service = Service(
            name=data['name'],
            duration=data['duration'],
            price=data['price'],
            description=data['description'],
            business_id=business_id
        )

        # Add Service to database
        db.session.add(service)
        db.session.commit()

        # Return serialized service as JSON
        return jsonify(business.serialize())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# PUT
# Update a Business
@business.route('/<int:business_id>/update', methods=['PUT'])
def update_business(business_id):
    try:
        # Get data from request
        data = request.json

        # Get business by ID
        business = Business.query.get(business_id)

        # If business is not found, return error
        if not business:
            return jsonify({'error': 'Business not found'}), 404

        # Update business attributes
        if 'name' in data:
            business.name = data['name']
        if 'address' in data:
            business.address = data['address']
        if 'city' in data:
            business.city = data['city']
        if 'state' in data:
            business.state = data['state']
        if 'phone_number' in data:
            business.phone_number = data['phone_number']
        if 'email' in data:
            business.email = data['email']

        # Commit changes to database
        db.session.commit()

        # Return serialized business as JSON
        return jsonify(business.serialize())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Update a Service for a Business
@business.route('/<int:business_id>/service/<int:service_id>/update', methods=['PUT'])
def update_service(business_id, service_id):
    try:
        # Get data from request
        data = request.json

        # Get business by ID
        business = Business.query.get(business_id)

        # If business is not found, return error
        if not business:
            return jsonify({'error': 'Business not found'}), 404
        
        # Get business service by ID
        service = Service.query.filter_by(id=service_id, business_id=business_id).first()

        # If service is not found, return error
        if not service:
            return jsonify({'error': 'Service not found'}), 404
        
        # Update service attributes
        if 'name' in data:
            service.name = data['name']
        if 'duration' in data:
            service.duration = data['duration']
        if 'price' in data:
            service.price = data['price']
        if 'description' in data:
            service.description = data['description']

        # Commit changes to database
        db.session.commit()

        # Return serialized service as JSON
        return jsonify(service.serialize())
    except Exception as e:
        return jsonify({'error': str(e)}), 500