# Import dependencies
from flask import Blueprint, request, jsonify
import json, bcrypt, os
from server.database import db
from datetime import datetime, time
from flask_jwt_extended import create_access_token

# Import models
from server.models import User, Appointment

# Import Environment Variables
JWT_SECRET = os.getenv('JWT_SECRET')

# Define blueprint
user = Blueprint('user', __name__)


# Define routes

# POST
# Create an appointment
@user.route('/<int:user_id>/appointments', methods=['POST'])
def create_appointment(user_id):
    try:
        # Get user by ID
        user = User.query.get(user_id)
        
        # If user is found, create appointment
        if user:
            # Get appointment data from request body
            data = json.loads(request.data)

            # Convert date string to date object
            date_str = data['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

            # Convert time string to time object
            time_str = data['time']
            time_obj = datetime.strptime(time_str, '%H:%M').time()

            # Create new appointment
            appointment = Appointment(
                date=date_obj,  
                time=time_obj,
                user_id=user.id,
                business_id=data['business_id'],
                service_id=data['service_id'],
                notes=data['notes']
            )
            # Add appointment to database
            db.session.add(appointment)
            db.session.commit()
            # Return serialized appointment as JSON
            return jsonify({"message": "Appointment created successfully"})
        # If user is not found, return error
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# GET
# All Users
@user.route('/all', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# User Profile
@user.route('/profile', methods=['GET'])
def get_user():
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()
        # If user is found, return serialized user as JSON
        if user:
            # Create a dictionary with user data excluding the password
            user_data = {
                'full_name': user.full_name,
                'email': user.email,
                'username': user.username,
                'phone_number': user.phone_number,
                'appointments': [appointment.serialize() for appointment in user.appointments] if user.appointments else 'No appointments found'
            }
            return jsonify(user_data)
        # If user is not found, return error
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# All User Appointments
@user.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        # If user is found, return their appointments
        if user:
            # Get all appointments for user
            appointments = Appointment.query.filter_by(user_id=user.id).all()
            # Return serialized appointments as JSON
            return jsonify([appointment.serialize() for appointment in appointments])
        # If user is not found, return error
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Specific User Appointment
@user.route('/<int:user_id>/appointments/<int:id>', methods=['GET'])
def get_appointment(user_id, id):
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.get(user_id)
        if user:
            appointment = Appointment.query.filter_by(id=id, user_id=user.id).first()
            if appointment:
                return jsonify(appointment.serialize())
            return jsonify({'error': 'Appointment not found'}), 404
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# PUT
# Update User
@user.route('/<int:user_id>/profile', methods=['PUT'])
def update_user(user_id):
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Get user data from request body
            data = json.loads(request.data)
            # Update user data if the fields exist in the request data
            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'email' in data:
                user.email = data['email']
            if 'username' in data:
                user.username = data['username']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            db.session.commit()

            user_data = {
                'full_name': user.full_name,
                'email': user.email,
                'username': user.username,
                'phone_number': user.phone_number
            }

            return jsonify(user_data)
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update Password
@user.route('/<int:user_id>/profile/password', methods=['PUT'])
def update_password(user_id):
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(id=user_id).first()
        if user:
            # Get password data from request body
            data = json.loads(request.data)
            # Check if the current password is correct
            if bcrypt.checkpw(data['current_password'].encode('utf-8'), user.password):
                # Hash new password
                hashed = bcrypt.hashpw(data['new_password'].encode('utf-8'), bcrypt.gensalt())
                # Update user password
                new_password = hashed.decode('utf-8')
                user.password = new_password

                db.session.commit()
                return jsonify({'message': 'Password updated successfully'})
            return jsonify({'error': 'Invalid password'}), 401
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update Appointment
@user.route('/<int:user_id>/appointments/<int:id>', methods=['PUT'])
def update_appointment(user_id, id):
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.get(user_id)
        if user:
            appointment = Appointment.query.filter_by(id=id, user_id=user.id).first()
            if appointment:
                data = json.loads(request.data)

                if 'date' in data:
                    appointment.date = data['date']
                if 'time' in data:
                    appointment.time = data['time']
                if 'notes' in data:
                    appointment.notes = data['notes']
                if 'service_id' in data:
                    appointment.service_id = data['service_id']
                
                db.session.commit()
                return jsonify(appointment.serialize())
            return jsonify({'error': 'Appointment not found'}), 404
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE
# Specific Appointment
@user.route('/<int:user_id>/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(user_id, id):
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.get(user_id)
        if user:
            appointment = Appointment.query.filter_by(id=id, user_id=user.id).first()
            if appointment:
                db.session.delete(appointment)
                db.session.commit()
                return jsonify({'message': 'Appointment deleted successfully'})
            return jsonify({'error': 'Appointment not found'}), 404
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
