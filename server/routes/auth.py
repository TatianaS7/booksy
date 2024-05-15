# Import Dependencies
from flask import Blueprint, request, jsonify
import json, bcrypt, os
from server.database import db
from flask_jwt_extended import create_access_token

# Import Models
from server.models import User

# Import Environment Variables
JWT_SECRET = os.getenv('JWT_SECRET')

# Define Blueprint
auth = Blueprint('auth', __name__)

# Define Routes

# Register
@auth.route('/register', methods=['POST'])
def create_user():
    try:
        # Get user data from request body
        data = json.loads(request.data)

        # Check if user already exists by email, phone number, or username
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify({'error': 'Phone number already exists'}), 400
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400   

        # Hash user password
        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        # Create new user
        user = User(
            full_name=data['full_name'],
            email=data['email'],
            username=data['username'],
            phone_number=data['phone_number'],
            password=hashed.decode('utf-8')
        )
        # Add user to database
        db.session.add(user)
        db.session.commit()

        # Serialize user to avoid JSON serialization errors
        serialized_user = user.serialize()

        # Create JWT token
        token = create_access_token(serialized_user, JWT_SECRET)
        
        # Return Token
        return jsonify({'success': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Login
@auth.route('/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # If user is found, check password
        if user:
            # If password is incorrect, return error
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return jsonify({'error': 'Invalid password'}), 401
            # If password is correct, create JWT token
            else:
                token = create_access_token({'email': email, 'password': password}, JWT_SECRET, algorithm='HS256')
                return jsonify({'success': token})
        # If user is not found, return error
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
